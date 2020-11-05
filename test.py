import asyncio
from datetime import datetime


from modules.dataCollector import Connect
from connection.var import *
from db import createDb
from smtp import send_email


TIME_LOOP = True
time_passage = 12000
date_as = str(datetime.now())
passwd = '<BLANK>'

conn = Connect.news(url=URL[4],header=HEADERS['agent_desktop'],reqToSend=True)
print(conn)