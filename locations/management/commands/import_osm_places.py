import os
from django.core.management.base import BaseCommand
import requests
from locations.models import Location, Category
import time

class Command(BaseCommand):
    help = 'Import locations from OpenStreetMap using Overpass API'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help='Category name')
        parser.add_argument('latitude', type=float, help='Center latitude')
        parser.add_argument('longitude', type=float, help='Center longitude')
        parser.add_argument('--radius', type=int, default=1000, help='Search radius in meters')
        parser.add_argument('--type', type=str, default='shop', help='OSM place type')

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

        # Overpass API endpoint
        overpass_url = "https://overpass-api.de/api/interpreter"

        # Overpass QL query
        query = f"""
        [out:json][timeout:25];
        (
          node["{place_type}"](around:{radius},{latitude},{longitude});
          way["{place_type}"](around:{radius},{latitude},{longitude});
          relation["{place_type}"](around:{radius},{latitude},{longitude});
        );
        out body;
        >;
        out skel qt;
        """

        try:
            # Make API request
            response = requests.post(overpass_url, data=query)
            data = response.json()

            if 'elements' in data:
                for element in data['elements']:
                    if 'tags' in element:
                        tags = element['tags']
                        
                        # Get coordinates
                        if element['type'] == 'node':
                            lat = element['lat']
                            lon = element['lon']
                        else:
                            # For ways and relations, use center point
                            lat = sum(node['lat'] for node in element.get('nodes', [])) / len(element.get('nodes', [])) if element.get('nodes') else latitude
                            lon = sum(node['lon'] for node in element.get('nodes', [])) / len(element.get('nodes', [])) if element.get('nodes') else longitude

                        # Create location
                        Location.objects.create(
                            name=tags.get('name', 'Unknown Place'),
                            description=tags.get('description', ''),
                            category=category,
                            address=tags.get('addr:street', '') + ' ' + tags.get('addr:housenumber', ''),
                            working_hours=tags.get('opening_hours', ''),
                            contact=tags.get('phone', ''),
                            latitude=lat,
                            longitude=lon
                        )
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully imported {tags.get("name", "Unknown Place")}')
                        )
                        
                        # Sleep to avoid rate limiting
                        time.sleep(0.1)
            else:
                self.stdout.write(
                    self.style.WARNING('No places found in the specified area')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            ) 