from flask import Flask, render_template, request, url_for, flash, redirect 
import pymongo
from pymongo import MongoClient
import certifi
import json
from bson.objectid import ObjectId

cluster = MongoClient('mongodb+srv://dlyonskeefe:BoN8xaXS9TcIUsuY@cs290.8hbfp.mongodb.net/CS290?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = cluster['CS290']
collection = db['movies']

app = Flask(__name__)
app.config['SECRET_KEY'] = '31dd0d2e46ad1a9e9e8c6fb34ad59863690737de29405bbf'

# collection.insert_one({'title': "Waiting for Guffman", 'year': 1996, 'director': 'Christopher Guest', 'rating': 10, 'review': 'Truly the best movie ever'})

# homepage route, gets all films in the DB and displays them along with navigation and short intro blurb
@app.route('/', methods=['GET'])
def get_home_page():
    all_movies = collection.find()
    return render_template('index.html', movies=all_movies)

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

@app.post('/<id>/delete')
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect('/')

@app.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    movie = collection.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        director = request.form['director']
        rating = request.form['rating']
        review = request.form['review']
        collection.find_one_and_update({"_id": ObjectId(id)}, {"title": title, "year": year, "director": director, "rating": rating, "review": review})
        return redirect('/')
    return render_template('edit_movie.html', movie=movie)

