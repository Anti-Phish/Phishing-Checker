import os
import threading
from os import system
import joblib
import pymongo as pymongo
from flask import Flask, request
from flask_cors import CORS
from tldextract import extract
import requests
from dotenv import load_dotenv
from url_detail_response import UrlResponse
import validators

load_dotenv()

vectorizer = joblib.load('Model/vectorizer.joblib')
model = joblib.load("Model/url_model.pkl")
db_client = pymongo.MongoClient(os.environ['MONGO'])
app = Flask(__name__)
CORS(app)


def ping_server():
    system("ping https://anti-phishing.herokuapp.com/")
    requests.get("https://anti-phishing.herokuapp.com/")
    threading.Timer(360, ping_server).start()


threading.Timer(360, ping_server).start()


@app.route('/')
def welcome():
    return 'Welcome to Anti-Phishing<br>' \
           'Send a POST request to /check endpoint to get info about the url. <br>' \
           '<h3> POST Body </h3><br>' \
           '{<br>' \
           '    "url": "https://example.com/path</br>' \
           '}<br>' \
           '<h3> Response code meaning </h3> <br>' \
           '<ol>' \
           '<li>Totally unsafe. Already confirmed phishing link.</li>' \
           '<li>Unsafe. ML model identity as a phishing link. Discretion is advised.</li>' \
           '<li>Generally safe, ML Model identify as safe but discretion is advised.</li>' \
           '<li>Safe. Already a well established site.</li>' \
           '</ol>'


@app.route('/check', methods=['POST'])
def check_url():
    url = request.json["url"]
    top_sites = db_client["top-mil"]["top-mil"]
    db = db_client["phising-url"]["phising"]
    tsd, td, tsu = extract(url)
    domain = td + '.' + tsu
    print(domain)
    if not validators.domain(domain):
        # return "bad request", 400
        return UrlResponse(0).response

    if top_sites.find_one({"url": domain}):
        print("Top mil site")
        return UrlResponse(4).response  # Safe

    db_check = db.find_one({"url": url})
    if db_check is not None:
        print("Found on Database")
        if db_check["Ok"] == "bad":
            return UrlResponse(1).response  # Already confirmed phishing site
        else:
            return UrlResponse(4).response  # Safe

    print("Found from model")
    if model.predict(vectorizer.transform([url])) == ['bad']:
        return UrlResponse(2).response  # Model identify as phishing link, Hard to confirm
    else:
        return UrlResponse(3).response  # Model identify as safe


@app.route('/health')
def check_health():
    return "healthy"


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
