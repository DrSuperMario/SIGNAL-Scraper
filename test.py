import asyncio
from datetime import datetime


from modules.dataCollector import Connect
from connection.var import *
from db import createDb
from smtp import send_email


TIME_LOOP = True
time_passage = 12000
date_as = str(datetime.now())

conn5 = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'])

conn5.to_html('test.html')