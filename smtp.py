from smtplib import SMTPAuthenticationError, SMTP_SSL , ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging
import os 

logging.basicConfig(filename=os.path.normpath('log/scraper.log'))


def send_email(messages, subject, password):
    port = 465
    smtp_server = 'smtp.gmail.com'
    sender_mail = 'muukmario@gmail.com'
    reciver_mail = 'mario@pythonslack.com'
    
    message = MIMEMultipart()
    message['From'] = sender_mail
    message['To'] = reciver_mail
    message['Subject'] = subject

    part = MIMEText(messages, "plain")

    message.attach(part)

    context = ssl.create_default_context()

    try:
        with SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_mail, password)
            server.sendmail(sender_mail, reciver_mail, message.as_string())
    except SMTPAuthenticationError:
        logging.error(f"{str(datetime.now())} E-Mail no sent, logging error")