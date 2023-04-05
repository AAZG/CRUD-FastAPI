from fastapi import FastAPI, HTTPException, status, Body
from fastapi.responses import HTMLResponse, JSONResponse
   

films = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'    
    },
        {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'    
    } 
]


#creación de una instancia de nuestra API
app = FastAPI(title="nombreAPP",
    description="un intento de api",
    version="0.0.1", #Colocar version en especifico
    terms_of_service="http://example.com/terms/",
    contact = {
        "name": "Fidelp27",
        "url": "https://fidelp27.github.io/portfolio/",
        "email": "telocreiste@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

#creacion del endpoin
#los tags nos permite agrupar las rutas de la aplicacion
@app.get("/", tags=['home']) #Se agrega el home para agrupar determinadas rutas
def read_root():
    return HTMLResponse('<h1 style=color:red> hola mundo </h1>') #utilizando html


#creaciòn de la ruta peliculas, y la etiqueta peliculas
@app.get('/films', 
         tags=['films'], 
         status_code=status.HTTP_200_OK,
         summary="All films")
def get_films(): #devuelve el listado de las peliculas
    """
    Obtener todas las peliculas
    """
    return JSONResponse(content=films)


@app.get(path="/films/read/{id}", 
        tags=["films"], 
        status_code=status.HTTP_200_OK,
        summary="Movie by id")
def get_movie_by_id(id: int):
    """
    Obtener película por id por parámetro de ruta
    """
    movie_by_id = [movie for movie in films if movie['id'] == id]
    if not movie_by_id:
        raise HTTPException(status_code=404, detail="Id movie not found")
    return JSONResponse(content=movie_by_id) 


@app.get('/films/read/', 
        tags=['films'],
        status_code=status.HTTP_200_OK,
        summary="Movie by category our year")
def get_movie_by_category_our_year(category: str=None, year: int=None):
    """
    Obtener película/as por una categoría o año por Query Parameters
    """
    if category is None and year is None:
        raise HTTPException(status_code=404, detail="Coloque algo, no sea pendejo")
        
    elif year is None:
        movie_categorie = [movie for movie in films if movie['category'] == category]
        if not movie_categorie:
            raise HTTPException(status_code=404, detail="Category of movie not found")
        return JSONResponse(content=movie_categorie)
    
    elif category is None:
        movie_year = [movie for movie in films if movie['year'] == str(year)]
        if not movie_year:
            raise HTTPException(status_code=404, detail="Year of movie not found")
        return JSONResponse(content=movie_year)
    
    else:
        movie_categorie_year = [movie for movie in films if (movie['category'] == category and movie['year'] == str(year))]
        if not movie_categorie_year:
            raise HTTPException(status_code=404, detail="Category our year of movie not found")
        return JSONResponse(content=movie_categorie_year)
    


        
movies_parameter = {
"title": "str",
"overview": "str",
"year": 2000,
"rating": 1.1,
"category": "str",
}


# @app.post('/movies', tags=['movies'])
# defcreate_movie(movie: Movie):
#     movie_list.append(movie.dict())
#     return movie

@app.post('/films/create/', 
          tags=['films'], 
          status_code=status.HTTP_200_OK,
          summary="Add Movie to films")
async def create_movie(movie_to_create: dict = movies_parameter):
    """
    Agregar una película por parámetros en el body, ID se coloca de manera automatica segun orden que sigue en nuestros "films"
    """
    if films:
        id = films[-1]['id'] + 1
    else:
        id = 1
    
    films.append(
        {
        'id': id,
        "title": movie_to_create["title"],
        "overview": movie_to_create["overview"],
        "year": movie_to_create["year"],
        "rating": movie_to_create["rating"],
        "category": movie_to_create["category"],
        }
    )
    return JSONResponse(content=films[-1])
             


@app.put(
    "/update/{id}",
    tags=['films'],
    status_code=status.HTTP_200_OK,
    summary="Update movie")
async def update_movie(id: int, movie_to_update: dict = movies_parameter):
    """
    Actualizar una película por parámetros en el body buscando por el parámetro de ID
    """
    movie_by_id = [movie for movie in films if movie['id'] == id]
    if not movie_by_id:
        raise HTTPException(status_code=404, detail="Movie not found! t(-_-t)")
    else:
        print("DEBUGGER")

        films[id - 1].update({
            "id": id,
            "title": movie_to_update["title"],
            "overview": movie_to_update["overview"],
            "year": movie_to_update["year"],
            "rating": movie_to_update["rating"],
            "category": movie_to_update["category"],
        })

    return JSONResponse(content=films[id - 1])


@app.delete(
    "/delete/{id}",
    tags=['films'],
    status_code=status.HTTP_200_OK,
    summary="Delete movie")
async def delete_movie(id: int):
    """
    Eliminar una película por el parámetro de ID
    """
    movie_by_id = [movie for movie in films if movie['id'] == id]
    if not movie_by_id:
        raise HTTPException(status_code=404, detail="Movie not found! t(-_-t)")
    else:
        print("DEBUGGER")

        films.pop(id - 1)

    return JSONResponse(content=films)
        
        
        
        
        
        
