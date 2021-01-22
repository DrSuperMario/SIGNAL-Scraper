import asyncio
from datetime import datetime


from modules.dataCollector import Connect
from connection.var import *
from db import createDb
from smtp import send_email
from uuid import uuid4
import requests as req


TIME_LOOP = True
time_passage = 12000
date_as = str(datetime.now())

conn1 = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'], reqToSend=True, send_notification=False)
conn4 = Connect.news(url=URL[4],header=HEADERS['agent_desktop'], reqToSend=True, send_notification=False)
conn6 = Connect.forex(url=URL[6],header=HEADERS['agent_desktop'], reqToSend=True, send_notification=False)
conn9 = Connect.stock(url=URL[9],header=HEADERS['agent_desktop'], reqToSend=True, send_notification=False)
print(conn4)


