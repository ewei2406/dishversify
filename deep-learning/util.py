import base64
import re
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError


def validate_email(email: str) -> bool:
    """Check if the email is valid."""
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.search(regex, email):
        return True
    else:
        return False
    

def send_email_with_pdf(email_address: str, pdf_path: str):
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
    flow = InstalledAppFlow.from_client_secrets_file('data/mail_credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    service = build('gmail', 'v1', credentials=creds)
    
    msg = MIMEMultipart()
    msg['to'] = email_address
    msg['subject'] = 'Email Subject'
    
    text = MIMEText('This is the body of the email')
    msg.attach(text)
    
    # Attach PDF file
    with open(pdf_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=str("report.pdf"))
        msg.attach(attach)
    
    # Base 64 encode the message
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    raw_message = {'raw': raw}
    
    try:
        message = (service.users().messages().send(userId="me", body=raw_message).execute())
        print(f'Sent message to {email_address}, Message Id: {message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')
    # from_email = "no.reply.smartoh@gmail.com"
    # from_password = "unbqfubrpqcwyugu"
    # # from_password = "eqafrqnzlbwmhhzr"

    # to_email = email_address
    # subject = "Your Session Report"

    # msg = MIMEMultipart()
    # msg['From'] = from_email
    # msg['To'] = to_email
    # msg['Subject'] = subject

    # body = "Please find attached your session report."
    # msg.attach(MIMEText(body, 'plain'))

    # with open(pdf_path, "rb") as f:
    #     attach = MIMEApplication(f.read(), _subtype="pdf")
    #     attach.add_header('Content-Disposition', 'attachment', filename=str("report.pdf"))
    #     msg.attach(attach)

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login(from_email, from_password)
    # server.sendmail(from_email, to_email, msg.as_string())
    # server.quit()