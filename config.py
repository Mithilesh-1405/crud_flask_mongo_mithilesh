import os
from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='secret-key')
    MONGO_URI= config('MONGO_URI', default='mongodb+srv://user:user@cluster0.q4jwf23.mongodb.net/crud_db')