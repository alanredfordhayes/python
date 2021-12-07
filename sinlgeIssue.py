import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://dotdash.atlassian.net/rest/api/3/search"
email = input("email address of admin user: ")
api_token = input("api_token of admin user: ")
auth = HTTPBasicAuth(email, api_token)
jqlQuery = 'Key = VIDEO-34771'

headers = {
"Accept": "application/json"
}

query = {
'jql': jqlQuery
}

response = requests.request(
"GET",
url,
headers=headers,
params=query,
auth=auth
)

data = json.loads(response.text)
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
