# Codigo en consola
## Creacion del proyecto con Pipenvwrapper
makeproject curso_introduccion_FastAPI_3.9.15 --python 3.9.15

## Activar nuestro entorno virtual
useenv curso_introduccion_FastAPI_3.9.15

## lanzar nuestro servidor en WSL
python -m uvicorn main:app --reload
### banderas interesantes
--port 5000 --host 0.0.0.0 # con esta cambiamos el puerto e ip default requeridos

