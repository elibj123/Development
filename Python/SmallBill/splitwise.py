from config import Config
import oauth2
import webbrowser
from urlparse import parse_qsl
from urllib import urlencode
import requests
import json
import time


def _get_authorize_url(oauth_consumer):
    oauth_client = oauth2.Client(oauth_consumer)
    resp, content = oauth_client.request(Config.Splitwise.URLS.request_token, 'POST')

    if resp['status'] != '200':
        raise Exception("Invalid response %s. Please check your consumer key and secret." % resp['status'])

    request_token = dict(parse_qsl(content.decode("utf-8")))

    authorize_url = "%s?oauth_token=%s" % (Config.Splitwise.URLS.authorize, request_token['oauth_token'])
    return authorize_url, request_token['oauth_token_secret']


def _get_access_token(oauth_consumer, token, secret, verifier):
    token = oauth2.Token(token, secret)
    token.set_verifier(verifier)
    client = oauth2.Client(oauth_consumer, token)

    resp, content = client.request(Config.Splitwise.URLS.get_access_token, "POST")

    # Check if the response is correct
    if resp['status'] != '200':
        raise Exception("Invalid response %s. Please check your consumer key and secret." % resp['status'])

    access_token = dict(parse_qsl(content.decode("utf-8")))

    return access_token


def _get_auth_from_gtw():
    attempt_count = 0
    while 1:
        attempt_count += 1
        print 'Attempting to access authorization gateway #%d' % attempt_count
        response = requests.get(Config.AuthGtw.url)
        response_json = json.loads(response.content)
        if response_json['success'] == 'true':
            return response_json['token'], response_json['verifier']
        time.sleep(Config.AuthGtw.poll_interval)


def _expense_dict(amount):
    expense = dict()
    expense['payment'] = 'lol'
    expense['cost'] = str(amount)
    expense['description'] = 'lal'
    return expense


def _get_oauth_client():

    # driver = webdriver.Chrome(config['CHROME_DRIVER_PATH'])
    # driver.get(authorize_url)

    # time.sleep(30)
    # username_element = driver.find_element_by_name('user_session[email]')
    # username_element.clear()
    # username_element.send_keys("elibj123@gmail.com")

    # password_element = driver.find_element_by_name('user_session[password]')
    # password_element.clear()
    # password_element.send_keys("gr,lyj5gr,lyj5")

    # login_element = driver.find_element_by_name('commit')
    # login_element.click()
    # element = driver.find_element_by_class_name('large btn primary')
    # element.click()

    oauth_consumer = oauth2.Consumer(key=Config.Splitwise.Creds.key, secret=Config.Splitwise.Creds.secret)
    authorize_url, secret = _get_authorize_url(oauth_consumer)
    webbrowser.open(authorize_url, new=2)
    token, verifier = _get_auth_from_gtw()
    access_token = _get_access_token(oauth_consumer, token, secret, verifier)
    oauth_token = oauth2.Token(key=access_token["oauth_token"], secret=access_token["oauth_token_secret"])
    oauth_client = oauth2.Client(oauth_consumer, oauth_token)

    return oauth_client


def create_splitwise_expense(amount):
    print 'Updating splitwise...'
    expense = _expense_dict(amount)
    oauth_client = _get_oauth_client()
    resp, content = oauth_client.request(Config.Splitwise.URLS.create_expense, 'POST', body=urlencode(expense))
    if resp['status'] != '200':
        raise Exception("Invalid response %s. Please check your consumer key and secret." % resp['status'])
    print content
