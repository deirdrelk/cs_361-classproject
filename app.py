from urllib.parse import quote
from flask import Flask, render_template, request, redirect
import requests
from random import randint
from pymongo import MongoClient
import certifi
from bson.objectid import ObjectId

cluster = MongoClient('mongodb+srv://dlyonskeefe:XXXXXXXY@cs290.8hbfp.mongodb.net/CS290?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = cluster['CS290']
collection = db['movies']

app = Flask(__name__)
app.config['SECRET_KEY'] = '31dd0d2e46ad1a9e9e8c6fb34ad59863690737de29405bbf'

# homepage route, gets all films in the DB and displays them along with navigation and short intro blurb
@app.route('/', methods=['GET'])
def get_home_page():
    all_movies = collection.find()
    return render_template('index.html', movies = all_movies)

# route to add new movie form
@app.route('/add', methods=['GET','POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        director = request.form['director']
        rating = request.form['rating']
        review = request.form['review']
        collection.insert_one({"title": title, "year": year, "director": director, "rating": rating, "review": review})
        return redirect('/')
    return render_template("add_movie.html")

@app.route('/about', methods=['GET'])
def get_about_page():
    return render_template('about.html')

@app.route('/<id>/delete', methods=['DELETE', 'GET'])
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect('/success')

@app.route('/success', methods = ['GET'])
def get_success_page():
    return render_template('success.html')

@app.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    movie = collection.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        director = request.form['director']
        rating = request.form['rating']
        review = request.form['review']
        collection.find_one_and_update({"_id": ObjectId(id)}, { "$set": {"title": title, "year": year, "director": director, "rating": rating, "review": review}})
        return redirect('/')
    return render_template('edit_movie.html', movie = movie)

@app.route('/generate', methods=['GET', 'POST'])
def generate_random_movie():
    random_titles_array = ['Jurassic Park', 'Robocop', 'Tootsie', 'North by Northwest', 'Volver', 'Young Frankenstein', 'Babe', 'Scream', 'Rear Window']
    movie_pick = quote(random_titles_array[randint(0,8)])
    movie_api_url = f'https://us-central1-atlantean-bebop-349722.cloudfunctions.net/info?title={movie_pick}'
    response = requests.get(movie_api_url)
    data = response.json()
    if data.get('status') == 'Success':
        return render_template('generatemovie.html', movie = data)

if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=5000, debug=True)