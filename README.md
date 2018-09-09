# RFID Attendance and Student Sign-In/Out System

This is a project for our school to eliminate the need for manual attendance, by allowing students to scan RFID tags to enter. This allows more time for learning in the classroom and allows teachers to see students' data through Google Sheets integration.

Features:

* [x] Small box that works when plugged in(easy-to-setup)
* [x] Can sign a student in and out of class through scanning of RFID
  * [ ] Possible NFC implementation with smartphones
* [x] Emails the teacher with a list of absent students
  * [ ] Hopefully in the near future, will be able to make completely automatic with Q Connection integration
* [x] Can sign out/in with one touch(leaving class for water)
* [ ] Possile Siri implementation for teachers

Collaborators: Vishal M., Kishore H., Prem G.


# How does this work?

This works by having a Student ID card with an RFID chip or an RFID sticker. An RFID Reader will be connected to a RPi with software to read a write data. When the ID card touches the reader, the ID card sends the ID Number to the python program on the RPi. The python program will process the data and will change the status of the student accordingly(PRESENT, ABSENT, SIGNED OUT). At the end of the period, an email will be sent to the teacher with a list of absent people. Soon, the teacher will be able to click one button and submit the attendance automatically. A posile integration with Siri for teachers may occur where teachers can ask Siri, "Who is absent in Period 1" and Siri will read out a list of people who are absent for period 1.


# How can I implement this system in my school?

You have two choices in which you can implement this system in your school. You can either but the software and hardware from us, and use the step-by-step instructions below tp assist you while assembling the system, or we can assemble the entire system for you(reccomended option)*. For more details, please email limelightfhs@gmail.com. If you chose to assemble the system on your own, you should be able to see the step-by-step instructions below. 

1) Download the repository and unzip the folder to the RPi's home directory(/home/pi).
2) Open the goglesheetslinks.txt file and open both URL's. Make a copy of each file and delete the "Copy of " part. 
3) Create a google account for the system,create credentials for the Google Drive API and enable Sheets API
	1) Go to https://accounts.google.com/signup/v2/webcreateaccount?hl=en&flowName=GlifWebSignIn&flowEntry=SignUp
	2) Create a new project at https://console.cloud.google.com
	3) Enable Google Drive API and create credentials(download the json file)
	4) Now go back to the two sheets and share it with the service account that ends with ".iam.gserviceaccount.com".
	5) Enable Sheets API
4) Open sheetsigninout.py, and replace /path/to/credentials.json, with the path to credentials(json file) on Line 15. Save the file and close it.
5) Open sheetswriter.py, and replace /path/to/credentials with the path to credentials(json file) on Line 13. Save the file and close it.
6) Make sure you are on the latest software and have all the dependencies installed for the python program to run on the RPi.



*Why do we reccomend this option?
The reason is because we have experience with this system as we are the one who created it. It is easier for us to troubleshoot any issue that may occur during the installation and the testing of the system. 
