import sqlite3

db = sqlite3.connect("recipes.db")

mycursor = db.cursor()

def initializeDB():
    mycursor.execute("CREATE TABLE IF NOT EXISTS recipes(Name TINYTEXT, Vegetarisch BIT, Papa BIT, PRIMARY KEY (Name))")
    db.commit()

def clearDB():
    mycursor.execute("DROP TABLE recipes")
    db.commit()
    initializeDB()

def addRecipe(name: str, veggie: int, dad: int) -> None:
    mycursor.execute(f"INSERT OR IGNORE INTO recipes(Name, Vegetarisch, Papa) VALUES('{name}', {veggie}, {dad})")

    db.commit()

def printRecipes(filter):
    query = "SELECT Name FROM recipes"
    if filter != 0:
        type = (
            "Vegetarisch" if filter == 1 else
            "Papa" if filter == 2 else
            0
        )
        query += f" WHERE {type} = 1 ORDER BY Name"
        
    printQueryResults(query)

def printQueryResults(query):
    mycursor.execute(query)
    for result in mycursor:
        print(result[0])

initializeDB()