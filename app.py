import joblib
import pymongo as pymongo
from flask import Flask, request
from urllib.parse import urlparse

db_client = pymongo.MongoClient(
    "mongodb+srv://admin:dhioc6uEtNGivrjJ@cluster0.74pvn.mongodb.net/phising-url?retryWrites=true&w=majority")
top_sites = db_client["top-mil"]["top-mil"]
db = db_client["phising-url"]["phising"]
model = joblib.load("Model/url_model.pkl")
vectorizer = joblib.load('Model/vectorizer.joblib')
app = Flask(__name__)


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
    domain = urlparse(url).netloc
    if top_sites.find_one({"url": domain}):
        print("Top mil site")
        return {"status": "4"}  # Safe

    db_check = db.find_one({"url": url})
    if db_check is not None:
        print("Found on Database")
        if db_check["Ok"] == "bad":
            return {"status": "1"}  # Already confirmed phishing site
        else:
            return {"status": "4"}  # Safe

    print("Found from model")
    if model.predict(vectorizer.transfor[url]) == ['bad']:
        return {"status": "2"}  # Model identify as phishing link, Hard to confirm
    else:
        return {"status": "3"}  # Model identify as safe


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
    # app.run(ssl_context='adhoc')
