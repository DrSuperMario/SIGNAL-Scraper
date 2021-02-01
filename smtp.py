from smtplib import SMTPAuthenticationError, SMTP_SSL , ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from connection.var import *

import logging

"""
Module for email logging

send_email() - email sending main function

Params:

    messages - message body to send
    subject - subject of the emal
    password - password for the SMTP server
    
"""

def send_email(messages, subject, password):
    
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = RECIVER_EMAIL
    message['Subject'] = subject

    part = MIMEText(messages, "plain")

    message.attach(part)

    context = ssl.create_default_context()

    try:
        with SMTP_SSL(SMTP_SERVER, EMAIL_PORT, context=context) as server:
            server.login(SENDER_EMAIL, password)
            server.sendmail(SENDER_EMAIL, RECIVER_EMAIL, message.as_string())
    except SMTPAuthenticationError as smt:
        logging.error("ERROR E-Mail not sent, logging error " + str(smt.__repr__))