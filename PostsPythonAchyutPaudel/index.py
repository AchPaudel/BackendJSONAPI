from unicodedata import numeric
from webbrowser import get
from flask import Flask, json, request

app = Flask(__name__)

f = open('data.json', 'r')
oldData = json.load(f)
recipesList = oldData['recipes']


@app.route('/recipes', methods=['GET'])
def getAllRecipes():
    namesList = []
    for i in recipesList:
        namesList.append(i['name'])
    toDict = dict()
    toDict['recipeNames'] = namesList
    return json.dumps(toDict, indent=4)




@app.route('/recipes/details/<recipe>', methods=['GET'])
def getRecipe(recipe):
    getName = '%s' % recipe
    numDict = dict()
    for i in recipesList:
        if(i['name'] == getName):
            #Number of steps
            numCount = len(i['instructions'])
            numDict["numSteps"] = numCount

            #Get ingredients
            jsonnewDict = dict()
            jsonnewDict["details"] = dict()
            jsonnewDict["details"]['ingredients'] = i['ingredients']
            jsonnewDict["details"].update(numDict)
            return json.dumps(jsonnewDict, indent=4)


@app.route('/recipes', methods=['POST'])
def addRecipe():
    data = json.loads(request.data)
    #Check if recipe already exists
    for i in recipesList:
        if(i['name'] == data['name']):
            return json.dumps({"error": "Recipe already exists"}, indent=4)
    
    #Get new recipe data
    newRecipe = dict()
    newRecipe['name'] = data['name']
    newRecipe['ingredients'] = data['ingredients']
    newRecipe['instructions'] = data['instructions']
    #Add new recipe to list
    recipesList.append(newRecipe)
    oldData['recipes'] = recipesList
    return json.dumps(recipesList, indent=4)



@app.route('/recipes', methods=["PUT"])
def updateRecipe():
    data = json.loads(request.data)
    #Add recipe to list
    newRecipe = dict()
    newRecipe['name'] = data['name']
    newRecipe['ingredients'] = data['ingredients']
    newRecipe['instructions'] = data['instructions']

    for i in recipesList:
        if(i['name'] == newRecipe['name']):
            i['ingredients'] = newRecipe['ingredients']
            i['instructions'] = newRecipe['instructions']
            oldData['recipes'] = recipesList
            return json.dumps(recipesList, indent=4)

    return json.dumps({"error":"Recipe does not exist"}, indent=4)






