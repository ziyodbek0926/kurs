# 📍 Joylashuvlar Qidiruv Boti

Bu loyiha OpenStreetMap ma'lumotlari asosida ishlaydi va foydalanuvchilarga yaqin atrofdagi joylarni topishda yordam beradi.

## 🛠 Texnologiyalar

- Python 3.8+
- Django 4.2+
- PostgreSQL + PostGIS
- Telegram Bot API (aiogram 3.x)
- OpenStreetMap + Overpass API

## 🚀 O'rnatish

1. Repositoriyani klonlash:
```bash
git clone https://github.com/ziyodbek0926/kurs.git
cd kurs
```

2. Virtual muhit yaratish va faollashtirish:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac uchun
# yoki
venv\Scripts\activate  # Windows uchun
```

3. Kerakli kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

4. PostgreSQL va PostGIS o'rnatish:
```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib postgis
```

5. Ma'lumotlar bazasini yaratish:
```bash
sudo -u postgres psql

CREATE DATABASE location_db;
CREATE USER location_user WITH PASSWORD 'location12345';
ALTER ROLE location_user SET client_encoding TO 'utf8';
ALTER ROLE location_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE location_user SET timezone TO 'Asia/Tashkent';
GRANT ALL PRIVILEGES ON DATABASE location_db TO location_user;
\c location_db
CREATE EXTENSION postgis;
\q
```

6. `.env` faylini yaratish:
```env
# Bot Token
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Database settings
DB_NAME=location_db
DB_USER=location_user
DB_PASSWORD=location12345
DB_HOST=localhost
DB_PORT=5432

# Django settings
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

7. Django migratsiyalarini bajarish:
```bash
python manage.py makemigrations
python manage.py migrate
```

8. Admin foydalanuvchini yaratish:
```bash
python manage.py createsuperuser
```

9. Ma'lumotlarni yuklash:
```bash
python init_data.py
```

## 🚀 Ishga tushirish

1. Django serverni ishga tushirish:
```bash
python manage.py runserver
```

2. Botni ishga tushirish (yangi terminal oynasida):
```bash
python bot.py
```

## 📱 Botdan foydalanish

1. Telegram orqali botni topish
2. `/start` buyrug'ini yuborish
3. Kategoriyani tanlash
4. Joylashuvni yuborish
5. Yaqin atrofdagi joylar ro'yxatini olish

## 👨‍💻 Admin panel

Admin panelga kirish: http://localhost:8000/admin

Admin panel orqali:
- Kategoriyalarni boshqarish
- Lokatsiyalarni boshqarish
- Foydalanuvchilar faolligini kuzatish
- Qidiruvlar statistikasini ko'rish

## 📊 Funksiyalar

- 8 ta asosiy kategoriya
- 2 km radius ichidagi joylarni qidirish
- Har bir joy uchun:
  - Nomi
  - Manzili
  - Ish vaqti
  - Kontakt ma'lumotlari
  - Masofa
  - Xaritada ko'rish havolasi