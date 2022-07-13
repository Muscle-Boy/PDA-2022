from flask import Flask
# from utils import nercolors, relationToNetwork, overviewRelationToNetwork, nerToSentiment

app= Flask(__name__)

@app.route("/")
def mainPage():
    return "Welcome to the index page"

@app.route('/h1/')
def who():
    return "Who are you"

@app.route('/h1/<username>')
def greet(username):
    return("Hi there,{username}!")

@app.route("/members")
def members():
    return{"members":["Member1","Member2","Member3"]}

if __name__ == "__main__":
	app.run(host="0.0.0.0", threaded=True)
 
#  test