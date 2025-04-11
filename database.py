from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .env faylidagi muhit o'zgaruvchilarini yuklash
load_dotenv()

# Ma'lumotlar bazasi URL manzilini olish
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine yaratish
# Bu - ma'lumotlar bazasi bilan bog'lanish uchun asosiy komponent
engine = create_engine(DATABASE_URL)

# SessionLocal klassini yaratish
# Bu - ma'lumotlar bazasi bilan ishlash uchun sessiya yaratadi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base klassini yaratish
# Bu - modellar uchun asosiy klass
Base = declarative_base()

# Ma'lumotlar bazasi sessiyasini olish uchun funksiya
def get_db():
    """
    Ma'lumotlar bazasi sessiyasini yaratish va qaytarish
    Try-finally bloki orqali sessiya to'g'ri yopilishini ta'minlaydi
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()