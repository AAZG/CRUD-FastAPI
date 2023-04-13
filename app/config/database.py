import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Guardamos el nombre de la base de datos
sqlite_file_name = "../../database.sqlite"

# Leemos el directorio actual del archivo database
base_dir = os.path.dirname(os.path.realpath(__file__))

# sqlite:/// es la forma en la que se conecta a una base de datos, se usa el metodo join para unir las urls
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Representa el motor de la base de datos, con el comando “echo=True” para que al momento de realizar la base de datos,
#me muestre por consola lo que esta realizando, que seria el codigo
engine = create_engine(database_url, echo=True)

# Creacion de session para conectarse a la base de datos, se enlaza con el comando “bind” y se iguala a engine
Session = sessionmaker(bind=engine)

# Usamos esta funcion para manipular todas las tablas de la base de datos
Base = declarative_base()





# # Importamos módulos requeridos:
# from pathlib import Path
# from sqlalchemy import create_engine


# # Obtenemos la carpeta del módulo actual:
# BASE_DIR=PATH(__file__).parent
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Establecemos la ruta completa a nuestra base de datos:
# SQLITE_FILE=BASE_DIR.join('db.sqlite3')

# # Y construimos la URL
# SQLITE_URL=f'sqlite:///{SQLITE_FILE}'

# # Todo listo, creamos un engine
# engine=create_engine(SQLITE_URL, echo=True)