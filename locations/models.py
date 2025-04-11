from django.contrib.gis.db import models
from django.utils import timezone
# Category modeli - kategoriyalarni saqlash uchun
class Category(models.Model):
    """
    Bu model kategoriyalarni saqlash uchun:
    - name: kategoriya nomi (Do'konlar, Restoranlar va h.k.)
    - emoji: kategoriya uchun emoji belgisi
    - created_at: kategoriya qo'shilgan vaqt
    """
    name = models.CharField(max_length=100)  # Kategoriya nomi
    emoji = models.CharField(max_length=10)  # Emoji belgisi
    created_at = models.DateTimeField(default=timezone.now)  # Yaratilgan vaqti

    def __str__(self):
        """Kategoriyani admin panelda ko'rsatish formati"""
        return f"{self.emoji} {self.name}"

    class Meta:
        """
        Meta ma'lumotlar:
        - verbose_name: admin paneldagi yakka holdagi nomi
        - verbose_name_plural: admin paneldagi ko'plik holdagi nomi
        """
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

# Location modeli - joylar haqidagi ma'lumotlarni saqlash uchun
class Location(models.Model):
    """
    Bu model joylar haqidagi ma'lumotlarni saqlash uchun:
    - name: joy nomi
    - address: manzili
    - point: geografik koordinatalari (PostGIS Point)
    - category: kategoriyasi (Category modeliga bog'langan)
    - working_hours: ish vaqti
    - contact: kontakt ma'lumotlari
    - is_active: faol yoki faol emasligi
    - created_at: qo'shilgan vaqti
    """
    name = models.CharField(max_length=255)  # Joy nomi
    address = models.TextField()  # Manzili
    point = models.PointField(srid=4326)  # Geografik koordinatalari
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Kategoriyasi
    working_hours = models.CharField(max_length=255, null=True, blank=True)  # Ish vaqti
    contact = models.CharField(max_length=255, null=True, blank=True)  # Kontakt
    is_active = models.BooleanField(default=True)  # Faol/faol emas
    created_at = models.DateTimeField(default=timezone.now)  # Yaratilgan vaqti

    def __str__(self):
        """Joyni admin panelda ko'rsatish formati"""
        return self.name

    class Meta:
        """Meta ma'lumotlar"""
        verbose_name = 'Lokatsiya'
        verbose_name_plural = 'Lokatsiyalar'

# UserActivity modeli - foydalanuvchilar faolligini kuzatish uchun
class UserActivity(models.Model):
    """
    Bu model foydalanuvchilar faolligini kuzatish uchun:
    - user_id: Telegram foydalanuvchi ID si
    - username: Telegram username
    - first_name, last_name: ism va familiya
    - total_searches: qidiruvlar soni
    - is_active: faol yoki faol emasligi
    - last_seen: oxirgi faollik vaqti
    - created_at: ro'yxatdan o'tgan vaqti
    """
    user_id = models.BigIntegerField(unique=True)  # Telegram ID
    username = models.CharField(max_length=255, null=True, blank=True)  # Username
    first_name = models.CharField(max_length=255, null=True, blank=True)  # Ismi
    last_name = models.CharField(max_length=255, null=True, blank=True)  # Familiyasi
    total_searches = models.IntegerField(default=0)  # Qidiruvlar soni
    is_active = models.BooleanField(default=True)  # Faol/faol emas
    last_seen = models.DateTimeField(auto_now=True)  # Oxirgi faollik
    created_at = models.DateTimeField(default=timezone.now)  # Ro'yxatdan o'tgan vaqt

    def __str__(self):
        """Foydalanuvchini admin panelda ko'rsatish formati"""
        return f"{self.username or self.first_name or self.user_id}"

    class Meta:
        """Meta ma'lumotlar"""
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

# UserSearch modeli - foydalanuvchilar qidiruvlarini saqlash uchun
class UserSearch(models.Model):
    """
    Bu model foydalanuvchilar qidiruvlarini saqlash uchun:
    - user_id: Telegram foydalanuvchi ID si
    - category: qidirilgan kategoriya
    - latitude, longitude: qidiruv joylashuvi
    - results_count: topilgan natijalar soni
    - search_time: qidiruv vaqti
    """
    user_id = models.BigIntegerField()  # Telegram ID
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Kategoriya
    latitude = models.FloatField()  # Kenglik
    longitude = models.FloatField()  # Uzunlik
    results_count = models.IntegerField(default=0)  # Natijalar soni
    search_time = models.DateTimeField(default=timezone.now)  # Qidiruv vaqti

    def __str__(self):
        """Qidiruvni admin panelda ko'rsatish formati"""
        return f"Qidiruv: {self.user_id} - {self.category.name}"

    class Meta:
        """Meta ma'lumotlar"""
        verbose_name = 'Qidiruv'
        verbose_name_plural = 'Qidiruvlar'