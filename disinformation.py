from flask import Flask, request, jsonify
from disinformation_modeling import *
from datetime import datetime


# _____________________________________________ Flask Configurations ________________________________________________

IS_LOCAL_DEPLOYMENT = False

app = Flask(__name__)

# _____________________________________________ Text Input Routes ___________________________________________________

@app.route('/text-input', methods=['POST'])
def text_input():

    try:
        input_json = request.get_json()

        input_text = input_json["input_text"]
        trusted_sources = input_json["trusted_sources"]
        article_count = input_json["article_count"]
        result_model = ''
        article_list, search_term, result_model = disinformation_analysis(input_text, trusted_sources, article_count, False)

        sentiment_dict = sentiment_analysis(input_text)

        return_json = {
            "input_text" : input_text,
            "search_term" : search_term,
            "result" : result_model,
            "sentiment_label" : sentiment_dict['label'],
            "sentiment_score" : sentiment_dict['score'],
            "date_created": datetime.now(),
            "Articles" : [
                {
                    "url" : article.url,
                    "title" : article.title,
                    "full_article" : article.full_article,
                    "summarized_article" : article.summarized_article,
                    "similarity_score" : article.similarity_score
                } for article in article_list
            ]
        }

        return jsonify(return_json), 200
    except Exception as e:
        return f"{e}", 404

# _____________________________________________ Batch Processing Routes _____________________________________________

@app.route('/batch-processing', methods=['POST'])
def batch_processing():
    
    try:
        input_list = request.get_json()
        return_json = {
            "batch_result_list" : []
        }

        for input in input_list:
            input_text = input["input_text"]

            article_list, search_term, result = disinformation_analysis(input_text, ['CNA', 'today'], 3, True)

            sentiment_dict = sentiment_analysis(input_text)

            return_dict = {
                "input_text" : input_text,
                "result" : result,
                "sentiment_label" : sentiment_dict['label'],
                "sentiment_score" : sentiment_dict['score'],
                "Articles" : [
                    {
                        "url" : article.url,
                        "title" : article.title,
                    } for article in article_list
                ]
            }

            return_json["batch_result_list"].append(return_dict)
        
        return_json["date_created"] = datetime.now()

        return jsonify(return_json), 200
    except Exception as e:
        return f"{e}", 404

# _____________________________________________ Helper Functions ____________________________________________________

if __name__ == "__main__":
    if IS_LOCAL_DEPLOYMENT:
        app.run(debug=True, port=8020) # host="0.0.0.0"
    else:
        app.run(host="0.0.0.0", port=8020)
