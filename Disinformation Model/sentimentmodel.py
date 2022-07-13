from transformers import pipeline
classifier = pipeline("sentiment-analysis")

def sentiment(a):
    aa = classifier(a)
    aa = str(aa)

    return aa

#print(sentiment("i hate you"))
