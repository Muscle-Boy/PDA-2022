from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def backend():
    if request.is_json:
        data = request.get_json()
        text = data['data']
        return text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8010)
