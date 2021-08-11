import joblib
import pymongo as pymongo
from flask import Flask, request
from urllib.parse import urlparse
from flask_cors import CORS
from tldextract import extract

from url_detail_response import UrlResponse

db_client = pymongo.MongoClient(
    "mongodb+srv://admin:dhioc6uEtNGivrjJ@cluster0.74pvn.mongodb.net/phising-url?retryWrites=true&w=majority")
top_sites = db_client["top-mil"]["top-mil"]
db = db_client["phising-url"]["phising"]
model = joblib.load("Model/url_model.pkl")
vectorizer = joblib.load('Model/vectorizer.joblib')
app = Flask(__name__)
CORS(app)


@app.route('/')
def welcome():
    return 'Welcome to Anti-Phishing<br>' \
           'Send a POST request to /check endpoint to get info about the url. <br>' \
           '<h3> POST Body </h3><br>' \
           '{<br>' \
           '    "url": "https://example.com/path</br>'\
           '}<br>' \
           '<h3> Response code meaning </h3> <br>'\
           '<ol>' \
           '<li>Totally unsafe. Already confirmed phishing link.</li>' \
           '<li>Unsafe. ML model identity as a phishing link. Discretion is advised.</li>' \
           '<li>Generally safe, ML Model identify as safe but discretion is advised.</li>' \
           '<li>Safe. Already a well established site.</li>' \
           '</ol>'


@app.route('/check', methods=['POST'])
def check_url():
    url = request.json["url"]
    # domain = urlparse(url).netloc
    tsd, td, tsu = extract(url)  # prints abc, hostname, com
    domain = td + '.' + tsu
    print(domain)
    if top_sites.find_one({"url": domain}):
        print("Top mil site")
        return UrlResponse(4).response
        # return {"status": "4"}  # Safe

    db_check = db.find_one({"url": url})
    if db_check is not None:
        print("Found on Database")
        if db_check["Ok"] == "bad":
            return UrlResponse(1).response
            # return {"status": "1"}  # Already confirmed phishing site
        else:
            return UrlResponse(4).response
            # return {"status": "4"}  # Safe

    print("Found from model")
    if model.predict(vectorizer.transform([url])) == ['bad']:
        return UrlResponse(2).response
        # return {"status": "2"}  # Model identify as phishing link, Hard to confirm
    else:
        return UrlResponse(3).response
        # return {"status": "3"}  # Model identify as safe


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
