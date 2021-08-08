import joblib
import pymongo as pymongo
from flask import Flask, request
from Vectorizer import Vectorizer
from urllib.parse import urlparse

db_client = pymongo.MongoClient(
    "mongodb+srv://admin:dhioc6uEtNGivrjJ@cluster0.74pvn.mongodb.net/phising-url?retryWrites=true&w=majority")
top_sites = db_client["top-mil"]["top-mil"]
db = db_client["phising-url"]["phising"]

vectorizer = Vectorizer("CSV Files/phishing_site_urls.csv")
model = joblib.load("Model/url_model.pkl")

app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to Anti-Phishing'


@app.route('/check', methods=['POST'])
def check_url():
    url = request.json["url"]
    domain = urlparse(url).netloc
    if top_sites.find_one({"url": domain}):
        print("Top mil site")
        return {"status": "good"}

    db_check = db.find_one({"url": url})
    if db_check is not None:
        print("Found on Database")
        return str(db_check["Ok"])

    print("Found from model")
    return str(model.predict(vectorizer.transform([url])))


if __name__ == '__main__':
    app.run()
