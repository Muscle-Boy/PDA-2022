from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId
import requests
# from datetime import datetime

# _____________________________________________ Flask Configurations ________________________________________________

IS_LOCAL_DEPLOYMENT = False

app = Flask(__name__)
# app.config["SECRET_KEY"] = '1da204f539bfd15c3c5a85e1397f8052'

# _____________________________________________ MongoDB Configurations ______________________________________________

if IS_LOCAL_DEPLOYMENT:
    app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
else:
    app.config["MONGO_URI"] = "mongodb://mongo-service.default.svc.cluster.local:5030/local"

mongo = PyMongo(app)
TextInputDB = mongo.db.TextInputDB
BatchProcessingDB = mongo.db.BatchProcessingDB

# _____________________________________________ Text Input Routes ___________________________________________________

@app.route('/text-input', methods=['POST'])
def text_input():

    try:
        input_json = request.get_json()

        if IS_LOCAL_DEPLOYMENT:
            response = requests.post('http://localhost:8020/text-input', json=input_json)
        else:
            response = requests.post('http://disinformation-service:5020/text-input', json=input_json)
        if response.status_code == 200:
            output_json = response.json()
        elif response.status_code == 404:
            raise Exception("Text Input Error 404")

        TextInputDB.insert_one(output_json)
        output_json["_id"] = str(output_json["_id"])

        return parse_json(output_json), 201
    except Exception as e:
        return f"{e}", 404

    
@app.route('/text-input/results', methods=['GET'])
def text_input_results():

    TextInputResult_list = []
    for TextInputResult in TextInputDB.find().sort("date_created", -1):
        TextInputResult["_id"] = str(TextInputResult["_id"])
        # TextInputResult["date_created"] = TextInputResult["date_created"].strftime("%b %d %Y %H:%M:%S")
        TextInputResult_list.append(TextInputResult)

    return jsonify(TextInputResult_list)


@app.route('/text-input/results/<id>', methods=['GET', 'DELETE'])
def text_input_results_indiv(id):

    if request.method == "GET":

        try:
            TextInputResult = TextInputDB.find_one_or_404({"_id":ObjectId(id)})
            TextInputResult["_id"] = str(TextInputResult["_id"])

            return parse_json(TextInputResult)
        except Exception as e:
            return f"{e}", 404

    elif request.method == "DELETE":

        try:
            TextInputDB.delete_one({"_id":ObjectId(id)})

            return f"Text Input Result id:{id} Deletion Sucess!", 200
        except Exception as e:
            return f"{e}", 404


# _____________________________________________ Batch Processing Routes _____________________________________________

@app.route('/batch-processing', methods=['POST'])
def batch_processing():

    try:
        input_json = request.get_json()
        
        if IS_LOCAL_DEPLOYMENT:
            response = requests.post('http://localhost:8020/batch-processing', json=input_json)
        else:
            response = requests.post('http://disinformation-service:5020/batch-processing', json=input_json)
        if response.status_code == 200:
            output_json = response.json()
        elif response.status_code == 404:
            raise Exception("Batch Processing Error 404")

        BatchProcessingDB.insert_one(output_json)
        output_json["_id"] = str(output_json["_id"])

        return parse_json(output_json), 201
    except Exception as e:
        return f"{e}", 404

    
@app.route('/batch-processing/results', methods=['GET'])
def batch_processing_results():

    BatchProcessingResult_list = []
    for BatchProcessingResult in BatchProcessingDB.find().sort("date_created", -1):
        BatchProcessingResult["_id"] = str(BatchProcessingResult["_id"])
        # BatchProcessingResult["date_created"] = BatchProcessingResult["date_created"].strftime("%b %d %Y %H:%M:%S")
        BatchProcessingResult_list.append(BatchProcessingResult)

    return jsonify(BatchProcessingResult_list)


@app.route('/batch-processing/results/<id>', methods=['GET', 'DELETE'])
def batch_processing_results_indiv(id):

    if request.method == "GET":

        try:
            BatchProcessingResult = BatchProcessingDB.find_one_or_404({"_id":ObjectId(id)})
            BatchProcessingResult["_id"] = str(BatchProcessingResult["_id"])

            return parse_json(BatchProcessingResult)
        except Exception as e:
            return f"{e}", 404

    elif request.method == "DELETE":

        try:
            BatchProcessingDB.delete_one({"_id":ObjectId(id)})

            return f"Batch Processing Result id:{id} Deletion Sucess!", 200
        except Exception as e:
            return f"{e}", 404

# _____________________________________________ Helper Functions ____________________________________________________

def parse_json(data):
    return json.loads(json_util.dumps(data))

if __name__ == "__main__":
    if IS_LOCAL_DEPLOYMENT:
        app.run(debug=True, port=8010) # host="0.0.0.0"
    else:
        app.run(host="0.0.0.0", port=8010)
