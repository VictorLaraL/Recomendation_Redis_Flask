from flask import Flask, request, render_template
import redis

dbMovies = redis.Redis(db = 0)
dbGenres = redis.Redis(db = 1)
app = Flask(__name__)

@app.route('/home')
def index():
    search = request.args.get('search', "no hay coincideincias")
    busqueda = str(dbGenres.smembers(search))
    return render_template('home.html', busqueda = busqueda)

@app.route('/list')
def listMov():
    return render_template('list.html')

if __name__ == '__main__':
    app.run(debug=True)