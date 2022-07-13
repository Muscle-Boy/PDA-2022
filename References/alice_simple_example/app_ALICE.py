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
            
            # start the file processing via runAlice(). results stored in tempJson
            tempJson = runAlice(text)

            absaChapter = tempJson['sentiment'][2]['absaChapter'].copy()
            sentimentWordChapter = tempJson['sentiment'][2]['sentimentWordChapter'].copy()
            absaDocument = absa_document_combined_c(absaDocument, absaChapter, name)
            sentimentWordDocument = entity_sentimentwords_document(sentimentWordDocument, sentimentWordChapter)

            returnJson[name] = tempJson

            tempEntity = tempJson['ner']['ents'].copy()
            for entity in tempEntity:
                key = entity['text']+'_'+entity['type']
                if key in corpusEntity:
                    corpusEntity[key]['value'] += 1
                    corpusEntity[key]['documents'].add(name)
                else:
                    corpusEntity[key] = {
                        'id': entity['text'],
                        'label': entity['text'],
                        'value': 1,
                        'documents': set([name]),
                        'type': entity['type'],
                        'color': nercolors[entity['type']]
                    }
            # corpusPassToRelation.extend(tempJson['ner'].pop('passToRelation'))
            corpus.append(text)
            print(f"Current Corpus Text: {corpus}", flush=True)

            newRelation = tempJson['relation'].copy()
            for relation in newRelation:
                relation['documents'] = [name]
                corpusRelation.append(relation)

        except Exception as err:
            print(err, "occured in"+fileName)
        except:
            print('Unknown error in'+fileName)
    if length > 1:
        print(f"Corpus being sent to overview {corpus}", flush=True)
        returnJson['Overview'] = getOverview(corpus, corpusEntity, corpusRelation,
                                             absaDocument, sentimentWordDocument, fileNames)
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

    # Sentiment
    sentimentJson = postSentimentRequest(text)
    sentimentList = sentimentJson["sentiment"]
    key_data_sentiment = sentimentList[0]["sentiment"]
    key_data_legitimacy = sentimentList[1]["sentiment"]
    sentimentList[0]["sentiment"] = "sentiment"
    sentimentList[1]["sentiment"] = "subjective"

    # Classifier
    print("sending classifier")
    classifyJson = postClassifierRequest(text)
    classify = classifyJson['classify']
    print("receive classifier")

    # Word cloud
    print("sending wordcloud")
    bytestringJson = postWordCloud(text)
    wordcloud = bytestringJson['data']
    print("receive wordcloud")

    # Summary
    print("Sending to summary")
    summaryJson = postSummaryRequest(text, 3)
    summary = summaryJson["summary"]
    print("Receive from summary")

    # NER
    print("Sending to NER")
    nerJson = postNerRequest(text)
    ner = nerJson['ner']
    passToRelation = ner.pop('passToRelation')
    print("Receive from NER")

    # Relation
    print("Send to relation")
    relationJson = postRelationRequest(passToRelation)
    relation = relationJson['relation']
    print("Receive from Relation")

    # Network
    print("start relation network")
    network = relationToNetwork(relation)
    print("finished relation network")

    # ABSA
    print("start ABSA")
    nerDataToSentiment = copy.deepcopy(ner)
    nerData = nerToSentiment(nerDataToSentiment)
    ABSAdata = postABSA(nerData)
    sentimentList.append(ABSAdata)
    print('finish ABSA')

    # wcabsa
    print('start wcabsa')
    wcabsaInput = ABSAdata['sentimentTableData']
    wcabsaData = postwcabsa(wcabsaInput)
    sentimentList[2]['sentimentWordCloud'] = wcabsaData['sentimentWordCloud']
    sentimentList[2]['sentimentWordChapter'] = wcabsaData['sentimentWordChapter']
    print('finish wcabsa')

    # Key Data
    print('doing key data stuff')
    key_data_classification = classify
    keyData = {"num_words": num_words, "topic_classifier": key_data_classification, "sentiment": key_data_sentiment,
               "legitimacy": key_data_legitimacy}

    jsonToReact = {}
    jsonToReact["keyData"] = keyData
    jsonToReact['sentiment'] = sentimentList
    jsonToReact['summary'] = summary
    jsonToReact['topics'] = topics
    jsonToReact['classify'] = classify
    jsonToReact['ner'] = ner
    jsonToReact['relation'] = relation
    jsonToReact['network'] = network
    jsonToReact['wordcloud'] = wordcloud
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



