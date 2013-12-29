from suds.client import Client
url = 'http://192.168.178.37:57605/fc6593d6-09ef-421a-9176-5497769db627.xml'
client = Client(url)
print client
