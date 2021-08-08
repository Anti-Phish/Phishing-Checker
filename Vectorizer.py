import pandas
from sklearn.feature_extraction.text import TfidfVectorizer


def make_tokens(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')  # make tokens after splitting by slash
    total_Tokens = []
    for i in tkns_BySlash:
        tokens = str(i).split('-')  # make tokens after splitting by dash
        tkns_ByDot = []
        for j in range(0, len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')  # make tokens after splitting by dot
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens + tokens + tkns_ByDot
    total_Tokens = list(set(total_Tokens))  # remove redundant tokens
    if 'com' in total_Tokens:
        total_Tokens.remove(
            'com')  # removing .com since it occurs a lot of times and it should not be included in our features
    return total_Tokens


class Vectorizer:

    def __init__(self, dataset):
        self.vectorizer = TfidfVectorizer(tokenizer=make_tokens)
        self.vectorizer.fit(pandas.read_csv("CSV Files/phishing_site_urls.csv")["URL"])

    def transform(self, url):
        return self.vectorizer.transform(url)
