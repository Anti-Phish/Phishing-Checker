# import pandas as pd
# csv_input = pd.read_csv('output.csv')
# del csv_input['rank']
# # csv_input['Lable'] = "good"
# csv_input.to_csv('output1.csv', index=False)
from urllib.parse import urlparse
import validators

print(validators.url("http://www.example.test/foo/bar"))
domain = urlparse('http://www.example.test/foo/bar')
print(domain)