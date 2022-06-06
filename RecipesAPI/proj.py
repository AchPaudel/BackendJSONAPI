from os import remove
from unittest.util import sorted_list_difference
from parso import parse
import requests
import json
from unicodedata import numeric
from webbrowser import get
from flask import Flask, json, request, url_for
from urllib import parse as urlparse

app = Flask(__name__)
app.debug = True

##TESTING Fetch
def getTagJSON(tagParam):
    response_API = requests.get("https://api.hatchways.io/assessment/blog/posts%s" % tagParam)
    data = json.loads(response_API.text)
    return data

def toYesQ(query):
    for i in range(len(query)):
        query[i] = '?' + query[i]
    return query

def getTagsDict(queriesNoQ):
    tagDict = dict()
    for i in queriesNoQ:
        i = i.split('=')
        a = i[0][1:]
        if(a == 'tags'):
            tagsList = i[1].split(',')
            if(len(tagsList) > 1):
                b = tagsList
            else:
                b = i[1]
        else:
            b = i[1]
        tagDict[a] = b
    return tagDict
        

@app.route('/api/ping', methods=['GET'])
def route1():
    returnDict = dict()
    returnDict["success"] = True
    return json.dumps(returnDict, indent=4)
        

def removeDuplicates(toSort):
    removeDuplicatesID = list()
    for i in toSort:
        id = i['id']
        if(id not in removeDuplicatesID):
            removeDuplicatesID.append(id)
            

    res = list()
    for ids in removeDuplicatesID:
        for i in toSort:
            if(i['id'] == ids):
                res.append(i)
    return res

def testFunc(result, sortBy, direction):
    checkSort = list()
    iter = 0
    checkSort.append(result[0][sortBy])
    for i in result:
        iter += 1
        checkSort.append(i[sortBy])
        if(iter > 0):
            if(direction == 'asc'):
                if(checkSort[iter] < checkSort[iter-1]):
                    return False
            if(direction == 'desc'):
                if(checkSort[iter] > checkSort[iter-1]):
                    return False
    print()
    print("Test Passed!", "\nSorted by:", sortBy, "\nDirection:", direction)
    print()
    return True


@app.route('/api/posts', methods=['GET'])
def routeMe():
    getTag = request.args.get('tags')
    getSortBy = request.args.get('sortBy', default='id')
    getDirection = request.args.get('direction', default='asc')

    queryDict = dict()
    queryDict['tags'] = getTag
    queryDict['sortBy'] = getSortBy
    queryDict['direction'] = getDirection

    #Parse if there are multiple tags to fetch
    tagsList = list(queryDict['tags'].split(','))
    if(len(tagsList) > 1):
        queryDict['tags'] = tagsList

    #Check if there are multiple queries
    isList = True
    if (type(queryDict['tags']) == type('test')):
        isList = False

    #Fetch from the API and store into dictionary
    getJsonResult = dict()
    getJsonResult['posts'] = list()
    if(isList):
        for i in queryDict['tags']:
            getJsonResult['posts'].append(getTagJSON('?tag=' + i).get('posts'))
        tempList = list()
        for i in getJsonResult['posts']:
            for j in i:
                tempList.append(j)
        getJsonResult['posts'] = tempList
        json.dump(getJsonResult['posts'], open('posts.json', 'w'), indent=4)
    else:
        getJsonResult['posts'] = list((getTagJSON('?tag=' + queryDict['tags']).get('posts')))
    

    #Sort the dictionary of results
    if (getSortBy=='popularity' or getSortBy=='reads' or getSortBy=='likes' or getSortBy=='id'):
        if(getDirection=='desc'):
            sortedReturn = sorted(getJsonResult['posts'], key= lambda x: x[getSortBy], reverse=True)
        elif(getDirection=='asc'):
            sortedReturn = sorted(getJsonResult['posts'], key= lambda x: x[getSortBy])            
        else:
            return json.dumps({"direction parameter is invalid."})
    else:
        return json.dumps({"sortBy parameter is invalid."})

    cleanList = removeDuplicates(sortedReturn)
    if(testFunc(cleanList, getSortBy, getDirection)):
        return json.dumps({"posts":cleanList}, indent=4)
    else:
        print("Test Failed!")


    