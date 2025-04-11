import os
import django
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from asgiref.sync import sync_to_async
from user_session import user_session

# Django sozlamalarini o'rnatish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'location_admin.settings')
django.setup()

# Django modellarini import qilish
from locations.models import Category, Location, UserActivity, UserSearch

# Logging sozlamalarini o'rnatish
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot tokenini olish va botni yaratish
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchi faoliyatini saqlash funksiyasi
@sync_to_async
def save_user_activity(user: types.User):
    """
    Foydalanuvchi faoliyatini ma'lumotlar bazasiga saqlaydi
    user: Telegram foydalanuvchisi
    """
    activity, created = UserActivity.objects.get_or_create(
        user_id=user.id,
        defaults={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    )
    activity.total_searches += 1
    activity.save()
    return activity

# Kategoriyalarni olish funksiyasi
@sync_to_async
def get_categories():
    """
    Barcha mavjud kategoriyalarni ma'lumotlar bazasidan oladi
    """
    return list(Category.objects.all())

# Joylashuvlarni qidirish funksiyasi
@sync_to_async
def search_locations(category_id, lat, lon, radius=2):
    """
    Berilgan koordinata atrofidan joylarni qidiradi
    category_id: Kategoriya ID si
    lat, lon: Koordinatalar
    radius: Qidiruv radiusi (km)
    """
    try:
        user_location = Point(lon, lat, srid=4326)
        category = Category.objects.get(id=category_id)
        
        locations = Location.objects.filter(
            category=category,
            is_active=True
        ).annotate(
            distance=Distance('point', user_location)
        ).filter(
            distance__lte=D(km=radius)
        ).order_by('distance')[:10]
        
        results = []
        for loc in locations:
            results.append({
                'id': loc.id,
                'name': loc.name,
                'address': loc.address,
                'working_hours': loc.working_hours or 'Ish vaqti ko\'rsatilmagan',
                'contact': loc.contact or 'Telefon raqam ko\'rsatilmagan',
                'latitude': loc.point.y,
                'longitude': loc.point.x,
                'distance': round(loc.distance.km, 2)
            })
        
        return results, category
    except Exception as e:
        logger.error(f"Qidirishda xatolik: {e}")
        return [], None

# Start komandasi uchun handler
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    /start komandasi uchun handler
    Foydalanuvchiga salomlashadi va kategoriyalarni ko'rsatadi
    """
    try:
        user = message.from_user
        await save_user_activity(user)
        
        welcome_text = (
            f"Assalomu alaykum, {user.first_name}! 👋\n\n"
            "Men sizga yaqin atrofda joylashgan qiziqarli joylarni topishda yordam beraman. "
            "Quyidagi kategoriyalardan birini tanlang:"
        )
        
        categories = await get_categories()
        keyboard = []
        row = []
        
        for i, category in enumerate(categories):
            button = InlineKeyboardButton(
                text=f"{category.emoji} {category.name}",
                callback_data=f"category_{category.id}"
            )
            row.append(button)
            
            if len(row) == 2 or i == len(categories) - 1:
                keyboard.append(row)
                row = []
        
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await message.answer(welcome_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Start komandasida xatolik: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

# Kategoriya tanlanganda ishlaydigan handler
@dp.callback_query(lambda c: c.data.startswith('category_'))
async def process_category(callback_query: types.CallbackQuery):
    """
    Kategoriya tanlanganda ishga tushadigan handler
    Foydalanuvchidan joylashuvni so'raydi
    """
    try:
        await callback_query.answer()
        
        category_id = int(callback_query.data.split('_')[1])
        category = await sync_to_async(Category.objects.get)(id=category_id)
        
        await save_user_activity(callback_query.from_user)
        
        # Joylashuv tugmasini yaratish
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
            is_persistent=True
        )
        
        message_text = (
            f"🎯 {category.emoji} {category.name} kategoriyasini tanladingiz.\n\n"
            "Endi joylashuvingizni yuboring, men sizga 2 km radiusda joylashgan eng yaqin joylarni topib beraman.\n\n"
            "📱 Mobil telefonda bo'lsangiz, pastdagi '📍 Joylashuvni yuborish' tugmasini bosing.\n"
            "💻 Kompyuterda bo'lsangiz, Telegram mobil ilovasidan foydalaning."
        )
        
        await callback_query.message.answer(message_text, reply_markup=keyboard)
        user_session.set_category(callback_query.from_user.id, category_id)
    except Exception as e:
        logger.error(f"Kategoriya tanlashda xatolik: {e}")
        await callback_query.message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

# Joylashuv qabul qilinganda ishlaydigan handler
@dp.message(lambda message: message.location is not None)
async def process_location(message: types.Message):
    """
    Foydalanuvchi yuborgan joylashuvni qayta ishlaydi
    Va yaqin atrofdagi joylarni qaytaradi
    """
    try:
        user = message.from_user
        location = message.location
        
        await save_user_activity(user)
        
        category_id = user_session.get_category(user.id)
        if not category_id:
            await message.answer(
                "❌ Kategoriya topilmadi. Iltimos, /start buyrug'ini yuborib, qaytadan urinib ko'ring."
            )
            return
        
        # Joylashuvlarni qidirish
        locations, category = await search_locations(category_id, location.latitude, location.longitude)
        
        if not locations:
            await message.answer(
                f"❌ Afsuski, {category.emoji} {category.name} kategoriyasida "
                "2 km radiusda hech qanday joy topilmadi."
            )
            return
        
        # Qidiruv natijalarini saqlash
        await sync_to_async(UserSearch.objects.create)(
            user_id=user.id,
            category=category,
            latitude=location.latitude,
            longitude=location.longitude,
            results_count=len(locations)
        )
        
        # Natijalarni yuborish
        await message.answer(
            f"🔍 {category.emoji} {category.name} kategoriyasida topilgan eng yaqin joylar:\n"
            f"(2 km radius ichida)"
        )
        
        for loc in locations:
            text = (
                f"🏢 {loc['name']}\n"
                f"📍 {loc['address']}\n"
                f"⏰ {loc['working_hours']}\n"
                f"📞 {loc['contact']}\n"
                f"📏 Masofa: {loc['distance']} km\n"
            )
            
            # Joylashuv havolasi uchun tugma
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="🗺 Xaritada ko'rish",
                    url=f"https://www.google.com/maps/dir/?api=1&origin={location.latitude},{location.longitude}&destination={loc['latitude']},{loc['longitude']}&travelmode=walking"
                )
            ]])
            
            await message.answer(text, reply_markup=keyboard)
        
        # Kategoriyalarni qayta ko'rsatish
        await cmd_start(message)
        
    except Exception as e:
        logger.error(f"Joylashuvni qayta ishlashda xatolik: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

# Botni ishga tushirish
async def main():
    """
    Botni ishga tushirish funksiyasi
    """
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())