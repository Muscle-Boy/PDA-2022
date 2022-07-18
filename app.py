from flask import Flask, render_template, request, redirect, flash
import requests
import pandas as pd

# _____________________________________________ Flask Configurations ________________________________________________

IS_LOCAL_DEPLOYMENT = False
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config["SECRET_KEY"] = '1da204f539bfd15c3c5a85e1397f8052'

# _____________________________________________ Mainpage Route ______________________________________________________

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

# _____________________________________________ Text Input Routes ___________________________________________________

@app.route('/text-input', methods=['GET', 'POST'])
def text_input():

    if request.method == 'GET':
        return render_template('text-input.html')

    elif request.method == 'POST':
        res_dict = request.form.to_dict()

        input_json = {}
        input_json["input_text"] = res_dict['text']
        input_json["article_count"] = int(res_dict['article_count'])

        trusted_sources = list(res_dict)
        trusted_sources.remove('text')
        trusted_sources.remove('article_count')
        input_json["trusted_sources"] = trusted_sources

        # print(f'res_dict is {res_dict}')
        # print(f'input_json is {input_json}')

        if IS_LOCAL_DEPLOYMENT:
            response = requests.post('http://localhost:8010/text-input', json=input_json)
        else:
            response = requests.post('http://main-service:5010/text-input', json=input_json)

        return redirect('/text-input/results')


@app.route('/text-input/results', methods=['GET', 'POST'])
def text_input_results():

    if request.method == 'GET':
        if IS_LOCAL_DEPLOYMENT:
            response = requests.get('http://localhost:8010/text-input/results')
        else:
            response = requests.get('http://main-service:5010/text-input/results')
        result_list = response.json()

        return render_template('text-input-results.html', result_list=result_list)

    elif request.method == 'POST':
        delete_id_dict = request.form.to_dict()
        id = delete_id_dict['id']

        if IS_LOCAL_DEPLOYMENT:
            response = requests.delete('http://localhost:8010/text-input/results/'+f'{id}')
        else:
            response = requests.delete('http://main-service:5010/text-input/results/'+f'{id}')

        return redirect('/text-input/results')


# _____________________________________________ Batch Processing Routes _____________________________________________

@app.route('/batch-processing', methods=['GET', 'POST'])
def batch_processing():

    if request.method == 'GET':

        return render_template('batch-processing.html')

    elif request.method == 'POST':

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            df = pd.read_excel(file, index_col=None, header=None)
            input_list = df[0].tolist()
            input_json = [{ "input_text" : input_text } for input_text in input_list]

        if IS_LOCAL_DEPLOYMENT:    
            response = requests.post('http://localhost:8010/batch-processing', json=input_json)
        else:
            response = requests.post('http://main-service:5010/batch-processing', json=input_json)
        
        return redirect('/batch-processing/results')


@app.route('/batch-processing/results', methods=['GET', 'POST'])
def batch_processing_results():

    if request.method == 'GET':
        if IS_LOCAL_DEPLOYMENT:
            response = requests.get('http://localhost:8010/batch-processing/results')
        else:
            response = requests.get('http://main-service:5010/batch-processing/results')

        result_list = response.json()

        return render_template('batch-processing-results.html', result_list=result_list)

    elif request.method == 'POST':
        delete_id_dict = request.form.to_dict()
        id = delete_id_dict['id']

        if IS_LOCAL_DEPLOYMENT:
            response = requests.delete('http://localhost:8010/batch-processing/results/'+f'{id}')
        else:
            response = requests.delete('http://main-service:5010/batch-processing/results/'+f'{id}')

        return redirect('/batch-processing/results')


# _____________________________________________ Helper Functions ____________________________________________________

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    if IS_LOCAL_DEPLOYMENT:
        app.run(debug=True, port=8000) # host="0.0.0.0"
    else:
        app.run(host="0.0.0.0", port=8000)