

from fastapi import FastAPI
from typing import Union

app = FastAPI()


##@app.get("/")
#async def root():
    #return {"message": "Hello World"}

@app.get("/get_max_duration")

async def get_max_duration(year:int=None, platform:str=None, duration_type:str=None):

    import pandas as pd
    
    # Cargar el archivo de películas en un dataframe de pandas
    df = pd.read_csv('./peliculasyseriesconscore.csv')
    
    # Aplicar los filtros opcionales al dataframe
    if year:
        df = df[df['release_year'] == year]
    if platform:
        df = df[df['platform'] == platform]
    if duration_type:
        df = df[df['duration_type'] == duration_type]
    max_duration = df['duration_int'].max()
    titulo = df.loc[df['duration_int'] == max_duration, 'title'].iloc[0]
    
    return titulo

@app.get("/get_score_count")

async def get_score_count(platform:str,scored:float,year:int):
    
    import pandas as pd
    
    # Cargar el dataframe de películas (supongamos que se llama "movies_df")
    movies_df = pd.read_csv("./peliculasyseriesconscore.csv")

    # Filtrar las películas que pertenecen a la plataforma y al año especificados
    filtered_df = movies_df[(movies_df["platform"] == platform) & (movies_df["release_year"] == year)]

    # Contar la cantidad de películas con puntaje mayor al valor especificado
    count = filtered_df[filtered_df["score_mean"] > scored].shape[0]

    return int(count)


@app.get('/get_count_platform')


async def get_count_platform(platform:str):
    
    import pandas as pd
    
    # Cargar el dataframe de películas (supongamos que se llama "movies_df")
    movies_df = pd.read_csv("./peliculasyseriesconscore.csv")

    # Filtrar las películas que pertenecen a la plataforma especificada
    filtered_df = movies_df[movies_df["platform"] == platform]

    # Contar la cantidad de películas por plataforma
    count_by_platform = filtered_df["platform"].value_counts()

    return int(count_by_platform[platform])




@app.get('/get_actor/{platform}/{year}')

async def get_actor3(platform: str, year: int):
    """
    Devuelve el actor que más se repite según plataforma y año.
    :param platform: plataforma del contenido
    :param year: año de lanzamiento del contenido
    :return: actor que más se repite
    """
    import pandas as pd
    
    df = pd.read_csv('peliculasyseriesconscore.csv')
    
    # Filtrar el DataFrame según plataforma y año
    df_filtered = df[(df['platform'] == platform) & (df['release_year'] == year)]
    # Verificar si el DataFrame filtrado no está vacío
    if len(df_filtered) == 0:
        return f"No se encontraron resultados para la plataforma {platform} en el año {year}"
    # Crear un diccionario para contar la cantidad de veces que aparece cada actor
    actor_count = {}
    for row in df_filtered.iterrows():
        cast = row[1]['cast']
        if isinstance(cast, str):
            actors = cast.split(',')
            for actor in actors:
                if actor in actor_count:
                    actor_count[actor] += 1
                else:
                    actor_count[actor] = 1
    # Verificar si el diccionario de conteo está vacío
    if len(actor_count) == 0:
        return f"No se encontraron actores para la plataforma {platform} en el año {year}"
    # Obtener el actor que más se repite
    max_actor = max(actor_count, key=actor_count.get)
    return max_actor