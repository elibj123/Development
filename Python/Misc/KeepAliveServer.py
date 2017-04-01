from flask import Flask, url_for;
import smtplib
import thread;
import threading;
import time;
import datetime;
import logging

# logging.basicConfig(filename='KeepAliverServer.log',level=logging.DEBUG)

timeLock = threading.Lock();
mailSentLock = threading.Lock();

lastUpdateTime = int(time.time());
mailSent = 0;

webServer = Flask('KeepAliveServer');

@webServer.route('/keepalive')
def api_keepalive():
	global timeLock
	global lastUpdateTime
	global mailSentLock
	global mailSent
	timeLock.acquire();
	lastUpdateTime = int(time.time());
	timeLock.release();
	
	mailSentLock.acquire();
	mailSent = 0;
	mailSentLock.release();
	# logging.info("[%s] New keep alive" % datetime.datetime.now())
	print "[%s] New keep alive" % datetime.datetime.now();
	return '{"status":"ok"}';

class timeCheckThread (threading.Thread):
    def __init__(self):
		threading.Thread.__init__(self);
		# logging.info("[%s] Time check thread initiated" % datetime.datetime.now());
		print "[%s] Time check thread initiated" % datetime.datetime.now();
		self.counter = 0;
    def run(self):
		global lastUpdateTime
		global mailSent
		global timeLock
		global mailSentLock
		global webServer
		
		while (1):
			time.sleep(60);
			self.counter = self.counter + 1;
			# logging.info("[%s] time check number %s" % (datetime.datetime.now(), self.counter));
			print "[%s] time check number %s" % (datetime.datetime.now(), self.counter);
			timeLock.acquire();
			delta = int(time.time()) - lastUpdateTime;
			timeLock.release();
			
			mailSentLock.acquire();
			mailSentTemp = mailSent;
			mailSentLock.release();
			if delta > 10*60 and mailSentTemp == 0:
				# logging.info("[%s] Failed to received keep alive, sending mail to ziyunim" % datetime.datetime.now());
				print "[%s] Failed to received keep alive, sending mail to ziyunim" % datetime.datetime.now()
				fromaddr = 'chotamzayan@gmail.com'
				toaddrs  = ['elibj123@gmail.com','cyberj19@gmail.com','godslay666@gmail.com','pinsker14@gmail.com']
				msg = "\r\n".join([
				  "Subject: Cam Control Server Crash",
				  "",
				  "Cam control server crash - haven't received a keep alive in 10 minutes"
				])
				# Credentials (if needed)
				username = 'chotamzayan@gmail.com'
				password = 'zayanim669'

				# The actual mail send
				mailServer = smtplib.SMTP('smtp.gmail.com:587');
				mailServer.starttls()
				mailServer.login(username,password)
				mailServer.sendmail(fromaddr, toaddrs, msg)
				mailServer.quit()
				
				mailSentLock.acquire();
				mailSent = 1;
				mailSentLock.release();

class webServerThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self);
	def run(self):
		webServer.run(host = '192.168.1.16', port = 5050);

# logging.info("[%s] Keep alive server starting" % datetime.datetime.now());
print "[%s] Keep alive server starting" % datetime.datetime.now()
webServerThread().start();
timeCheckThread().start();



