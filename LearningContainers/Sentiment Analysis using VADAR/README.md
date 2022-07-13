## Flask Web App for Sentiment Analysis using VADER 

### VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media.
https://github.com/cjhutto/vaderSentiment

For Learning of:
1)  Dockerizing Flask web application
2)  Local Deployment of Kubernetes through Minikube using Docker driver

### Running Flask locally using virtual environment
```
py -3 -m venv venv
venv\Scripts\activate
pip install Flask
python3 app.py
```

### Docker build and run application locally
```
docker build --tag <name-of-container> .
docker run -d -p 5000:5000 python-docker
docker ps
docker stop <name-of-container>
```

venv/Lib/site-packages not uploaded due to github 100 file limit
