import requests
from requests.auth import HTTPBasicAuth
from csv import reader
import json
import os
import base64

csv_path = os.environ [ 'confluence_import_csv' ]
importCSV = open(csv_path, 'r')
csv_reader = reader(importCSV) 
domain = os.environ[ 'confluence_domain' ]
email = os.environ[ 'confluence_admin_email' ]
api_token = os.environ[ 'confluence_api_token' ]
message = email + ":" + api_token
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')
auth = "Basic " + base64_message 

headers = {
   "Accept": "application/json",
   "Authorization": auth
}

member_list = []    
name = "confluence-users"
start = 0
flag = False
while flag is False:
    query = {
        'name': name,
        'start': start
    }

    rest = ".atlassian.net/wiki/rest/api"
    url = "https://" + domain + rest + "/group/member"
    response = requests.request( "GET", url, headers=headers, params=query)
    data = json.loads(response.text)
    results = data[ 'results' ]
    member_number = len(results)
    start = start + member_number
    member_list.append(results)

    if member_number == 0:
        flag = True


api_token = os.environ[ 'atlassian_api_token' ]
message = email + ":" + api_token
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')
auth = "Basic " + base64_message 

for row in csv_reader:
    name = row[0]
    email = row[1]
    found = False
                
    for list in member_list:
        for confluence_user in list:
            confluence_user_email = confluence_user['email']
            if email is confluence_user:
                found = True
                
    if found is False:
        if email != 'Email':
            print("Not found: " + email)
            directory_id = os.environ['confluence_dir_id']
            url = "https://api.atlassian.com/scim/directory/" + directory_id + "/Users"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": auth
            }
            
            print(auth)
            payload = json.dumps( {
                "userName": email,
                "emails": [
                    {
                    "value": email,
                    "type": "work",
                    "primary": True
                    }
                ],
                "name": {
                    "formatted": "",
                    "familyName": "",
                    "givenName": "",
                    "middleName": "",
                    "honorificPrefix": "",
                    "honorificSuffix": ""
                },
                "displayName": name,
                "nickName": "",
                "title": "",
                "preferredLanguage": "",
                "department": "",
                "organization": "",
                "timezone": "",
                "phoneNumbers": [
                    {
                    "value": "",
                    "type": "",
                    "primary": True
                    }
                ],
                "active": True
            } )
            
            response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers
            )
            
            print(response.text)

        