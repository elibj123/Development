import requests

base_api_url = 'http://192.168.1.20:3000/api/v1'
rocket_chat_host = '192.168.1.20'
rocket_chat_port = 3000
rocket_chat_api_base = '/api/v1'


class UnknownRocketChatApiVersion(Exception):
    def __init__(self, ver):
        self.message = 'Unknown RocketChat API version ' + ver


class RocketChatFailedToLogin(Exception):
    def __init__(self, error):
        self.message = 'Failed to login: ' + error


class RocketChat(object):
    def __init__(self, host, port, ver):
        self.host = host
        self.port = port
        self.api_base = _get_api_base(ver)
        self.credentials = {}

    def _get_base_url(self):
        return self.host + ':' + self.port + self.api_base

    def login(self, username, password):
        login_url = self._get_base_url()
        response = requests.post(login_url, data={'username': username, 'password': password}).json()
        if response['status'] == 'error':
            raise RocketChatFailedToLogin(response['error'])
        else:
            self.credentials = {'UserId': response['data']['userId'],
                               'AuthToken': response['data']['authToken'],
                               'UserName': username,
                               'Password': password}

    def createChannel(self, channel_name, user_list=[]):
        return []

def rcCreateChannel(credentials, channel_name, user_list):
    req_url = 'http://192.168.1.20:3000/api/v1/channels.create'
    data = {'name': channel_name, 'members': user_list}
    return rcAuthorizedRequest('post', credentials, req_url, data, {}).json()


# def rcDeleteChannel(credentials, channelName):
# credentials = rcVerifyCredentials(credentials);
# reqUrl = 'http://192.168.1.20:3000/api/v1/channels.removeOwner';
# data = {'roomId':rcFindChannelIdByName(credentials,channelName), 'userId':credentials['userId']};
# return rcAuthorizedRequest('post',credentials,reqUrl,data,{}).json();


def rcGetChannelList(credentials):
    credentials = rcVerifyCredentials ( credentials );
    reqUrl = 'http://192.168.1.20:3000/api/v1/channels.list';
    return rcAuthorizedRequest ( 'get' , credentials , reqUrl , {} , {} ).json ( );


def rcFindChannelIdByName(credentials , channelName):
    credentials = rcVerifyCredentials ( credentials );
    channels = rcGetChannelList ( credentials );
    for channel in channels['channels']:
        if channel['name'] == channelName:
            return channel['_id'];
    return 0;


def rcAuthorizedRequest(method , credentials , reqUrl , reqData , reqHeaders):
    rcHeaders = {'X-Auth-Token': credentials['authToken'] , 'X-User-Id': credentials['userId']};
    rcHeaders.update ( reqHeaders );
    if method == 'get':
        return requests.get ( reqUrl , data=reqData , headers=rcHeaders );
    elif method == 'post':
        return requests.post ( reqUrl , data=reqData , headers=rcHeaders );
