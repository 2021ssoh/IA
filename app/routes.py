import os
from app import app
from flask import render_template, request, redirect, session, url_for

events = [
        {},

    ]


from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'IA'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:SUdKE0PRiU1r4Ihv@cluster0-f3oyp.mongodb.net/IA?retryWrites=true&w=majority'

mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    # connect to the MONGO_DB
    collection = mongo.db.events
    # find all events in database using a query
    # {} will return everything in the database
    events = list(collection.find({}))
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""

@app.route('/homepage')
def homepage():
    return render_template('index.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/secret', methods = ["get", "post"])
def secret():
    food_info = dict(request.form)
    print(food_info)
    try:
        event_name = food_info["name"]
    except:
        print("the event name is ", event_name)
    try:
        event_price = food_info["price"]
    except:
        print("the price is ", event_price)
    try:
        ingredients = food_info["ingredients"]
    except:
        print(" ingredients include ", ingredients)
    try:
        calorie = food_info["calorie"]
    except:
        print("no of calories is", calorie)
        # connects to db
    collection = mongo.db.events
    # inserts info into db
    collection.insert({"event_name": event_name, "event_price": event_price, "ingredients": ingredients, "calorie": calorie})

    events = list(collection.find({}))
    return render_template('secret.html', events = events)

@app.route('/input_event')
def input_event():
    return render_template('newproduct.html')

@app.route('/delete')
def delete():
    collection = mongo.db.events
    collection.delete_many({})
    return redirect('/index')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/login')
def login():
    return render_template('signin.html')

@app.route('/signup',  methods = ["get", "post"])
def signup():
    client_info = dict(request.form)
    print(client_info)
    name = client_info["name"]
    age = client_info["age"]
    problem = client_info["problem"]
    hw = client_info["hw"]
    breed = client_info["breed"]
    email = client_info["email"]
    collection = mongo.db.information
    collection.insert({"name": name, "age": age, "problem": problem, "hw": hw, "breed": breed, "email": email})
    events = list(collection.find({}))
    return render_template('index.html', events = events)

@app.route('/filter', methods = ["get", "post"])
def filter():
    food_info = dict(request.form)
    collection = mongo.db.events
    food_name = food_info["name"]
    price = food_info["price"]
    ingredients = food_info["ingredients"]
    calorie = food_info["calorie"]
    product_info = list(collection.find({"name": food_name, "price": price, "ingredients": ingredients, "calorie": calorie}))
    print (product_info)
    
