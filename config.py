# config.py
import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/your_database_name")
    SECRET_KEY = os.urandom(24)
