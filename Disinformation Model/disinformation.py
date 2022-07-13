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
    page = requests.get(URL, headers = {'User-agent': 'your bot 0.1'})

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

def disinformationmodel(a):

    #if len > 60, use summerization
    links = google(a)  
    print(links)
    links = crawlall(links)
    crossref_results = test(a,links[0],links[1],links[2])

    
    return crossref_results
