from re import T
from flask import Flask, request, render_template, jsonify
from transformers import pipeline
import time

from flask_cors import CORS

#use axios to call the end point of backend
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
classifier = pipeline("sentiment-analysis")
app = Flask(__name__)
CORS(app)

#api calling is fetch/axios/ajax

# @app.route('/')
# def my_form():
#     return render_template('my-form.html')


#api  actions
@app.route("/app/upload", methods=['POST'])
def my_form_post(): 
    # text = request.form['text']
    text = request.get_json(force=True)['form']
    print(text.get('textinput'))
    #processed_text = text + text
    result = summarizer(text.get('textinput'), max_length=130, min_length=3, do_sample=False)
    # print(result)
    # return jsonify(result=result)
    return jsonify(success=True, result=result)


@app.route('/login')
def hello_name():
    return "processed_text"

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/movies')
def get_movies():
    movies = [
        "test",
        "hi"
    ]
    return jsonify(results=movies)

if __name__ == 'main':
    app.run()