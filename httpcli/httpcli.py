import json
import logging
import urllib2
import urllib
from urllib2 import HTTPError


def doPost(url, params):
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data.encode('UTF-8'))
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Accept', 'application/json')

    try:
        response = urllib2.urlopen(req)
        logging.info("HTTP Status Code: " + str(response.getcode()))
        responseData = response.read()
    except HTTPError, e:
        error_message = e.headers['x-error']
        logging.error(error_message)
        raise e

    return responseData

#'16843-7517fa2d71db64499739fd22'
#'http://pocketapp1234.authorizationFinished.com'
def doRequest(consumer_key, redirect_uri):
    page = doPost("https://getpocket.com/v3/oauth/request",
                  {'consumer_key': consumer_key, 'redirect_uri': redirect_uri})
    print page
    code = json.loads(page)['code']
    return code

#browser
def getLoginUrl(redirect_uri, code):
    uri = 'https://getpocket.com/auth/authorize?request_token={code}&redirect_uri={redirect_uri}'.format(
        code=code, redirect_uri=redirect_uri)
    print uri
    return uri


def doAuthorize(consumer_key, code):
    logging.debug("doAuthorize with: " +  str(consumer_key) + " - " + str(code))
    page = doPost("https://getpocket.com/v3/oauth/authorize",
                  {'consumer_key': consumer_key,
                   'code': code})
    print page
    json_data = json.loads(page)
    access_token = json_data['access_token']
    username = json_data['username']
    return (access_token, username)


#redirectUri = 'http://localhost:9080/do-callback'
##redirectUri = 'http://pocketapp1234.authorizationFinished.com'
#consumerKey = '16843-7517fa2d71db64499739fd22'
#code = ''

#code = doRequest(consumerKey, redirectUri)
#print code
#url = getLoginUrl(redirectUri, code)
#print url
#
#raw_input('pulse')
#
#accessToken = doAuthorize(consumerKey, code)
#print accessToken
#exit(0)
