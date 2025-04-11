import os
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from locations.models import Location, Category

class Command(BaseCommand):
    help = 'Import locations from Google Places API'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help='Category name')
        parser.add_argument('latitude', type=float, help='Center latitude')
        parser.add_argument('longitude', type=float, help='Center longitude')
        parser.add_argument('--radius', type=int, default=5000, help='Search radius in meters')
        parser.add_argument('--type', type=str, default='establishment', help='Place type')

    def handle(self, *args, **options):
        category_name = options['category']
        latitude = options['latitude']
        longitude = options['longitude']
        radius = options['radius']
        place_type = options['type']

        # Get or create category
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'emoji': '🏪'}
        )

        # Google Places API endpoint
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        
        # Parameters for the API request
        params = {
            'location': f'{latitude},{longitude}',
            'radius': radius,
            'type': place_type,
            'key': settings.GOOGLE_MAPS_API_KEY
        }

        try:
            # Make API request
            response = requests.get(url, params=params)
            data = response.json()

            if data['status'] == 'OK':
                for place in data['results']:
                    # Get place details
                    place_id = place['place_id']
                    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
                    details_params = {
                        'place_id': place_id,
                        'fields': 'name,formatted_address,formatted_phone_number,opening_hours,website',
                        'key': settings.GOOGLE_MAPS_API_KEY
                    }
                    
                    details_response = requests.get(details_url, params=details_params)
                    details_data = details_response.json()

                    if details_data['status'] == 'OK':
                        place_details = details_data['result']
                        
                        # Create location
                        Location.objects.create(
                            name=place_details.get('name', ''),
                            description='',
                            category=category,
                            address=place_details.get('formatted_address', ''),
                            working_hours=str(place_details.get('opening_hours', {}).get('weekday_text', [])),
                            contact=place_details.get('formatted_phone_number', ''),
                            latitude=place['geometry']['location']['lat'],
                            longitude=place['geometry']['location']['lng']
                        )
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully imported {place_details.get("name", "")}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Could not get details for place {place.get("name", "")}')
                        )
            else:
                self.stdout.write(
                    self.style.ERROR(f'API request failed: {data["status"]}')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            ) 