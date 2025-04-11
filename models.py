from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from database import Base

class Category(Base):
    """
    Kategoriyalar jadvali:
    - id: kategoriya identifikatori
    - name: kategoriya nomi
    - emoji: kategoriya emojisi
    - locations: kategoriyaga tegishli joylar (Location bilan bog'lanish)
    """
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    locations = relationship("Location", back_populates="category")

class Location(Base):
    """
    Joylar jadvali:
    - id: joy identifikatori
    - name: joy nomi
    - description: tavsifi
    - address: manzili
    - working_hours: ish vaqti
    - contact: kontakt ma'lumotlari
    - location: geografik koordinatalari (PostGIS Point)
    - category_id: kategoriya ID si
    """
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    address = Column(String, nullable=False)
    working_hours = Column(String)
    contact = Column(String)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    category = relationship("Category", back_populates="locations")

    @property
    def latitude(self):
        """Kenglikni olish"""
        if self.location is not None:
            return self.location.y
        return None

    @property
    def longitude(self):
        """Uzunlikni olish"""
        if self.location is not None:
            return self.location.x
        return None