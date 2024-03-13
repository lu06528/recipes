
from database import *
from recipe import *

def copyRecipesToDB():
    file = open("./recipes.txt", "r")
    Lines = file.readlines()
    for(line) in Lines:
        lineValues = line.split('|')
        addRecipe(lineValues[0], int(lineValues[1]), int(lineValues[2]))

#clearDB()

copyRecipesToDB()

#Parameters: All 0 | Vegetarian 1 | Dad would eat it 2
printRecipes(1)