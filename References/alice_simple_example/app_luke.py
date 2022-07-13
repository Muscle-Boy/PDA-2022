from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
import jwt
import random
import json
from utils import nercolors, relationToNetwork, overviewRelationToNetwork, nerToSentiment
import requests
import os
import pdfplumber
import chardet
import re
import datetime
from bson import ObjectId
import nltk
import copy

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def mainPage():
    return f"<h1>Hello World</h1>"

# load previously processed file
@app.route("/loadExistingFile", methods=["POST"])
def loadExistingFile():
    file = request.files['existingFile']
    jsonData = json.loads(file.read())
    return jsonData

# load new file to be processed
@app.route("/uploadFile", methods=["GET", "POST"])
def receiveFile():
    print("Receiving File", flush=True)
    length = int(request.form['length'])
    returnJson = {}
    fileNames = json.loads(request.form['fileNames'])
    absaDocument = {}
    sentimentWordDocument = {}
    corpus = []
    corpusEntity = {}
    # corpusPassToRelation = []
    corpusRelation = []
    for i in range(length):
        file = request.files[f'file{i}']

        # Get filename
        fileName = fileNames[i]

        # Get file extension
        name, extension = os.path.splitext(fileName)
        print('POST SUCCESSFUL', fileName, flush=True)
        try:
            if extension == '.txt':
                byteString = file.read()
                encoding = chardet.detect(byteString)['encoding']
                text = byteString.decode(encoding)
            elif extension == '.pdf':
                text = ''
                with pdfplumber.load(file) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text()
            text = re.sub('\\\\', '', text)
            
            ## start the file processing via runAlice(). results stored in tempJson
            tempJson = runAlice(text)

        except Exception as err:
            print(err, "occured in"+fileName)
        except:
            print('Unknown error in'+fileName)
    print('RESULT', json.dumps(returnJson))
    returnJson = jsonify(returnJson)
    return returnJson

def runAlice(text):
    text = text.replace("\\x92", "")
    text = text.replace("\\x93", "")
    text = text.replace("\\x94", "")
    num_words = len(text.split(' '))

    # Topic Modelling
    print("Sending topic")
    
    ## see further bottom of codes to see the def for postTopicRequest
    topicJson = postTopicRequest([text], 1, 10)
    topics = topicJson['topics']
    print("receive topic")

    # variable for react
    jsonToReact = {}
    jsonToReact['topics'] = topics

    return jsonToReact
## End of runALICE ##

# Class to perform topic modelling
def postTopicRequest(text, no_topic, no_top_words):
    # "http://topics-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/topic_modelling"
    # define URL of API to be called 
    url = "http://topics:5040/topic_modelling"
    # message content to be sent with API call
    requestJson = {"document": text, "no_topic": no_topic, "no_top_words": no_top_words}
    # send api call to url
    result = requests.post(url, json=requestJson)
    return result.json()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)
© 2022 GitHub, Inc.
