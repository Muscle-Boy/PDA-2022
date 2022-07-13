from twitterScraper import run_scraper
from flask import Flask, send_file, request
from flask_cors import CORS
from zipfile import ZipFile, ZIP_DEFLATED
import os

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def run():
    return 'Twitter scraper running'

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    form = request.json
    json_request = {}

    limit = int(form["limit"])
    json_request['query'] = form['queries']
    print(json_request['query'], limit)

    json_request["only_sg"] = True
    excluded_users = ["ChannelNewsAsia", "straits_times", "STForeignDesk", "TODAYonline", "HIREMAIDEA"]
    json_request["excluded_users"] = excluded_users
    url = generate_url(json_request)

    print(url)

    run_scraper(url, app.root_path, limit, get_json=True)

    # Create zip folder for outputs and images
    filename = 'twitter.zip'
    zip_path = os.path.join(app.root_path, filename)
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zf:
        for folder in ['outputs', 'images']:
            folder_path = os.path.join(app.root_path, folder)
            for file in os.listdir(folder_path):
                path = os.path.join(folder_path, file)
                zf.write(path, arcname=os.path.join(folder, file))

    # Send the zip file
    return send_file(filename, mimetype='zip', download_name=filename, as_attachment=True)

def generate_url(json_request):
    search_query = json_request["query"]
    only_sg = json_request["only_sg"]
    excluded_users = json_request["excluded_users"]

    search_query = search_query.replace("\"", "%22")
    search_query = search_query.replace(" ", "%20")

    loc_str = ""
    if only_sg:
        loc_str = "near%3Asingapore%20within%3A10mi"

    exclude_str = ""
    for user in excluded_users:
        exclude_str += "-from%3A%40" + user + "%20"

    lang_str = "lang%3Aen" # Assume English by default

    url = "https://twitter.com/search?q=Mahathir%20mohamad&src=typeahead_click"
    return url

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7000, threaded=True)