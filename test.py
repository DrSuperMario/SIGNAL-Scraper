from modules.dataCollector import Connect
from connection.var import *
from db import createDb
from smtp import send_email

#newConnection = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'])
"""
newConnection = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'])
#secondConnection = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'])
#thirdConnection = Connect.forex(url=URL[6], header=HEADERS['agent_desktop'])

print(newConnection)
#print(secondConnection)
#print(thirdConnection)
newsConn, dbName = createDb("newsTable")  
newConnection.to_sql(dbName, newsConn, if_exists='append')
newsConn.close()"""
send_email(messages='Information Collected Crypto', subject="asd", password='Haxx0r001')
