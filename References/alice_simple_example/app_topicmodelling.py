from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from flask import Flask, request
import random

app = Flask(__name__)


@app.route('/')
def run():
    return 'Topics running'


@app.route('/topic_modelling', methods=['GET', 'POST'])
def topic_modelling_api():
    data = request.json
    document = data['document']
    no_topics = data['no_topic']
    no_top_words = data['no_top_words']
    list_of_topics = topic_modelling(document, no_topics, no_top_words)
    returnJson = {"topics": list_of_topics}
    return returnJson


def topic_modelling(documents, no_topics=3, no_top_words=5):

    """
    Args:
            documents: list of strings, each string is a document 
            no_topics: integer, number of topics to be extracted 
            no_top_words: integer, number of words describing each topic 
    
    """
    no_features = 1000

    # NMF is able to use tf-idf
    tfidf_vectorizer = TfidfVectorizer(max_features=no_features, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(documents)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    # Run NMF
    nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)

    # Extract words describing each topic, appending each topics's description to list_of_topics
    list_of_topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        words_of_topic = " ".join([tfidf_feature_names[i]
                                   for i in topic.argsort()[:-no_top_words - 1:-1]])
        list_of_topics.append(words_of_topic)

    # Altering data structure to pass to frontend 
    topics_words = []
    for topics in list_of_topics:
        words = topics.split()
        topics_words.append(words)

    outJson = {
        'name': 'Topics',
        'color': "hsl(13, 70%, 50%)",
        'children': []
    }

    t = 0
    for topic in topics_words:
        t = t + 1
        topic_vis = {
            "name": f"Topic{t}",
                    "color": "hsl(50, 70%, 50%)",
                    "children": []
        }

        for word in topic:
            loc = random.randint(5000, 100000)
            word_vis = {
                "name": word,
                "color": "hsl(196, 70%, 50%)",
                "loc": loc
            }
            topic_vis['children'].append(word_vis)
        outJson['children'].append(topic_vis)
    return outJson


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5040)