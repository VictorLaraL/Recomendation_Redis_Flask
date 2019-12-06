from flask import Flask, request, render_template
import redis

#Variables donde almacenamos los clientes de la DB que ingresaran y extraeran informacion
dbMovies = redis.Redis(charset="utf-8", decode_responses=True, db = 0)
dbGenres = redis.Redis(charset="utf-8", decode_responses=True, db = 1)
dbGenresM = redis.Redis(charset="utf-8", decode_responses=True, db = 2)
dbUsers = redis.Redis(charset="utf-8", decode_responses=True, db = 3)


app = Flask(__name__)

@app.route('/home/<string:addMovie>')
@app.route('/home') #Pagina de inicio donde mostramos el catalogo completo
def index(addMovie = None):
    listMov = [] #Lista donde almacenamos todas las peliculas, las almacenamos como str
    
    search = request.args.get('search', "no hay coincideincias") #Almacenamos los datos ingresados en el input

    searchMov = ' '
    for x in range (1, 9742):
        for movie in dbMovies.smembers(x):
            listMov.append(movie) #Agregamos cada pelicula a la lista
            if (search == movie): #Validacion de coincideincia de la busqueda
                searchMov = movie

    if(addMovie != None and addMovie != ' '):
        dbUsers.sadd('u1', addMovie)

    return render_template('home.html', list = listMov, result = searchMov)


@app.route('/list/<string:delMov>')
@app.route('/list') #Lista de peliculas del usuario
def listMov(delMov = None):
    listMov = [] #Lista de peliculas del usuario

    if(delMov != None):
        dbUsers.srem('u1', delMov)

    for movie in dbUsers.smembers('u1'):
       listMov.append(movie) 
        
    return render_template('list.html', list = listMov)

@app.route('/listRecInt/<string:addMovie>')
@app.route('/listRecInt')
def ListRecomInter(addMovie = None):
    listMov = [] #Lista de peliculas del usuario
    listRec = [] #Lista de peliculas recomendadas
    
    for movie in dbUsers.smembers('u1'): #Almacenamos en listMov las peliculas asociadas al usuario
       listMov.append(movie) 

    if(len(listMov) != 0):
        interGenres = dbGenres.sinter(listMov) #Almacenamos los generos que coincidan en la variable
        print(interGenres)
        for genre in interGenres:
            for idMovie in dbGenresM.smembers(genre):
                for movie in dbMovies.smembers(idMovie):
                    listRec.append(movie)

    if(addMovie != None):
        dbUsers.sadd('u1', addMovie)

    return render_template('listRecInt.html', listMov = listRec)

@app.route('/listRecUn/<string:addMovie>')
@app.route('/listRecUn')
def ListRecomUnion(addMovie = None):
    listMov = [] #Lista de peliculas del usuario
    listRec = [] #Lista de peliculas recomendadas
    
    for movie in dbUsers.smembers('u1'): #Almacenamos en listMov las peliculas asociadas al usuario
       listMov.append(movie) 

    if(len(listMov) != 0):
        interGenres = dbGenres.sunion(listMov) #Almacenamos los generos que coincidan en la variable
        print(interGenres)
        for genre in interGenres:
            for idMovie in dbGenresM.smembers(genre):
                for movie in dbMovies.smembers(idMovie):
                    listRec.append(movie)
    
    if(addMovie != None):
        dbUsers.sadd('u1', addMovie)

    return render_template('listRecUn.html', listMov = listRec)

if __name__ == '__main__':
    app.run(debug=True)