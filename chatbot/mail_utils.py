import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def envoyer_email(destinataire, sujet, corps):
    host = os.getenv("MAIL_HOST")
    port = int(os.getenv("MAIL_PORT"))
    user = os.getenv("MAIL_USERNAME")
    pwd = os.getenv("MAIL_PASSWORD")
    mail_from = os.getenv("MAIL_FROM")

    msg = MIMEText(corps)
    msg['Subject'] = sujet
    msg['From'] = mail_from
    msg['To'] = destinataire

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, pwd)
        server.sendmail(mail_from, [destinataire], msg.as_string())
