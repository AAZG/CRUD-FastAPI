# Codigo en consola
## Creacion del proyecto con Pipenvwrapper
makeproject curso_introduccion_FastAPI_3.9.15 --python 3.9.15

## Activar nuestro entorno virtual
useenv curso_introduccion_FastAPI_3.9.15

## lanzar nuestro servidor en WSL
python -m uvicorn main:app --reload
### banderas interesantes
--port 5000 --host 0.0.0.0 # con esta cambiamos el puerto e ip default requeridos


## HTTP response status code
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status


# Ramas creadas
git branch
git checkout -b main
git checkout -b FastAPI_CRUD
git checkout -b FastAPI_scheme
git checkout -b FastAPI_SQLAlchemy
git checkout -b 
git checkout -b 
git checkout -b 
git checkout -b 



# Push al repositorio
git push origin workflow_testing_api
git push --all origin


# hacer pruebas con pytest
pytest tests/tests_api.py
Aqui pidio: instalar pip install httpx, luego corri la linea anterior y funciono (yo trabaje con python 3.9.15)