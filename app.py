from flask import Flask, render_template, url_for, request, redirect, flash
import requests

# _____________________________________________ Flask Configurations _____________________________________________

app = Flask(__name__)

# _____________________________________________ Mainpage Route _____________________________________________

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

# _____________________________________________ Text Input Routes _____________________________________________

@app.route('/text-input', methods=['GET', 'POST'])
def text_input():

    if request.method == 'GET':
        return render_template('text-input.html')

    elif request.method == 'POST':
        res_dict = request.form.to_dict()

        input_json = {}
        input_json["input_text"] = res_dict['text']
        input_json["trusted_sources"] = list(res_dict)
        input_json["article_count"] = int(res_dict['article_count'])

        response = requests.post('http://localhost:8010/text-input', json=input_json)
        
        return 0


@app.route('/text-input/results', methods=['GET'])
def text_input_results():

    response = requests.get('http://localhost:8010/text-input/results')

    result_list = response.json()

    return render_template('text-input-results.html')


@app.route('/text-input/results/<id>', methods=['GET'])
def text_input_results_indiv(id):

    response = requests.get('http://localhost:8010/text-input/results/'+f'{id}')

    result = response.json()

    return render_template('text-input-results-indiv.html')

# _____________________________________________ Batch Processing Routes _____________________________________________

@app.route('/batch-processing', methods=['GET', 'POST'])
def batch_processing():
    if request.method == 'GET':
        return render_template('batch-processing.html')

    elif request.method == 'POST':
        
        return 0


@app.route('/batch-processing/results', methods=['GET'])
def batch_processing_results():
    return render_template('batch-processing-results.html')


@app.route('/batch-processing/results/<id>', methods=['GET'])
def batch_processing_results_indiv(id):
    return render_template('batch-processing-results-indiv.html')

# _____________________________________________ Helper Functions _____________________________________________

if __name__ == "__main__":
    app.run(debug=True, port=8000)