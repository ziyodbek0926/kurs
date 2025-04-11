import csv
from django.core.management.base import BaseCommand
from locations.models import Category, Location

class Command(BaseCommand):
    help = 'CSV fayldan joylashuvlarni import qilish'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV fayl yo\'li')
        parser.add_argument('category_name', type=str, help='Kategoriya nomi')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        category_name = options['category_name']

        # Kategoriyani topish yoki yaratish
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'emoji': '📍'}  # Default emoji
        )

        if created:
            self.stdout.write(f'Yangi kategoriya yaratildi: {category_name}')

        # CSV faylni o'qish
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Joylashuvni yaratish
                    Location.objects.create(
                        name=row['name'],
                        description=row.get('description', ''),
                        address=row['address'],
                        working_hours=row.get('working_hours', ''),
                        contact=row.get('contact', ''),
                        latitude=float(row['latitude']),
                        longitude=float(row['longitude']),
                        category=category
                    )
                    self.stdout.write(f'Joylashuv qo\'shildi: {row["name"]}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Xatolik: {row["name"]} - {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import muvaffaqiyatli yakunlandi!')) 