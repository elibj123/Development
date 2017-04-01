import requests;
import time;

while (1):
	time.sleep(2.5*60);
	response = requests.get("192.168.1.16:5050/keepalive");
	print response.text;
	print "new keep alive dispatched";