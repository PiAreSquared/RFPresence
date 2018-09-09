import gspread
import oauth2client.client
import time
import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from oauth2client import client
import time
from emailer.emailer import sendemail

JSON_FILENAME = 'client_secret.json'

# Google sheet to save to`
GSHEET_NAME = 'Attendance Sheet Test'
SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#load credentials from json and open the spreadsheet for writing
json_key = json.load(open(JSON_FILENAME))

creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, SCOPES)

client = gspread.authorize(creds)
log = client.open(GSHEET_NAME).get_worksheet(1)
log.clear()
names = client.open(GSHEET_NAME).sheet1

signedin = []
signedout = []
lastentry = [00000, 0]

row = 1
col = 1

studentnames = names.range("A4:A11")
ids = names.range("B4:B11")
students = {}
absentstudents = {}

for i in ids:
    students[i.value] = [studentnames[ids.index(i)].value, "nosign", None, 0]
    absentstudents[i.value] = studentnames[ids.index(i)].value

while True:
    try:
        id = input("ID Number: ")
        if id == "bash rfid.sh":
            raise KeyboardInterrupt
        if id == lastentry[0] and time.time() - lastentry[1] <= 15:
            continue
        if id in signedin:
            del signedin[signedin.index(id)]
            signedout.append(id)
            log.update_cell(row, col, id + " OUT")
            students[id][1] = "OUT"
            students[id][2] = time.time()
            row += 1
        elif id in signedout:
            signedin.append(id)
            log.update_cell(row, col, id + " IN")
            students[id][1] = "IN"
            students[id][3] = time.time() - students[id][2]
            row += 1
            students[id][2] = None
            log.update_cell(row, col, id + " TIMEOUT")
            log.update_cell(row, col+1, students[id][3])
            row += 1
        elif (id not in signedin and id not in signedout):
            signedin.append(id)
            log.update_cell(row, col, id + " IN")
            students[id][1] = "IN"
            del absentstudents[id]
            row += 1
        lastentry[0] = id
        lastentry[1] = time.time()
    except KeyboardInterrupt:
        print("Andy's coming! ANDY'S COMING!")
        break

sendemail("premgiridhar11@gmail.com", absentstudents, str(1))