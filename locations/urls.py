from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_locations, name='search_locations'),
    path('categories/', views.get_categories, name='get_categories'),
] 