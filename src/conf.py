import pandas as pd
import redis

mov = pd.read_csv('movies.csv') 
dbMovies = redis.Redis(db = 0) 
dbGenres = redis.Redis(db = 1)
dbGenresM = redis.Redis(db = 2)

for index, row in mov.iterrows():
    listGen = row['genres'].split('|')
    for genre in listGen:
        dbGenres.sadd(row['title'], genre)
        dbGenresM.sadd(genre, row['movieId'])
    
    dbMovies.sadd(row['movieId'], row['title'])
    
print('done')