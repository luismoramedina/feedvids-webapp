import logging
import hmac
import base64

__author__ = 'mora'


def get_cookie(username):
    hmac_new = hmac.new('my_very_private_key', username)
    digest = hmac_new.hexdigest()
    return base64.b64encode(username + '|' + digest)


def split_cookie(cookie):
    decoded_cookie = base64.b64decode(cookie)
    (username, hash_in_cookie) = decoded_cookie.split('|')
    return username, hash_in_cookie


def check_cookie(cookie):
    logging.debug('cookie: ' + str(cookie))
    if cookie:
        username, hash_in_cookie  = split_cookie(cookie)
        hmac_new = hmac.new('my_very_private_key', username).hexdigest()
        return hmac_new == hash_in_cookie
    else:
        return False

def get_user(cookie):
    if cookie:
        return split_cookie(cookie)[0]
    else:
        return None

if __name__ == '__main__':
    print get_cookie('luismoramedina')
    print get_cookie('moramorita')
    print get_cookie('test')
    print check_cookie(get_cookie('luismoramedina'))
    print get_user(get_cookie('luismoramedina'))


