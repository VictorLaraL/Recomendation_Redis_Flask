from flask import Flask, request, render_template
import redis

dbMovies = redis.Redis(charset="utf-8", decode_responses=True, db = 0)
dbGenres = redis.Redis(charset="utf-8", decode_responses=True, db = 1)

app = Flask(__name__)

@app.route('/home')
def index():
    listMov = [] #Lista donde almacenamos todas las peliculas, las almacenamos como str
    
    search = request.args.get('search', "no hay coincideincias") #Almacenamos los datos ingresados en el input

    searchMov = ' '
    for x in range (1, 9742):
        for movie in dbMovies.smembers(x):
            listMov.append(movie) #Agregamos cada pelicula a la lista
            if (search == movie):
                searchMov = 'si tenemos la pelicula: {}'.format(movie)
        
    return render_template('home.html', list = listMov, result = searchMov)

@app.route('/list')
def listMov():
    return render_template('list.html')

if __name__ == '__main__':
    app.run(debug=True)