def absa_document_combined_c(combined, inc, filename):
    for entity, value in inc.items():
        sentiment = value['sentiment']
        if entity not in combined.keys():
            combined[entity] = {
                'sentiment': '',
                'chapters': {
                    'Positive': [],
                    'Negative': [],
                    'Neutral': []
                }
            }
        combined[entity]['chapters'][sentiment].append(filename)

    for ent, val in combined.items():
        index_label = {0: 'Positive', 1: 'Negative', 2: 'Neutral'}
        pos_list_len = len(val['chapters']['Positive'])
        neg_list_len = len(val['chapters']['Negative'])
        neu_list_len = len(val['chapters']['Neutral'])
        len_list = [pos_list_len, neg_list_len, neu_list_len]
        index = len_list.index(max(len_list))
        label = index_label[index]
        combined[ent]['sentiment'] = label

    return combined


def entity_sentimentwords_document(combined, inc):
    df = ['neutral']
    for entity, s_w in inc.items():
        if entity in combined.keys():
            if not all(elem in df for elem in s_w['pos']):
                if all(elem in df for elem in combined[entity]['pos']):
                    combined[entity]['pos'] = s_w['pos']
                    combined[entity]['neg'] = s_w['neg']
                else:
                    combined[entity]['pos'] = combined[entity]['pos'] + s_w['pos']
                    combined[entity]['neg'] = combined[entity]['neg'] + s_w['neg']
        else:
            combined[entity] = {}
            combined[entity]['pos'] = s_w['pos']
            combined[entity]['neg'] = s_w['neg']
    return combined


def absa_document_to_react(dic):
  returnlist = []
  for entity in dic.keys():
    returnlist.append({
        'aspect':entity, 
        'sentiment':dic[entity]['sentiment'], 
        'chapters':{
            'Positive': dic[entity]['chapters']['Positive'], 
            'Negative': dic[entity]['chapters']['Negative'], 
            'Neutral': dic[entity]['chapters']['Neutral']
            }
    }) 
  return returnlist 


def postSummaryRequest(text, no_of_sentence):
    # "http://summary-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/textSummarizer"
    url = "http://summary:5060/textSummarizer"
    requestJson = {"text": text, "no_of_sentence": no_of_sentence}
    result = requests.post(url, json=requestJson)
    return result.json()


def postSentimentRequest(text):
    # "http://sentiment-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/sentiment"
    url = "http://sentiment:5050/sentiment"
    requestJson = {"text": text}
    result = requests.post(url, json=requestJson)
    return result.json()


def postNerRequest(text):
    # "http://ner-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/ner"
    url = "http://ner:5020/ner"
    requestJson = {"text": text}
    result = requests.post(url, json=requestJson)
    return result.json()


def postRelationRequest(ner):
    # "http://relation-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/relation"
    url = "http://relation:5010/relation"
    requestJson = {"ner": ner}
    try:
        result = requests.post(url, json=requestJson)
    except Exception as err:
        print("Relation Error", err, flush=True)
    return result.json()


def postClassifierRequest(text):
    # "http://classifier-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/classifier"
    url = "http://classifier:5030/classifier"
    requestJson = {"document": text}
    result = requests.post(url, json=requestJson)
    return result.json()


def postWordCloud(text):
    # "http://wordcloud-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/wordcloud"
    url = "http://wordcloud:5070/wordcloud"
    requestJson = {"data": text}
    result = requests.post(url, json=requestJson)
    return result.json()


def postCluster(corpus):
    # "http://clustering-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/cluster"
    url = "http://clustering:5080/cluster"
    print("Corpus is: ", corpus, flush=True)
    result = requests.post(url, json=corpus)
    print("result in server: ", result)
    return result.json()


def postABSA(data):
    try:
        # http://absa-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/aspectSentiment
        url = "http://absa:5090/aspectSentiment"
        result = requests.post(url, json=data)
        result = result.json()
    except Exception as err:
        print(f"Error in ABSA: {err}", flush=True)
    return result

def postwcabsa(data):
    try:
        # http://wcabsa-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/wordCloudABSA
        url = "http://wordcloudabsa:5100/wordCloudABSA"
        result = requests.post(url, json=data)
        result = result.json()
    except Exception as err:
        print(f'Error in wcabsa:{err}', flush=True)
    return result


def postwcabscaOverview(data):
    try:
        # "http://wcabsaoverview-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/wcABSAOverview"
        url = "http://wordcloudabsa:5100/wcABSAOverview"
        result = requests.post(url, json=data)
        result = result.json()
    except Exception as err:
        print(f'Error in wcabsaOverview:{err}', flush=True)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)
© 2022 GitHub, Inc.
