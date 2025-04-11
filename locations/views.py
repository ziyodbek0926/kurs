from django.shortcuts import render
from django.http import JsonResponse
from .models import Location, Category
from math import radians, sin, cos, sqrt, atan2
import requests
import json

def calculate_distance(lat1, lon1, lat2, lon2):
    """Haversine formulasi orqali masofani hisoblash"""
    R = 6371  # Yer radiusi (km)

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return round(distance, 2)

def search_locations(request):
    """Joylashuvlarni qidirish"""
    try:
        # Parametrlarni olish
        lat = float(request.GET.get('latitude'))
        lon = float(request.GET.get('longitude'))
        category_id = request.GET.get('category')
        radius = float(request.GET.get('radius', 5))  # Default 5 km

        # Joylashuvlarni olish
        locations = Location.objects.filter(is_active=True)
        if category_id:
            locations = locations.filter(category_id=category_id)

        # Masofani hisoblash va filtrlash
        result = []
        for loc in locations:
            distance = calculate_distance(lat, lon, loc.latitude, loc.longitude)
            if distance <= radius:
                result.append({
                    'id': loc.id,
                    'name': loc.name,
                    'description': loc.description,
                    'address': loc.address,
                    'working_hours': loc.working_hours,
                    'contact': loc.contact,
                    'latitude': loc.latitude,
                    'longitude': loc.longitude,
                    'distance': distance,
                    'category': {
                        'id': loc.category.id,
                        'name': loc.category.name,
                        'emoji': loc.category.emoji
                    }
                })

        # Masofaga qarab tartiblash
        result.sort(key=lambda x: x['distance'])

        # Agar natijalar yetarli bo'lmasa, OpenStreetMap dan qo'shimcha ma'lumotlarni olish
        if len(result) < 5 and category_id:
            osm_results = get_osm_locations(lat, lon, category_id, radius)
            result.extend(osm_results)

        return JsonResponse({
            'status': 'success',
            'count': len(result),
            'locations': result
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def get_osm_locations(lat, lon, category_id, radius):
    """OpenStreetMap dan joylashuvlarni olish"""
    try:
        # Kategoriyani olish
        category = Category.objects.get(id=category_id)
        
        # Kategoriya uchun OSM taglarini aniqlash
        osm_tags = get_osm_tags_for_category(category)
        
        # Overpass API so'rovi
        query = f"""
        [out:json][timeout:25];
        (
          node{osm_tags}(around:{radius*1000},{lat},{lon});
          way{osm_tags}(around:{radius*1000},{lat},{lon});
          relation{osm_tags}(around:{radius*1000},{lat},{lon});
        );
        out body;
        >;
        out skel qt;
        """
        
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query
        )
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        results = []
        
        for element in data.get('elements', []):
            if 'tags' not in element:
                continue
                
            tags = element['tags']
            
            # Joylashuv ma'lumotlarini olish
            name = tags.get('name', 'Nomsiz joy')
            address = tags.get('addr:street', '')
            if tags.get('addr:housenumber'):
                address += f", {tags['addr:housenumber']}"
            
            # Koordinatalarni olish
            if element['type'] == 'node':
                elem_lat = element['lat']
                elem_lon = element['lon']
            else:
                # Way va relation uchun markaz nuqtasini olish
                if 'center' in element:
                    elem_lat = element['center']['lat']
                    elem_lon = element['center']['lon']
                else:
                    continue
            
            # Masofani hisoblash
            distance = calculate_distance(lat, lon, elem_lat, elem_lon)
            
            results.append({
                'id': f"osm_{element['id']}",
                'name': name,
                'description': tags.get('description', ''),
                'address': address,
                'working_hours': tags.get('opening_hours', ''),
                'contact': tags.get('phone', ''),
                'latitude': elem_lat,
                'longitude': elem_lon,
                'distance': distance,
                'category': {
                    'id': category.id,
                    'name': category.name,
                    'emoji': category.emoji
                },
                'source': 'osm'
            })
        
        return results
    
    except Exception as e:
        print(f"OSM error: {str(e)}")
        return []

def get_osm_tags_for_category(category):
    """Kategoriya uchun OSM taglarini aniqlash"""
    # Kategoriya nomiga qarab OSM taglarini qaytarish
    category_name = category.name.lower()
    
    if 'do\'kon' in category_name or 'magazin' in category_name:
        return '(shop)'
    elif 'avto' in category_name or 'mashina' in category_name:
        return '(amenity=car_service|amenity=car_wash|amenity=car_repair)'
    elif 'shifoxona' in category_name or 'klinika' in category_name or 'dorixona' in category_name:
        return '(amenity=hospital|amenity=clinic|amenity=pharmacy)'
    elif 'restoran' in category_name or 'kafe' in category_name or 'taomnoma' in category_name:
        return '(amenity=restaurant|amenity=cafe)'
    elif 'maktab' in category_name or 'universitet' in category_name or 'kollej' in category_name:
        return '(amenity=school|amenity=university|amenity=college)'
    elif 'bank' in category_name or 'kassa' in category_name:
        return '(amenity=bank|amenity=atm)'
    else:
        return '(amenity)'

def get_categories(request):
    """Kategoriyalar ro'yxatini olish"""
    categories = Category.objects.all()
    return JsonResponse({
        'status': 'success',
        'categories': list(categories.values('id', 'name', 'emoji'))
    })
