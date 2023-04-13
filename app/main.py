from fastapi import FastAPI
from utils.config_api import create_configuration_fastapi
from config.database import engine, Base

# Creación de una instancia de nuestra API
app = FastAPI()
create_configuration_fastapi(app)

Base.metadata.create_all(bind=engine)