
import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import os
import time

domain = os.environ['jira_domain']
url = "https://" + domain + ".atlassian.net/rest/api/3/search"
email = os.environ['jira_admin_email']
api_token = os.environ['jira_api_token']
auth = HTTPBasicAuth(email, api_token)
csv_name = '/Users/ahayes/Downloads/QA Metadata Sheet - THE SPRUCE- READY.csv'
filePath = "/Users/ahayes/Downloads/badDocID.txt"
csv_path = "/Users/ahayes/Downloads/import.csv"
csv_header = ['Summary', 'Issue key', 'Issue id', 'Issue Type', 'Tags', 'Status']

if os.path.exists(csv_path):
    os.remove(csv_path)

if os.path.exists(filePath):
    os.remove(filePath)

importCSV = open(csv_path, 'w', encoding='UTF8')
writer = csv.writer(importCSV)
writer.writerow(csv_header)
importCSV.close()

with open(csv_name, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        lenghtIssues = 0
        newTags = row['NEW QA TAGS']
        videoDocID = row['Video Document ID']
        jqlQuery = 'project = "VIDEO" AND "Document ID[Number]" = ' + videoDocID
        
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
        print(response)

        data = json.loads(response.text)
        issues = data['issues']
        lenghtIssues = len(issues)
        if lenghtIssues > 0:
            tagData = data['issues'][0]['fields']['customfield_13794']
            idData = data['issues'][0]['id']
            keyData = data['issues'][0]['key']
            issueTypeData = data['issues'][0]['fields']['issuetype']['name']
            sumData = data['issues'][0]['fields']['customfield_13212']
            if tagData == None:
                totalTagData = newTags
            else:
                totalTagData = tagData + ", " + newTags
            data = ['Afghanistan', 652090, 'AF', 'AFG']
            csv_line = [ sumData, keyData, idData, issueTypeData, totalTagData, 'On Hold (migrated)' ]
            print(csv_line)
            importCSV = open(csv_path, 'a', encoding='UTF8')
            writer = csv.writer(importCSV)
            writer.writerow(csv_line)
            importCSV.close()

        else:
            print('Doc ID Not Foudn in Jira')
            badDocID = open(filePath, "a")
            badDocID.write(videoDocID)
            badDocID.write(', ')
            badDocID.close()

        # print(data['issues'][0]['fields']['customfield_13794'])

        # with open(artifact, 'w') as outfile:
        #     json.dump(json.loads(response.text), outfile)


