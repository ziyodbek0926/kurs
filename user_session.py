from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserLocation:
    latitude: float
    longitude: float
    timestamp: datetime

class UserSession:
    def __init__(self):
        self._sessions: Dict[int, dict] = {}
    
    def set_location(self, user_id: int, latitude: float, longitude: float):
        """Foydalanuvchi joylashuvini saqlash"""
        if user_id not in self._sessions:
            self._sessions[user_id] = {}
        
        self._sessions[user_id]['location'] = UserLocation(
            latitude=latitude,
            longitude=longitude,
            timestamp=datetime.now()
        )
    
    def get_location(self, user_id: int) -> Optional[UserLocation]:
        """Foydalanuvchi joylashuvini olish"""
        session = self._sessions.get(user_id, {})
        return session.get('location')
    
    def set_category(self, user_id: int, category_id: int):
        """Foydalanuvchi tanlagan kategoriyani saqlash"""
        if user_id not in self._sessions:
            self._sessions[user_id] = {}
        
        self._sessions[user_id]['category_id'] = category_id
    
    def get_category(self, user_id: int) -> Optional[int]:
        """Foydalanuvchi tanlagan kategoriyani olish"""
        session = self._sessions.get(user_id, {})
        return session.get('category_id')
    
    def clear_session(self, user_id: int):
        """Foydalanuvchi sessiyasini tozalash"""
        if user_id in self._sessions:
            del self._sessions[user_id]

user_session = UserSession()