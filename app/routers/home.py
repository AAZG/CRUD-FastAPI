from fastapi import APIRouter
from fastapi.responses import HTMLResponse

home_router = APIRouter()

#creacion de los endpoin
#los tags nos permite agrupar las rutas de la aplicacion
@home_router.get("/", tags=['home']) #Se agrega el home para agrupar determinadas rutas
def read_root():
    # Permite retornar cualquier cosa
    # return "Hello world"
    # return {"Hello": "World"}
    html_content = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>My FastAPI Website</title>
      </head>
      <body>
        <h1 style=color:red>Welcome to My FastAPI Website!</h1>
        <p>Here's some news:</p>
        <ul>
          <li><a href="http://127.0.0.1:8000/docs">Documentation</a></li>
        </ul>
      </body>
    </html>
    """
    print("DEBUGGER")
    return HTMLResponse(content=html_content, status_code=200)
    # return HTMLResponse('<h1 style=color:red> hola mundo </h1>') #utilizando html
    
    # http://127.0.0.1:8000/docs