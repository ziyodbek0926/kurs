"""
Django loyihasining boshqaruv skripti.
Bu fayl orqali:
- Ma'lumotlar bazasi migratsiyalari
- Development server ishga tushirish
- Management buyruqlarini bajarish
- va boshqa Django buyruqlarini bajarish mumkin
"""
import os
import sys

def main():
    """
    Asosiy funksiya:
    - Django sozlamalarini yuklaydi
    - Buyruqlarni qayta ishlaydi
    - Xatoliklarni ushlaydi
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'location_admin.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django import qilib bo'lmadi. U o'rnatilganiga va "
            "PYTHONPATH muhit o'zgaruvchisida mavjudligiga ishonch hosil qiling."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()