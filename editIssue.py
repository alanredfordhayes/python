
from typing import TYPE_CHECKING
import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import os
import time

url = "https://dotdash.atlassian.net/rest/api/3/search"

email = input("email address of admin user: ")
api_token = input("api_token of admin user: ")
auth = HTTPBasicAuth(email, api_token)

csv_name = '/Users/ahayes/Documents/code/powershell/import12.csv'
csv_path = "/Users/ahayes/Downloads/import.csv"
csv_header = ['Summary', 'Issue key', 'Issue id', 'Issue Type', 'Status', 'Parent id']

importCSV = open(csv_path, 'w', encoding='UTF8')
writer = csv.writer(importCSV)
writer.writerow(csv_header)
importCSV.close()

with open(csv_name, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        headers = {"Accept": "application/json"}
        childkey = row['jira_key']
        parentKey = row['parent_key']

        childJqlQuery = 'project = "VIDEO" AND key = ' + childkey
        childQuery = {'jql': childJqlQuery}
        childResponse = requests.request(
        "GET",
        url,
        headers=headers,
        params=childQuery,
        auth=auth
        )
        childData = json.loads(childResponse.text)
        if len(parentKey) == 0:
            parentID = None
        else:
            parentJqlQuery = 'project = "VIDEO" AND key = ' + parentKey
            parentQuery = {'jql': parentJqlQuery}
            parentResponse = requests.request(
            "GET",
            url,
            headers=headers,
            params=parentQuery,
            auth=auth
            )
            parentData = json.loads(parentResponse.text)
            parentID = parentData['issues'][0]['id']

        issueID = childData['issues'][0]['id']
        issueKey = childData['issues'][0]['key']
        issueType = childData['issues'][0]['fields']['issuetype']['name']
        summary = childData['issues'][0]['fields']['summary']
        status = childData['issues'][0]['fields']['status']['name']

        csv_line = [ summary, issueKey, issueID, issueType, status, parentID ]
        print(csv_line)

        importCSV = open(csv_path, 'a', encoding='UTF8')
        writer = csv.writer(importCSV)
        writer.writerow(csv_line)
        importCSV.close()