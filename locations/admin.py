from django.contrib import admin
from .models import Category, Location, UserActivity, UserSearch
# Admin panelda kategoriyalarni ko'rsatish
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Kategoriyalar uchun admin panel sozlamalari:
    - list_display: ro'yxatda ko'rsatiladigan maydonlar
    - search_fields: qidiruv maydonlari
    - ordering: tartiblash
    """
    list_display = ('name', 'emoji', 'created_at')  # Ko'rsatiladigan ustunlar
    search_fields = ('name',)  # Qidiruv maydoni
    ordering = ('-created_at',)  # Tartiblash (eng yangilari yuqorida)

# Admin panelda lokatsiyalarni ko'rsatish
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Lokatsiyalar uchun admin panel sozlamalari:
    - list_display: ro'yxatda ko'rsatiladigan maydonlar
    - list_filter: filtrlash maydonlari
    - search_fields: qidiruv maydonlari
    - ordering: tartiblash
    """
    list_display = ('name', 'category', 'address', 'is_active')  # Ko'rsatiladigan ustunlar
    list_filter = ('category', 'is_active')  # Filtrlash
    search_fields = ('name', 'address')  # Qidiruv maydonlari
    ordering = ('category', 'name')  # Tartiblash

# Admin panelda foydalanuvchilar faolligini ko'rsatish
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """
    Foydalanuvchilar faolligi uchun admin panel sozlamalari:
    - list_display: ro'yxatda ko'rsatiladigan maydonlar
    - list_filter: filtrlash maydonlari
    - search_fields: qidiruv maydonlari
    """
    list_display = ('user_id', 'username', 'first_name', 'last_name', 'total_searches', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user_id', 'username', 'first_name', 'last_name')

# Admin panelda qidiruvlarni ko'rsatish
@admin.register(UserSearch)
class UserSearchAdmin(admin.ModelAdmin):
    """
    Qidiruvlar uchun admin panel sozlamalari:
    - list_display: ro'yxatda ko'rsatiladigan maydonlar
    - list_filter: filtrlash maydonlari
    - search_fields: qidiruv maydonlari
    """
    list_display = ('user_id', 'category', 'search_time', 'results_count')
    list_filter = ('category', 'search_time')
    search_fields = ('user_id',)