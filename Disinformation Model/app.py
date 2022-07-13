from flask import Flask, request, render_template, jsonify
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

@app.route('/')  
def home ():  
    return render_template("home.html")

@app.route('/checker')
def my_form():
    return render_template('my-form.html')

@app.route('/checker',  methods=['POST'])
def my_form_post():
    text = request.form['text']
    links = google(text)  
    print(links)
    links = crawlall(links)
    crossref_results = test(text,links[0],links[1],links[2])  
    return crossref_results

from sentence_transformers import SentenceTransformer, util

def google(a):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

# to search
    query = a
    x = []
    for j in search(query, tld="co.in", num=1, stop=3, pause=2):
        x.append(j)
    #returning a list
    return x

import requests
from bs4 import BeautifulSoup

def crawl(a):
    URL = a
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    company = soup.find_all('p')
    c = ""
    for i in range(0,len(company)):
        c = c + company[i].get_text()
    
    return(c)

def crawlall(a):
    xx = []
    for i in range(0,len(a)):
        y = str(crawl(a[i]))
        xx.append(y)
    return xx

def test(a,b,c,d):
    sentences_one = [a,b]
    sentences_two = [a,c]
    sentences_three = [a,d]

    model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(sentences_one)
    one = (util.pytorch_cos_sim(embeddings[0], embeddings[1]))
    print(one)

    embeddings = model.encode(sentences_two)
    two = (util.pytorch_cos_sim(embeddings[0], embeddings[1]))
    print(two)
    
    embeddings = model.encode(sentences_three)
    three = (util.pytorch_cos_sim(embeddings[0], embeddings[1]))
    print(three)
    
    avg = (one + two + three)/3
    print(avg)
    
    avg = avg.item()
    
    if avg >= 0.5:
        result = "real with" + " " + str(avg*100) + "% " + "confidence"
    
    else:
        result = "fake with" + " " + str((1-avg)*100) + "% " + "confidence"
    
    return(result)



if __name__ == '__main__':
    app.run()