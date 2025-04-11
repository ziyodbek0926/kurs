import os
from django.core.management.base import BaseCommand
import requests
from locations.models import Location, Category
import time

"""
Bu fayl - asosiy import fayli. Samarqand shahri uchun barcha turdagi joylarni 
(do'konlar, restoranlar, maktablar va h.k.) OpenStreetMap dan bir vaqtda import qiladi.

Ishlatish: python manage.py import_all_places "Samarqand" 39.6547 66.9597 --radius 10000
"""


class Command(BaseCommand):
    help = 'Import all places from OpenStreetMap for a specific city'

    def add_arguments(self, parser):
        parser.add_argument('city', type=str, help='City name')
        parser.add_argument('latitude', type=float, help='Center latitude')
        parser.add_argument('longitude', type=float, help='Center longitude')
        parser.add_argument('--radius', type=int, default=2000, help='Search radius in meters')

    def handle(self, *args, **options):
        city = options['city']
        latitude = options['latitude']
        longitude = options['longitude']
        radius = options['radius']

        # Define place types and their categories
        place_types = {
            'shop': {'name': "Do'konlar", 'emoji': "🏪"},
            'restaurant': {'name': "Restoranlar", 'emoji': "🍽"},
            'cafe': {'name': "Kafelar", 'emoji': "☕"},
            'pharmacy': {'name': "Aptekalar", 'emoji': "💊"},
            'university': {'name': "Universitetlar", 'emoji': "🎓"},
            'school': {'name': "Maktablar", 'emoji': "🏫"},
            'historic': {'name': "Me'moriy yodgorliklar", 'emoji': "🏛"},
            'mosque': {'name': "Me'morlar", 'emoji': "🕌"},
            'park': {'name': "Bog'lar", 'emoji': "🌳"},
            'marketplace': {'name': "Bozorlar", 'emoji': "🛍"},
            'hotel': {'name': "Mehmonxonalar", 'emoji': "🏨"},
            'museum': {'name': "Muzeylar", 'emoji': "🏛"},
            'bank': {'name': "Banklar", 'emoji': "🏦"},
            'hospital': {'name': "Kasalxonalar", 'emoji': "🏥"},
            'bus_station': {'name': "Avtobus bekati", 'emoji': "🚌"},
            'taxi': {'name': "Taksi", 'emoji': "🚕"},
            'cinema': {'name': "Kinoteatrlar", 'emoji': "🎬"},
            'theatre': {'name': "Teatrlar", 'emoji': "🎭"},
            'stadium': {'name': "Stadionlar", 'emoji': "⚽"},
            'library': {'name': "Kutubxonalar", 'emoji': "📚"}
        }

        # Overpass API endpoint
        overpass_url = "https://overpass-api.de/api/interpreter"

        for place_type, category_info in place_types.items():
            self.stdout.write(f"Importing {category_info['name']}...")

            # Get or create category
            category, created = Category.objects.get_or_create(
                name=category_info['name'],
                defaults={'emoji': category_info['emoji']}
            )

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
                    count = 0
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
                            
                            count += 1
                            
                            # Sleep to avoid rate limiting
                            time.sleep(0.1)
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully imported {count} {category_info["name"]}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'No {category_info["name"]} found in the specified area')
                    )

                # Sleep between categories to avoid rate limiting
                time.sleep(1)

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error importing {category_info["name"]}: {str(e)}')
                ) 