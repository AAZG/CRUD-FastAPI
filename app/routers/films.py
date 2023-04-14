from fastapi import APIRouter
from fastapi import HTTPException, status, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Union, List
from config.database import Session
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
import datetime
from fastapi import HTTPException
from schemas.movie import MovieAPI
from services.films import FilmsService

films_router = APIRouter()


# creacion de la ruta peliculas, y la etiqueta peliculas
@films_router.get('/films', 
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
    db = Session()
    result = FilmsService(db).get_films()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List films empty")
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "message": "Get all films successfully",
                            "details": jsonable_encoder(result)
                            }
                        )


@films_router.get(path="/films/read/{id}", 
        tags=["films"], 
        status_code=status.HTTP_200_OK,
        summary="Movie by id",
        response_model=MovieAPI,
        dependencies=[Depends(JWTBearer())])
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> MovieAPI:
    """
    Obtener película por id por parámetro de ruta
    """
    db = Session()
    result = FilmsService(db).get_movie(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id movie not found")
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "message": "Get movie por id successfully",
                            "details": jsonable_encoder(result)
                            }
                        )
    

@films_router.get('/films/read/', 
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
    db = Session()
    if category is None and year is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coloque algo, no sea pendejo")
    
    elif year is None:
        result = FilmsService(db).get_films_by_category(category)
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
        result = FilmsService(db).get_films_by_year(year)
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
        result = FilmsService(db).get_films_by_category_and_year(category, year)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category our year of movie not found")
        print("DEBUGGER")
        return JSONResponse(status_code=status.HTTP_200_OK,
                content={
                    "message": f"Get all films for year {year} and category {category} successfully",
                    "details": jsonable_encoder(result)
                    }
                )


@films_router.post('/films/create/', 
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
    db = Session()
    new_movie = FilmsService(db).create_movie(movie)
    return JSONResponse(status_code=status.HTTP_201_CREATED, 
                        content={"message": "Se ha registrado la película"})
    

@films_router.put(
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
    db = Session()
    movie_update = FilmsService(db).get_movie_id(id)
    if not movie_update: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID No found")
    
    FilmsService(db).update_movie(id, movie)
    
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"message": "Updated movie successfully",
                                 "details": jsonable_encoder(movie_update)
                            }
                        )
        



@films_router.delete(
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
    db = Session()
    movie_delete = FilmsService(db).get_movie_id(id)

    if not movie_delete: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID No found")
    
    FilmsService(db).delete_movie(id)
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={
                            "message": "Deleted movie successfully",
                            "details": jsonable_encoder(movie_delete)
                            })
    
    
    
@films_router.delete(
    "/films/delete/",
    tags=['films'],
    status_code=status.HTTP_200_OK,
    summary="Delete all movie", 
    response_model=dict,
    dependencies=[Depends(JWTBearer())]
    )
async def delete_all_movie() -> dict:
    """
    Eliminar una película por el parámetro de ID
    """
    db = Session()
    all_films_delete = FilmsService(db).get_films()
    if not all_films_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List films empty")

    FilmsService(db).delete_all_movie()
    
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "message": "Delete all films successfully",
                            "details": jsonable_encoder(all_films_delete)
                            }
                        )