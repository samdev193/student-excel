# student-excel
 
student-excel is a mailing list app that is meant to work with google sheets geared towards people that may be running a class where payment is needed. 
It uses the googlesheets API and a web-accessible REST API that was built to work directly with the program. 

# Required

excel sheet must have the parameters "FIRST NAME", "LAST NAME", "EMAIL" "AMOUNT" and "PAID" in order for the mailing list to work properly. 

The app starts looking 1 row beneath the month name you choose to input, so if you have a cell that says "June" the app will assume all relevant information is below that cell.

A .env is required listing your email username and password in the variables "EMAIL_USERNAME", "EMAIL_PASSWORD" so that the students can be emailed.
You'll also need to allow 2 factor authentication if you use gmail and generate an app password.

Lastly you'll need to use the google sheets and google drive api in cloud google console and get the json file with your credentials from the cloud console.
Name the file "creds.json" and you should be ready to use the app. 