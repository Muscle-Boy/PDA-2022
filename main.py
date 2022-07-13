from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId
import requests
# from datetime import datetime

# _____________________________________________ Flask Configurations _____________________________________________

app = Flask(__name__)
# app.config["SECRET_KEY"] = '1da204f539bfd15c3c5a85e1397f8052'

# _____________________________________________ MongoDB Configurations _____________________________________________

app.config["MONGO_URI"] = "mongodb://localhost:27017/local"

mongo = PyMongo(app)
DisAnalysisDB = mongo.db.resultDisAnalysisDB

# _____________________________________________ Text Input Routes _____________________________________________

@app.route('/text-input', methods=['POST'])
def text_input():

    try:
        input_json = request.get_json()

        response = requests.post('http://localhost:8020/text-input', json=input_json)
        if response.status_code == 200:
            output_json = response.json()
        elif response.status_code == 404:
            raise Exception("Text Input Error 404")

        DisAnalysisDB.insert_one(output_json)
        output_json["_id"] = str(output_json["_id"])

        return parse_json(output_json), 201
    except Exception as e:
        return f"{e}", 404

    
@app.route('/text-input/results', methods=['GET'])
def text_input_results():

    DisAnalysisResults = []
    for DisAnalysisResult in DisAnalysisDB.find().sort("date_created", -1):
        DisAnalysisResult["_id"] = str(DisAnalysisResult["_id"])
        DisAnalysisResult["date_created"] = DisAnalysisResult["date_created"] #.strftime("%b %d %Y %H:%M:%S")
        DisAnalysisResults.append(DisAnalysisResult)

    return jsonify(DisAnalysisResults)


@app.route('/text-input/results/<id>', methods=['GET', 'DELETE'])
def text_input_results_indiv(id):
    if request.method == "GET":

        try:
            DisAnalysisResult = DisAnalysisDB.find_one_or_404({"_id":ObjectId(id)})
            DisAnalysisResult["_id"] = str(DisAnalysisResult["_id"])

            return parse_json(DisAnalysisResult)
        except Exception as e:
            return f"{e}", 404

    elif request.method == "DELETE":

        try:
            DisAnalysisDB.delete_one({"_id":ObjectId(id)})

            return "Disinformation Analysis Deletion Sucess!", 200
        except Exception as e:
            return f"{e}", 404


# _____________________________________________ Batch Processing Routes _____________________________________________




# _____________________________________________ Helper Functions _____________________________________________

def parse_json(data):
    return json.loads(json_util.dumps(data))

if __name__ == "__main__":
    app.run(debug=True, port=8010) # host="0.0.0.0"