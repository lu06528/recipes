import sqlite3
import datetime

myDB = sqlite3.connect("recipes.db")

mycursor = myDB.cursor()

# TODO: Database needs a 'Last time cooked' column
def initializeDB():
    mycursor.execute("CREATE TABLE IF NOT EXISTS recipes(Name TINYTEXT, Vegetarisch BIT, Papa BIT, Zuletzt DATETIME, PRIMARY KEY (Name));")
    myDB.commit()

def clearDB():
    mycursor.execute("DROP TABLE recipes;")
    myDB.commit()
    initializeDB()

def addRecipe(db: sqlite3.Connection, cursor: sqlite3.Cursor, name: str, veggie: int, dad: int) -> None:
    today = datetime.date.today()
    cursor.execute(f"INSERT OR IGNORE INTO recipes(Name, Vegetarisch, Papa, Zuletzt) VALUES('{name}', {veggie}, {dad}, '{today.strftime('%d.%m.%Y')}');")

    db.commit()

def updateRecipeDate(db: sqlite3.Connection, cursor: sqlite3.Cursor, name: str, date: datetime.date):
    cursor.execute(f"UPDATE recipes SET Zuletzt = '{date}' WHERE Name = '{name}';")

    db.commit()

def updateRecipeToday(db: sqlite3.Connection, cursor: sqlite3.Cursor, name: str):
    today = datetime.date.today()
    cursor.execute(f"UPDATE recipes SET Zuletzt = '{today}' WHERE Name = '{name}';")

    db.commit()

def fetchRecipes(cursor: sqlite3.Cursor, filter):
    query = "SELECT Name, Zuletzt FROM recipes"
    if filter != 0:
        type = (
            "Vegetarisch" if filter == 1 else
            "Papa" if filter == 2 else
            0
        )
        query += f" WHERE {type} = 1"
    query += " ORDER BY Zuletzt ASC, Name;"

    cursor.execute(query)
    result = []
    for(Rezept) in cursor:
        recipeDate = Rezept[1].split('-')
        rezeptTupel = (Rezept[0], recipeDate[2] + "." + recipeDate[1] + "." + recipeDate[0])
        result.append(rezeptTupel)
    return result
   
#    printQueryResults(query)
#
#def printQueryResults(query):
#    mycursor.execute(query)
#    for result in mycursor:
#        print(result[0])

# def fetchQueryResults(query):

def copyRecipesToDB():
    # Lese Zeilen aus Text-Datei für Rezepte
    file = open("./recipes.txt", "r")
    Lines = file.readlines()
    for(line) in Lines:
        lineValues = line.split('|')
        addRecipe(mycursor, lineValues[0], int(lineValues[1]), int(lineValues[2]))

def printAll():
    print("Inhalt der Datenbank:")
    query = "SELECT Name, Zuletzt FROM recipes ORDER BY Zuletzt ASC, Name;"
    mycursor.execute(query)
    for result in mycursor:
        print(result[0] + " | " + result[1])

#clearDB()
#copyRecipesToDB()
#printAll()
