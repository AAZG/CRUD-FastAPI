from fastapi import FastAPI, HTTPException, status, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from models import Movie, User, JWTBearer
from data import films
from config import create_configuration_fastapi
from jwt_manager import create_token
import datetime
from typing import Union, List


# Creación de una instancia de nuestra API
app = FastAPI()
create_configuration_fastapi(app)
         

#creacion de los endpoin
#los tags nos permite agrupar las rutas de la aplicacion
@app.get("/", tags=['home']) #Se agrega el home para agrupar determinadas rutas
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
          <li>News item 1</li>
          <li>News item 2</li>
          <li>News item 3</li>
        </ul>
      </body>
    </html>
    """
    print("DEBUGGER")
    return HTMLResponse(content=html_content, status_code=200)
    # return HTMLResponse('<h1 style=color:red> hola mundo </h1>') #utilizando html


@app.post("/login", tags=['auth'])
def login(user: User):
    if (user.email == "admin@gmail.com" and user.password == 12345):
        token: str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, 
                            content={
                                "message": "Get all films successfully",
                                "details": token
                                }
                            )
    else:
        return JSONResponse(status_code=401, 
                            content={"message": "Credenciales inválidas, intente de nuevo"})
    
    # print("DEBUGGER")
    # return user


# creaciòn de la ruta peliculas, y la etiqueta peliculas
@app.get('/films', 
         tags=['films'], 
         status_code=status.HTTP_200_OK,
         summary="All films",
         response_model=List[Movie],
         dependencies=[Depends(JWTBearer())])
def get_films() -> List[Movie]: # devuelve el listado de las peliculas
    """
    Obtener todas las peliculas
    """
    try:
        list_all_movie = films
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        if not list_all_movie:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List films empty")
        else:
            print("DEBUGGER")
            return JSONResponse(status_code=status.HTTP_200_OK,
                            content={
                                "message": "Get all films successfully",
                                "details": list_all_movie
                                }
                            )


@app.get(path="/films/read/{id}", 
        tags=["films"], 
        status_code=status.HTTP_200_OK,
        summary="Movie by id",
        response_model=Movie,
        dependencies=[Depends(JWTBearer())])
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:
    """
    Obtener película por id por parámetro de ruta
    """
    try:
        list_all_movie = films
        movie_by_id = [movie for movie in list_all_movie if movie['id'] == id]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        if not movie_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id movie not found")
        print("DEBUGGER")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={
                                "message": "Get movie por id successfully",
                                "details": movie_by_id[0]
                                }
                            )
    

@app.get('/films/read/', 
        tags=['films'],
        status_code=status.HTTP_200_OK,
        summary="Movie by category our year",
        response_model=List[Movie],
        dependencies=[Depends(JWTBearer())]
        )
# Cuando no se deja un parámetro en la ruta pero si en la función, fastAPI detecta que es por query
def get_movie_by_category_our_year(category: Union[str, None] = Query(None, min_length=5, max_length=20), 
                                   year: Union[int, None] = Query(None, ge=1900, le=datetime.date.today().year)) -> List[Movie]:
    """
    Obtener película/as por una categoría o año por Query Parameters
    """
    try:
        list_all_movie = films
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        if category is None and year is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coloque algo, no sea pendejo")
            
        elif year is None:
            movie_categorie = [movie for movie in list_all_movie if movie['category'] == category]
            if not movie_categorie:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category of movie not found")
            print("DEBUGGER")
            return JSONResponse(status_code=status.HTTP_200_OK,
                    content={
                        "message": f"Get all films for category {category} successfully",
                        "details": movie_categorie
                        }
                    )
        
        elif category is None:
            movie_year = [movie for movie in list_all_movie if movie['year'] == year]
            if not movie_year:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Year of movie not found")
            print("DEBUGGER")
        
            return JSONResponse(status_code=status.HTTP_200_OK,
            content={
                "message": f"Get all films for year {year} successfully",
                "details": movie_year
                }
            )
        
        else:
            movie_categorie_year = [movie for movie in list_all_movie if (movie['category'] == category and movie['year'] == year)]
            if not movie_categorie_year:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category our year of movie not found")
            print("DEBUGGER")
            
            return JSONResponse(status_code=status.HTTP_200_OK,
            content={
                "message": f"Get all films for year {year} and category {category} successfully",
                "details": movie_categorie_year
                }
            )


@app.post('/films/create/', 
          tags=['films'], 
          status_code=status.HTTP_201_CREATED,
          summary="Add Movie to films", 
          response_model=dict,
          dependencies=[Depends(JWTBearer())]
          )
async def create_movie(movie: Movie) -> dict:
    """
    Agregar una película por parámetros en el body, ID se coloca de manera automatica segun orden que sigue en nuestros "films"
    """
    try:
        list_all_movie = films
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        if list_all_movie:
            id = list_all_movie[-1]['id'] + 1
        else:
            id = 1
        
        movie_dict = movie.dict()
        movie_dict['id'] = id
        films.append(movie_dict)
        print("DEBUGGER")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={
                                "message": "Created movie successfully",
                                "details": films[-1]
                                }
                            )


@app.put(
    "/films/update/{id}",
    tags=['films'],
    status_code=status.HTTP_200_OK,
    summary="Update movie", 
    response_model=dict,
    dependencies=[Depends(JWTBearer())]
    # response_model_exclude={'id'}
    )
async def update_movie( movie: Movie, id: int = Path(ge=1, le=2000))  -> dict:
    """
    Actualizar una película por parámetros en el body buscando por el parámetro de ID
    """
    try:
        list_all_movie = films
        movie_by_id = [movie for movie in list_all_movie if movie['id'] == id]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        if not movie_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found! t(-_-t)")
        else:
            print("DEBUGGER")

            movie_dict = movie.dict()
            movie_dict['id'] = id
            films[id - 1] = movie_dict

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Updated movie successfully",
                    "details": films[id - 1]
                    }
                )
    


@app.delete(
    "/films/delete/{id}",
    tags=['films'],
    status_code=status.HTTP_200_OK,
    summary="Delete movie", 
    response_model=dict,
    dependencies=[Depends(JWTBearer())]
    )
async def delete_movie(id: int = Path(ge=1, le=2000)) -> dict:
    """
    Eliminar una película por el parámetro de ID
    """
    try:
        list_all_movie = films
        movie_by_id = [movie for movie in list_all_movie if movie['id'] == id]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        if not movie_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found! t(-_-t)")
        else:
            print("DEBUGGER")
            films.remove(movie_by_id[0])

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Deleted movie successfully",
                "details": movie_by_id[0]
                }
            )