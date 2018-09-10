import smtplib
from string import Template
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def sendemail(recipient, absencedict, periodnum):
    datetoday = str(date.today())

    f = open("/home/vishal/RFPresence/emailer/password.txt", 'r')
    txt = f.read().split()
    MY_ADDRESS = txt[0]
    PASSWORD = txt[1]
    f.close()

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    message_template = read_template('/home/vishal/RFPresence/emailer/messagetemplate.txt')
    absentstring = ""

    for i in absencedict:
        absentstring += absencedict[i] + " - ID #" + i + "\n"

    message = message_template.substitute(DATE=datetoday, PERIODNUM=periodnum, ABSENCES=absentstring)

    msg = MIMEMultipart()

    msg['From'] = MY_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = "People Absent " + datetoday + " in Period " + periodnum
    msg.attach(MIMEText(absentstring, 'plain'))

    s.send_message(msg)
    del msg
    s.quit()
