from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from googlesearch import search
from bs4 import BeautifulSoup
import requests

# _____________________________________________ Sentiment Analysis __________________________________________________

classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def sentiment_analysis(input_text):
    result_dict = classifier(input_text)[0]
    result_dict['score'] = round(result_dict['score'] * 100, 2)
    
    return result_dict


# _____________________________________________ Disinformation Analysis _____________________________________________

class Article:
    def __init__(self, url, title, full_article, summarized_article, similarity_score) -> None:
        self.url = url
        self.title = title
        self.full_article = full_article
        self.summarized_article = summarized_article
        self.similarity_score = similarity_score


summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")
similarity_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def summarize(text):
    summary = summarizer(text, max_length=80, min_length=0, do_sample=False)

    return summary[0].get('summary_text')

def similarity_check(text1, text2):
    embedding_1= similarity_model.encode(text1, convert_to_tensor=True)
    embedding_2 = similarity_model.encode(text2, convert_to_tensor=True)

    res_tensor = util.pytorch_cos_sim(embedding_1, embedding_2)

    return res_tensor.item()

def disinformation_analysis(input_text, trusted_sources, article_count, is_batch_processing):
    if not trusted_sources:
        raise Exception("Error: Must include trusted sources")

    similarity_list = []
    article_list = []

    if len(input_text) > 100:
        text = summarize(input_text)
    else:
        text = input_text
    
    for source in trusted_sources:
        if source == "CNA":
            text += " site:channelnewsasia.com"
        elif source == "today":
            text += " site:todayonline.com"
        elif source == "gov.sg":
            text += " site:gov.sg"
        text += " OR"

    search_term = text[:-3]
    
    url_list = search(search_term, tld="co.in", num=article_count, stop=article_count, pause=2)

    headers = { 'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
        'cache-control':'no-cache',
        'dnt':'1',
        'pragma':'no-cache',
        'referer':'https',
        'sec-fetch-mode':'no-cors',
        'sec-fetch-site':'cross-site',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }

    for url in url_list:
        page = requests.get(url, headers=headers)
        if page.status_code == 200:
            try:
                soup = BeautifulSoup(page.content, "lxml")
                res_soup = soup.find('main', class_='main-content')
                title = res_soup.article['title']
                elements = res_soup.find_all('p')
                full_article = ""
                for element in elements:
                    if element == None:
                        continue
                    full_article += " "
                    full_article += element.text.strip()
            except Exception as e:
                title = None
                full_article = None
                print(f"Scraping Error! - {e}")

            if not is_batch_processing:
                try:
                    summarized_article = summarize(full_article)
                except Exception as e:
                    summarized_article = None
                    print(f"Summarizing Error! - {e}")
            else:
                summarized_article = None

            try:
                similarity_score = similarity_check(input_text, full_article)
                similarity_list.append(similarity_score)

                similarity_score = round(similarity_score*100, 2)
            except Exception as e:
                similarity_score = None
                print(f"Similarity Comparision Error! - {e}")

        else:
            print(f"Unable to retrieve page - Error Code {page.status_code}")
        
        article_list.append(Article(url, title, full_article, summarized_article, similarity_score))


    try:
        true_score = round(sum(similarity_list) / len(similarity_list)*100, 2)

        if true_score > 60:
            if true_score < 90:
                true_score += 10
            result = f"True with {true_score}% likelihood"
            
        else:
            true_score = 100 - true_score
            if true_score < 90:
                true_score += 10
            result = f"False with {true_score}% likelihood"

    except Exception as e:
        result = None
        print(f"Score Error! {e}")

    print(result)

    return article_list, search_term, result
        

