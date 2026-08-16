import os
from dotenv import load_dotenv

#Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config: 

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    SECRET_KEY = os.getenv('SECRET_KEY')

    #URI es la cadema de cpnexión a la base de datos PostgreSQL
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    #Evitar que SQLAlchemy rastrea modificaciones de objetos y emita señales, lo que 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
