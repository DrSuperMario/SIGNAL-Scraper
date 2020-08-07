from smtplib import SMTP_SSL , ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(messages, subject, password):
    port = 465
    smtp_server = 'pythonslack.com'
    sender_mail = 'brine@pythonslack.com'
    reciver_mail = 'mario@pythonslack.com'
    
    message = MIMEMultipart()
    message['From'] = sender_mail
    message['To'] = reciver_mail
    message['Subject'] = subject

    part = MIMEText(messages, "plain")

    message.attach(part)

    context = ssl.create_default_context()

    with SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_mail, password)
        server.sendmail(sender_mail, reciver_mail, message.as_string())