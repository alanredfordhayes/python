import requests
import pymongo
from requests.auth import HTTPBasicAuth
import os
import json

# Jira Vars
domain = os.environ['jira_domain']
jira_admin_email = os.environ['jira_admin_email']
jira_api_token = os.environ['jira_api_token']
url = "https://" + domain + ".atlassian.net/rest/api/3/applicationrole"
auth = HTTPBasicAuth(jira_admin_email, jira_api_token)

# Mongo Vars
mongo_initdb_root_username = os.environ['MONGO_INITDB_ROOT_USERNAME']
mongo_initdb_root_password = os.environ['MONGO_INITDB_ROOT_PASSWORD']
mongo_url = os.environ['MONGO_URL']
mongo_client_url = 'mongodb://' + mongo_initdb_root_username + ':' + mongo_initdb_root_password + '@' + mongo_url 

#Mongo DB Setup
mongo_client = pymongo.MongoClient(mongo_client_url)
jira_db = mongo_client['jira_db']
collection_jira_application_roles = jira_db['jira_application_roles']
items_collection_jira_application_roles = list(collection_jira_application_roles.find())

#JIA API CALL
headers = { "Accept": "application/json"}
response = requests.request( "GET", url, headers=headers, auth=auth )
data = json.loads(response.text)

#Loop Through Data and Insert it in DB
for defaultGroup in data:
   insert_defaultGroup_bool = True
   defaultGroup_key = defaultGroup['key']
   for found in items_collection_jira_application_roles:
      found_key = found['key']
      if defaultGroup_key == found_key:
         insert_defaultGroup_bool = False
   if insert_defaultGroup_bool is True:
      insert_defaultGroup = collection_jira_application_roles.insert_one(defaultGroup)
      print(insert_defaultGroup.inserted_id)