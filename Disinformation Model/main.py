from disinformation import *
from sentimentmodel import *
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from flask_cors import CORS
app = Flask(__name__)
# app.secret_key = 'This is your secret key to utilize session in Flask'
CORS(app)

# @app.route('/')  
# def home ():  
#     return render_template("home.html")


# @app.route('/checker')
# def my_form():
#     return render_template('my-form.html')

@app.route('/checker',  methods=['POST'])
def my_form_post():
    text = request.get_json(force=True)['form']
    print(text)
    test = text.get('textinput')
    crossref_results = disinformationmodel(test)
    print(crossref_results)
    return jsonify(success=True,result = crossref_results)

# @app.route('/sentiment')
# def my_form2():
#     return render_template('stance.html')

@app.route('/sentiment',  methods=['POST'])
def my_form_post2():
    # text = request.form['text']
    text = request.get_json(force=True)['form']
    sen = sentiment(text.get('textinput')) 
    return jsonify(result=sen)


@app.route('/readcsv')
def index():
    return ("still in progress")    

if __name__ == '__main__':
    app.run()
