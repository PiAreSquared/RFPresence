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

def nar(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

def signOut(idnum):
    del signedin[signedin.index(idnum)]
    signedout.append(idnum)
    log.update_cell(row, col, idnum + " OUT")
    students[idnum][1] = "OUT"
    students[idnum][2] = time.time()
    return None

def signIn(idnum):
    signedin.append(idnum)
    log.update_cell(row, col, idnum + " IN")
    students[idnum][1] = "IN"
    students[idnum][3] = time.time() - students[id][2]
    row += 1
    students[idnum][2] = None
    log.update_cell(row, col, idnum + " TIMEOUT")
    log.update_cell(row, col+1, students[idnumum][3])

def firstSignIn(idnum):
    signedin.append(idnum)
    log.update_cell(row, col, idnum + " IN")
    students[idnum][1] = "IN"
    del absentstudents[idnum]

def absentStudents(absentlist, pernum):
    absentsheet.update_cell(int(nar(absentsheet)), 1, str(pernum))
    absentsheet.update_cell(int(nar(absentsheet))-1, 2, str(absentlist))

JSON_FILENAME = '/home/vishal/Downloads/RFID-b01812ec4010.json'

# Google sheet to save to`
GSHEET_NAME = 'Attendance Sheet'
SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#load credentials from json and open the spreadsheet for writing
json_key = json.load(open(JSON_FILENAME))

creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, SCOPES)

client = gspread.authorize(creds)
log = client.open(GSHEET_NAME).get_worksheet(1)
log.clear()
names = client.open(GSHEET_NAME).sheet1
absentsheet = client.open(GSHEET_NAME).get_worksheet(3)

signedin = []
signedout = []
lastentry = [00000, 0]

row = 1
col = 1
per=str(1)
timeout=15
pernum=str(int(per)+1)
period="Period "+pernum

studentnames = names.range("A3:A999")
ids = names.range("B3:B999")
students = {}
absentstudents = {}

for i in ids:
    students[i.value] = [studentnames[ids.index(i)].value, "nosign", None, 0]
for i in ids:
	if studentnames[ids.index(i)].value==period:
		break
	absentstudents[i.value] = studentnames[ids.index(i)].value

while True:
    try:
        valid = names.col_values(2)
        id = input("ID Number: ")
        if id == "bash rfid.sh":
            raise KeyboardInterrupt
        if id not in valid:
            print("Invalid ID")

        else:
            if id == lastentry[0] and time.time() - lastentry[1] <= timeout:
                continue
            if id in signedin:
                signOut(id)
                row += 1
            elif id in signedout:
                signIn(id)
                row += 1
            elif (id not in signedin and id not in signedout):
                firstSignIn(id)
                row += 1
            lastentry[0] = id
            lastentry[1] = time.time()
    except KeyboardInterrupt:
        print("\nAndy's coming! ANDY'S COMING!")
        break

sendemail("vishvib@gmail.com", absentstudents, per)
absentstring = ""
for i in absentstudents:
    absentstring += absentstudents[i] + "\n"
absentStudents(absentstring, per)
