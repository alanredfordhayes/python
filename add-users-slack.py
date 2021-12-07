import logging
import os
import csv
from slack_sdk import WebClient

#Logging
logging.basicConfig(level=logging.DEBUG)

#Get Slack Users data
slack_token = os.environ["SLACK_TOKEN"]
client = WebClient(token=slack_token)
response_1 = client.users_list()
response_2 = client.users_list(cursor = 'dXNlcjpVRTJBQThBSjA=')
response_3 = client.users_list(cursor = 'dXNlcjpVMDFRQUJCVFQ0Rw==')
responses = [ response_1, response_2, response_3 ]

#Where the CSV will be saved
csv_path = "c:\\exports\slack\slack_export.csv"
csv_header = ['id', 'email']

#Open CSV and write the header
importCSV = open(csv_path, 'w', encoding='UTF8')
writer = csv.writer(importCSV)
writer.writerow(csv_header)
importCSV.close()

for response in responses:
    data = response.data

    #Filter data and loop through users
    users = data['members']
    for user in users:
        member_id = user['id']
        profile = user['profile']
        try:
            email = user['profile']['email']
        except KeyError:
            email = "Not Found"
        
        #Format row for csv and write it
        csv_line = [ member_id, email ]
        importCSV = open(csv_path, 'a', encoding='UTF8')
        writer = csv.writer(importCSV)
        writer.writerow(csv_line)
        importCSV.close()