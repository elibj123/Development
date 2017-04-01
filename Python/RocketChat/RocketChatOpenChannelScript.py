import requests;
from rocketChatUtils import *


rc = RocketChat('192.168.1.20', 3000, 1)
rc.login('elibj123', 'gr,lyj5')
newChannelName = 'pythonChannel3';
userList = ['elibj123', 'cyberjake', 'arthur']
rc.createChannel(newChannelName, userList)
