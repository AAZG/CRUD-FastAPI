from fastapi import FastAPI, HTTPException, status, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import datetime
from typing import Union, List
from routers.models_api import MovieAPI, User, JWTBearer
from routers.data import films
from routers.config_api import create_configuration_fastapi
from routers.jwt_manager import create_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from middlewares.error_handler import ErrorHandler

# Creación de una instancia de nuestra API
app = FastAPI()
create_configuration_fastapi(app)
         
app.add_middleware = ErrorHandler     
         
Base.metadata.create_all(bind=engine)



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
    
    

# creaciòn de la ruta peliculas, y la etiqueta peliculas
@app.get('/films', 
         tags=['films'], 
         status_code=status.HTTP_200_OK,
         summary="All films",
         response_model=List[MovieAPI],
        #  dependencies=[Depends(JWTBearer())]
         )
def get_films() -> List[MovieAPI]: # devuelve el listado de las peliculas
    """
    Obtener todas las peliculas
    """
    try:
        db = Session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        result = db.query(MovieModel).all()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List films empty")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={
                                "message": "Get all films successfully",
                                "details": jsonable_encoder(result)
                                }
                            )


@app.get(path="/films/read/{id}", 
        tags=["films"], 
        status_code=status.HTTP_200_OK,
        summary="Movie by id",
        response_model=MovieAPI,
        dependencies=[Depends(JWTBearer())])
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> MovieAPI:
    """
    Obtener película por id por parámetro de ruta
    """
    try:
        db = Session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        result = db.query(MovieModel).filter(MovieModel.id == id).one_or_none()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id movie not found")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={
                                "message": "Get movie por id successfully",
                                "details": jsonable_encoder(result)
                                }
                            )
    

@app.get('/films/read/', 
        tags=['films'],
        status_code=status.HTTP_200_OK,
        summary="Movie by category our year",
        response_model=List[MovieAPI],
        dependencies=[Depends(JWTBearer())]
        )
# Cuando no se deja un parámetro en la ruta pero si en la función, fastAPI detecta que es por query
def get_movie_by_category_our_year(category: Union[str, None] = Query(None, min_length=5, max_length=20), 
                                   year: Union[int, None] = Query(None, ge=1900, le=datetime.date.today().year)) -> List[MovieAPI]:
    """
    Obtener película/as por una categoría o año por Query Parameters
    """
    try:
        db = Session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        if category is None and year is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coloque algo, no sea pendejo")
        
        elif year is None:
            result = db.query(MovieModel).filter(MovieModel.category == category).all()
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category of movie not found")
            print("DEBUGGER")
            return JSONResponse(status_code=status.HTTP_200_OK,
                    content={
                        "message": f"Get all films for category {category} successfully",
                        "details": jsonable_encoder(result)
                        }
                    )
        elif category is None:
            result = db.query(MovieModel).filter(MovieModel.year == year).all()
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Year of movie not found")
            print("DEBUGGER")
            return JSONResponse(status_code=status.HTTP_200_OK,
                    content={
                        "message": f"Get all films for year {year} successfully",
                        "details": jsonable_encoder(result)
                        }
                    )
        else:
            result = db.query(MovieModel).filter(MovieModel.category == category and MovieModel.year == year).all()
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category our year of movie not found")
            print("DEBUGGER")
            return JSONResponse(status_code=status.HTTP_200_OK,
                    content={
                        "message": f"Get all films for year {year} and category {category} successfully",
                        "details": jsonable_encoder(result)
                        }
                    )


# class YourSchema(BaseModel):
#     field_1: int
#     field_n: str

#     class Config:
#         orm_mode = True


@app.post('/films/create/', 
          tags=['films'], 
          status_code=status.HTTP_201_CREATED,
          summary="Add Movie to films", 
          response_model=dict,
          dependencies=[Depends(JWTBearer())]
          )
async def create_movie(movie: MovieAPI) -> dict:
    """
    Agregar una película por parámetros en el body, ID se coloca de manera automatica segun orden que sigue en nuestros "films"
    """
    try:
        db = Session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        new_movie = MovieModel(**movie.dict())
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
        return JSONResponse(status_code=status.HTTP_201_CREATED, 
                            content={"message": "Se ha registrado la película",
                                     "details": jsonable_encoder(new_movie)})
    

@app.put(
    "/films/update/{id}",
    tags=['films'],
    status_code=status.HTTP_200_OK,
    summary="Update movie", 
    response_model=dict,
    dependencies=[Depends(JWTBearer())]
    )
async def update_movie( movie: MovieAPI, id: int = Path(ge=1, le=2000))  -> dict:
    """
    Actualizar una película por parámetros en el body buscando por el parámetro de ID
    """
    try:
        db = Session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        movie_update = db.query(MovieModel).filter(MovieModel.id == id).one_or_none()
        if not movie_update: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID No found")
        movie_update.update(movie.dict(exclude_unset=True))
        db.commit()
        db.refresh(movie_update)
        return JSONResponse(status_code=status.HTTP_200_OK, 
                            content={"message": "Updated movie successfully"}
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
        db = Session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        movie_delete = db.query(MovieModel).where(MovieModel.id == id).one_or_none()

        if movie_delete: 
            db.delete(movie_delete)
            db.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, 
                                content={
                                    "message": "Deleted movie successfully",
                                    "details": jsonable_encoder(movie_delete)
                                    })
            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID No found")
    
    
    
# @app.delete(
#     "/films/delete/",
#     tags=['films'],
#     status_code=status.HTTP_200_OK,
#     summary="Delete all movie", 
#     response_model=dict,
#     dependencies=[Depends(JWTBearer())]
#     )
# async def delete_all_movie() -> dict:
#     """
#     Eliminar una película por el parámetro de ID
#     """
#     try:
#         db = Session()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#     else:
#         all_films_delete = db.query(MovieModel).all()
#         if not all_films_delete:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List films empty")
        
#         db.delete(all_films_delete)
#         db.commit()
#         return JSONResponse(status_code=status.HTTP_200_OK,
#                             content={
#                                 "message": "Delete all films successfully",
#                                 "details": jsonable_encoder(all_films_delete)
#                                 }
#                             )