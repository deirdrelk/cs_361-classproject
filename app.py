from urllib.parse import quote
from flask import Flask, render_template, request, redirect
import requests
from random import randint
from pymongo import MongoClient
import certifi
from bson.objectid import ObjectId
from dotenv import dotenv_values

mongo_config = dotenv_values('.env')
mongo_url = mongo_config.get('MONGO_SERVER_URI')

cluster = MongoClient(mongo_url, tlsCAFile=certifi.where())
db = cluster['CS290']
collection = db['movies']

app = Flask(__name__)

# homepage route, gets all films in the DB and displays them along with navigation and short intro blurb
@app.route('/', methods = ['GET'])
def get_home_page():
    all_movies = collection.find()
    return render_template('index.html', movies = all_movies)

# route to add new movie form
@app.route('/add', methods = ['GET','POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        director = request.form['director']
        rating = request.form['rating']
        date_watched = request.form['date_watched']
        review = request.form['review']
        collection.insert_one({"title": title, "year": year, "director": director, "rating": rating, "date_watched": date_watched, "review": review})
        return redirect('/')
    return render_template("add_movie.html")

# route to about page
@app.route('/about', methods = ['GET'])
def get_about_page():
    return render_template('about.html')

# route to delete - called in index.html
@app.route('/<id>/delete', methods = ['DELETE'])
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return get_home_page()

# update a film
@app.route('/<id>/edit', methods = ['GET', 'POST'])
def edit(id):
    movie = collection.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        director = request.form['director']
        rating = request.form['rating']
        date_watched = request.form['date_watched']
        review = request.form['review']
        collection.find_one_and_update({"_id": ObjectId(id)}, { "$set": {"title": title, "year": year, "director": director, "rating": rating, "date_watched": date_watched, "review": review}})
        return redirect('/')
    return render_template('edit_movie.html', movie = movie)

# generate a random movie by calling microservice
@app.route('/generate', methods = ['GET'])
def generate_random_movie():
    if request.method == 'GET':
        random_titles_array = ['Jurassic Park', 'Robocop', 'Tootsie', 'North by Northwest', 'Volver', 'Young Frankenstein', 'Babe', 'Scream', 'Rear Window']
        movie_pick = quote(random_titles_array[randint(0,8)])
        movie_api_url = f'https://us-central1-atlantean-bebop-349722.cloudfunctions.net/info?title={movie_pick}'
        headers = {'Accept': 'application/json'}
        response = requests.get(movie_api_url, headers = headers)
        data = response.json()
        if data.get('status') == 'Success':
            return render_template('generatemovie.html', movie = data)

# filter films by year watched
@app.route('/<sort>/archives', methods = ['GET'])
def show_sort(sort):
    if sort == 'date_watched':
        movies_by_year = collection.find({}).sort(sort, 1)
        return render_template('movies_archive.html', movie = movies_by_year)
    if sort == 'year':
        movies_by_release = collection.find({}).sort(sort, 1)
        return render_template('movies_release.html', movie = movies_by_release)
    if sort == 'rating':
        movies_by_rating = collection.find({}).sort(sort, 1)
        return render_template('movies_rating.html', movie = movies_by_rating)

if __name__ == "__main__":

    #Start the app on port 5000, it will be different once hosted
    app.run(port=5000, debug=True)