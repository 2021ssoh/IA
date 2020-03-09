import os
from app import app
from flask import render_template, request, redirect, session, url_for
from bson.objectid import ObjectId

events = [
        {},

    ]


from flask_pymongo import PyMongo

app.secret_key = b'_5#y2L "F4Q8z\n\xec]/'

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

@app.route('/input_event')
def input_event():
    return render_template('newproduct.html')

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


@app.route('/delete')
def delete():
    collection = mongo.db.events
    collection.delete_many({})
    return redirect('/index')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/signup',  methods = ["get", "post"])
def signup():
    # sending data by using post method
    if request.method == 'POST':
        # connect to mongo info collection
        collection = mongo.db.information
        # look for an existing account
        existing_user = collection.find_one({'name' : request.form['name']})

        # if there is no account:
        if existing_user is None:
            # then indert all this info into Mongo when they sign up
            collection.insert({'name': request.form['name'], 'age': request.form['age'], 'problem': request.form['problem'], 'hw': request.form['hw'], 'breed': request.form['breed'], 'email': request.form['email'], 'password': request.form['password']})
            session['name'] = request.form['name']
            return render_template('index.html')
        return ("That username already exists, try logging in!")

    return render_template ('signup.html')

@app.route('/login', methods = ["get","post"])
def login():
    collection = mongo.db.information
    # query mongo to see if such a user exists
    login_user = collection.find_one({'name' : request.form['name']})

        # if user exists,
    if login_user:
            # check to see if what the user submitted matched with what previously stored on Mongo
        if request.form['password'] == login_user['password']:
            session['name'] = request.form['name']
            return render_template('index.html')
    return ("Invalid username/password combination")

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

# a route to show whatever was stored previously under someone's account history
@app.route('/myshoppingcart')
def name():
    collection = mongo.db.information
    name = session['name']
    events = collection.find({"name": name})
    return render_template('shoppingcart.html', events = events)



@app.route('/filter', methods = ["get", "post"])
def filter():
    food_info = dict(request.form)
    _id = food_info["product"]
    print(food_info)
    collection = mongo.db.events
    # event_name = food_info["event_name"]
    # event_price = food_info["event_price"]
    # ingredients = food_info["ingredients"]
    # calorie = food_info["calorie"]
    product_info = list(collection.find({"_id": ObjectId(_id)}))
    print (product_info)
    return render_template('info.html', events = product_info)

@app.route('/shoppingcart', methods = ["get", "post"])
def shoppingcart():
    if request.method == "POST":
        food_info = dict(request.form)
        print("the info from the form is", food_info)
        _id = food_info["product"]
        # connect to cart collection
        cart = mongo.db.carts
        # insert username and product ID to cart collection
        try:
            cart.insert({'name': session['name'], "_id": _id})
        except:
            print("That's already in the shopping cart")
        collection = mongo.db.events
        product_info = list(collection.find({"_id": ObjectId(_id)}))
        # collection.insert({"id": ObjectId(_id)})
        # events = list(collection.find({}))
        return render_template('shoppingcart.html', events = product_info)
    else:
        # query
        cart = mongo.db.carts
        shopping_cart = cart.find({"name": session['name']})
        results = []
        events = mongo.db.events
        for item in shopping_cart:
            print(item)
            results.append(list(events.find({"_id": ObjectId(item["_id"])})))
            print(results)
        return render_template('shoppingcart.html', events = results)

@app.route('/buy')
def buy():
    username = cart.find({"name": session['name']})
    print(username)
