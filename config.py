import os
from dotenv import load_dotenv
from decouple import config
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI= os.getenv('MONGO_URI')
    PORT = int(os.getenv('PORT', 5000))  
