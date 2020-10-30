from modules.dataCollector import Connect
from connection.var import *


#newConnection = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'])

newConnection = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'])
secondConnection = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'])
thirdConnection = Connect.forex(url=URL[6], header=HEADERS['agent_desktop'])

print(newConnection)
print(secondConnection)
print(thirdConnection)