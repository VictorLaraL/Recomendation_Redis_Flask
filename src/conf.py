import pandas as pd
import redis

mov = pd.read_csv('movies.csv') 
dbMovies = redis.Redis(db = 0) 
dbGenres = redis.Redis(db = 1) 

dicGen = {'Action':[], 'Adventure':[], 'Animation':[], 'Comedy':[], 'Crime':[], 'Documentary':[],
            'Drama':[], 'Fantasy':[], 'Film-Noir':[], 'Horror':[], 'Musical':[], 'Mystery':[], 'Romance':[],
             'Sci-Fi':[], 'Thriller':[], 'War':[], 'Western':[]} 

genres = dicGen.keys()

for index, row in mov.iterrows():
    
    listGen = row['genres'].split('|')
    for genre in listGen:
        dbGenres.sadd(row['title'], genre)
    
    dbMovies.sadd(row['movieId'], row['title'])
    
print(dbGenres.smembers('Toy Story (1995)')) 
print('done')