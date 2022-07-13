from flask import Flask, request, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
set(stopwords.words('english'))

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    stop_words = stopwords.words('english')
    
    #convert to lowercase
    text1 = request.form['text1'].lower()
    text_final = ''.join(c for c in text1 if not c.isdigit())
        
    #remove stopwords    
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    compound = dd['compound']

    if (compound > 0.05):
        final = "Positive"
    elif (compound < -0.05):
        final = "Negative"
    else:
        final = "Neutral"

    return render_template('index.html', final=final, pos=dd['pos'], neu=dd['neu'], neg=dd['neg'], compound=compound, text_final=text_final)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002, threaded=True)