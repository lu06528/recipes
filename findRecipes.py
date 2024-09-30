from database import *
from recipe import *
from flask import Flask, render_template, request
from werkzeug.local import Local
#from jinja2 import Environment, PackageLoader, select_autoescape
#env = Environment(
#    loader=PackageLoader("findRecipes"),
#    autoescape=select_autoescape()
#)
#template = env.get_template("template.html")

app = Flask(__name__)
local = Local()

def get_db():
    if not hasattr(local, 'recipes_db'):
        local.recipes_db = sqlite3.connect('recipes.db')
    return local.recipes_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(local, 'recipes_db'):
        local.recipes_db.close()

@app.route('/')
def index():
    '''Zeigt die Startseite an (Bisher leer).'''
    return render_template('/index.html')

@app.route('/filter')
def unfiltered_recipes():
    '''Zeigt die Page mit allen Rezepten an.'''
    db = get_db()
    mycursor = db.cursor()
    rows = fetchRecipes(mycursor, 0)
    return render_template('/template.html', rows=rows)

@app.route('/filter', methods=['POST'])
def filtered_recipes():
    '''Zeigt die Page mit den gefilterten Rezepten an.'''
    # Verbindung zur Datenbank herstellen
    db = get_db()
    mycursor = db.cursor()
    # db_filter sollte die Werte 0, 1 oder 2 haben
    try:
        db_filter = request.form['filter']
    except:
        db_filter = 0
    rows = fetchRecipes(mycursor, int(db_filter))
    # HTML-Vorlage mit Jinja2 rendern  und Daten einfügen
    return render_template('/template.html', rows=rows)

@app.route('/updateRecipe', methods=['POST'])
def update_recipe():
    '''Für das übergebene Rezept wird das 'Zuletzt' Datum in der
    Datenbank aktualisiert.'''
    # Verbindung zur Datenbank herstellen
    db = get_db()
    mycursor = db.cursor()
    # Speichere Name des zu aktualisierenden Rezeptes
    recipeName = request.form['updateButton']
    # Aktualisiere Datum
    updateRecipeToday(db, mycursor, recipeName)
    # Lade Rezepte Page neu
    rows = fetchRecipes(mycursor, 0)
    return render_template('/template.html', rows=rows)

@app.route('/addRecipe')
def add_recipe_page():
    '''Zeige die Page 'addRecipe' an.'''
    return render_template('/addRecipe.html')

@app.route('/recipeAdded', methods=['POST'])
def add_recipe():
    '''Die Daten, die durch das Form übertragen werden, werden zur Datenbank hinzugefügt.'''
    # Verbindung zur Datenbank herstellen
    db = get_db()
    mycursor = db.cursor()
    # Speichere Name des zu aktualisierenden Rezeptes
    recipeName = request.form['recipeName']
    veggie = int(request.form['veggie'])
    dadApproved = int(request.form['dadApproved'])
    # Füge Rezept zur Datenbank hinzu
    addRecipe(db, mycursor, recipeName, veggie, dadApproved)
    # Lade Rezepte Page neu
    rows = fetchRecipes(mycursor, 0)
    return render_template('/template.html', rows=rows)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)