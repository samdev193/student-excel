from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
import gspread
from typing import List, Dict, Tuple

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]
googleAPI = 'creds.json'
creds = service_account.Credentials.from_service_account_file(googleAPI)
scopedCreds = creds.with_scopes(scope)
# accesses google sheet
client = gspread.Client(auth=scopedCreds)
# opens it.
client.session = AuthorizedSession(scopedCreds)

from decouple import config


import requests


def email_student(subject: str, body: str, email_list: List[Tuple[str, str]]) -> List[str]:


    import smtplib

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    from_email = config('EMAIL_NAME')
    email_password = config('EMAIL_PASSWORD')
    error_list = []
    # gets student name and email
    for name, email in email_list:
        to_email = email

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        html = """
               <h4> Hello %s </h4>
                %s
              
            """ % (name, body)

        mime = MIMEText(html, 'html')
        msg.attach(mime)
        try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.ehlo()
            mail.login(from_email, email_password)
            mail.sendmail(from_email, to_email, msg.as_string())
            mail.quit()

        except Exception as e:
            error_list.append(to_email)

    return error_list

def get_students() -> Dict:

    all_students = requests.get("https://student-excel-api.herokuapp.com/students").json()
    student_dict = {}
    for student in all_students:
        student_name = student['first_name'] + " " + student['last_name']
        student_email = student['email']
        student_dict[student_name] = student_email
    return student_dict

def update_db(month: str, sheet_name: str):

    all_students = requests.get("https://student-excel-api.herokuapp.com/students")
    # clears db
    for student in all_students.json():
        requests.delete(f"https://student-excel-api.herokuapp.com/student/{student['id']}")

    try:
        sheet = client.open(sheet_name).sheet1
    except Exception as e:
        return False

    # gets all data in google sheet.
    data = sheet.get_values()
    cell = sheet.find(month)
    if cell is None:
        return False
    start = cell.row
    id = 0

    updating = True
    while id != '' and start < len(data):

        first_name_col = sheet.find('FIRST NAME').col - 1
        last_name_col = sheet.find("LAST NAME").col - 1
        email_col = sheet.find('EMAIL').col - 1
        amount_col = sheet.find('AMOUNT').col - 1
        paid_col = sheet.find('PAID').col - 1

        # ignores headers.
        if data[start][first_name_col] == 'FIRST NAME':
            start += 1

        id = data[start][0]
        fname = data[start][first_name_col]
        lname = data[start][last_name_col]
        email = data[start][email_col]
        tuition_paid = True
        tuition_cost = int(data[start][amount_col])
        student_paid = int(data[start][paid_col])

        if student_paid < tuition_cost:
            tuition_paid = False

        id = int(id)

        query = {
          "id": id,
          "first_name": fname,
          "last_name": lname,
          "email": email,
          "tuition_paid": tuition_paid
        }

        response = requests.post("https://student-excel-api.herokuapp.com/students", json=query)

        start += 1



# gets a list of students that haven't finished paying for class.
def students_not_paid() -> List[str]:
    all_students = requests.get("https://student-excel-api.herokuapp.com/students").json()
    target_students = []
    for student in all_students:
        if not student['tuition_paid']:
            name = student['first_name'] + " " + student['last_name']
            target_students.append(name)
    return target_students

