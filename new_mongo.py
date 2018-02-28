import pymongo
from bson.objectid import ObjectId
import os
from flask import Flask, redirect, render_template, request, flash, jsonify, url_for
# from flask_cors import CORS, cross_origin
# MONGO_URI=mongodb://root:1234@ds263137.mlab.com:63137/cookbookdb python3 new_mongo.py

HOST = os.getenv('IP', '0.0.0.0')
PORT = int(os.getenv('PORT', '8080'))

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'some_secret'
data = []

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "cookbookdb" #database name
COLLECTION_NAME = "cookMDB" #collection name

def mongo_connect(url):
  try:
    conn = pymongo.MongoClient(url)
    return conn
  except pymongo.errors.ConnectionFailure as e:
    print("could not connect to MongoDB: %s") % e

conn = mongo_connect(MONGODB_URI)
coll = conn[DBS_NAME][COLLECTION_NAME]

def get_recipe_by_id(recipe_id):
    recipe = coll.find_one({ '_id': ObjectId(recipe_id) })
    if recipe is not None:
        recipe['str_id'] = str(recipe['_id'])
    return recipe

def update_recipe(recipe_id, recipe_updated_values):
    coll.update_one({'_id': ObjectId(recipe_id)},  {"$set": recipe_updated_values})

# Looking up for a recipe - added lower so the capitalization does not matter when looking up something (recycling function)
def get_recipe(recipe_title):
    doc = None
    try:
        doc = coll.find_one({'recipe': recipe_title.lower()})
    except:
        print("Error accessing the database")

    return doc

# ADD RECIPES
def add_recipe(title, ingredients, steps, chef_notes):
  new_recipe = {'title': title, 'ingredients': ingredients, 'steps': steps, 'notes': chef_notes}

  try:
      coll.insert(new_recipe)
      print("")
      print("Document inserted")
  except:
      print("Error accessing the database")


# DISPLAY RECIPE - JONATHAN
def display_recipe(title, ingredients, steps, chef_notes):
    edit_recipe = {'title': title, 'ingredients': ingredients, 'steps': steps, 'notes': chef_notes}

try:
    coll.edit(new_recipe)
except:
    print("Error editing the database")
# DISPLAY RECIPE - JONATHAN

# FIND RECIPES
def get_recipes():
    # List comprehension
    recipes = [recipe for recipe in coll.find()]
    for i in range(len(recipes)):
        recipe = recipes[i]
        recipe['str_id'] = str(recipe['_id'])
        recipes[i] = recipe
    # print(recipes)
    return recipes

def delete_recipe(recipe_id):
    # print(recipe_id)
    result = coll.delete_one({ '_id': ObjectId(recipe_id) })
    return result.deleted_count == 1


# EDIT RECIPES START - Jonathan
def edit_recipes():
    # List comprehension
    recipes = [recipe for recipe in coll.update_one()]
    return recipes
try:
    coll.update_one(doc, {'$set': update_doc})
    print("")
    print("Recipe Updated")
except:
    print("Error accessing the recipes")
# EDIT RECIPES ENDS - Jonathan

# routing
@app.route('/')
def index():
    recipes=get_recipes()
    return render_template(
        'recipes.html',
        page_name='Home',
        recipes=recipes)

# ADD RECIPE ROUTING
@app.route('/add', methods=['POST'])
def add():
    add_recipe(
        title=request.form['title'],
        ingredients=request.form['ingredients'],
        steps=request.form['steps'],
        chef_notes=request.form['chef_notes']
    )
    flash('Recipe added')
    return redirect(url_for('index'))

@app.route('/delete', methods=['GET'])
# @cross_origin(origin='*')
def delete():
    recipe_id = request.args.get('recipeId')
    deleted = delete_recipe(recipe_id)
    # return jsonify({ 'deleted': deleted })
    if deleted:
        flash('Recipe deleted')
    else:
        flash('Failed to find recipe')
    print(deleted)
    return redirect(url_for('index'))

@app.route('/edit', methods=['GET'])
def edit():
    recipe_id = request.args.get('recipeId')
    recipe = get_recipe_by_id(recipe_id)
    return render_template('edit.html', recipe=recipe)
    # recipes=get_recipes()
    # return render_template('edit.html', recipes=recipes)

@app.route('/update', methods=['POST'])
def update():
    recipe_id = request.args.get('recipeId')
    recipe_updated_values = request.form
    update_recipe(recipe_id, recipe_updated_values)
    return redirect(url_for('index'))


# HARDCODED OWN RECIPES - non database
    # porktacos NAVIGATION
@app.route('/porktacos', methods=['GET', 'POST'])
def porktacos():
    if request.method == 'POST':
        return redirect(url_for('recipes'))
    return render_template('porktacos.html')

    # cheesy NAVIGATION
@app.route('/cheesy', methods=['GET', 'POST'])
def cheesy():
    if request.method == 'POST':
        return redirect(url_for('recipes'))
    return render_template('cheesy.html')

    # buffalo NAVIGATION
@app.route('/buffalo', methods=['GET', 'POST'])
def buffalo():
    if request.method == 'POST':
        return redirect(url_for('recipes'))
    return render_template('buffalo.html')

    # shrimp NAVIGATION
@app.route('/shrimp', methods=['GET', 'POST'])
def shrimp():
    if request.method == 'POST':
        return redirect(url_for('recipes'))
    return render_template('shrimp.html')

    # turkey NAVIGATION
@app.route('/turkey', methods=['GET', 'POST'])
def turkey():
    if request.method == 'POST':
        return redirect(url_for('recipes'))
    return render_template('turkey.html')

    # tuna NAVIGATION
@app.route('/tuna', methods=['GET', 'POST'])
def tuna():
    if request.method == 'POST':
        return redirect(url_for('recipes'))
    return render_template('tuna.html')

    # back to recipes.html:
@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        return redirect(url_for('porktacos', 'cheesy', 'shirmp', 'tuna', 'buffalo', 'turkey'))
    return render_template('recipes.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'), port=int(os.environ.get('PORT', 0)), debug=True)
