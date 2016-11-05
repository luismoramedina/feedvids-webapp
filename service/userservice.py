from service import cookieservice

__author__ = 'mora'

def get_logged_username(request):
    cookie = request.cookies.get('user')
    if cookieservice.check_cookie(cookie):
        return cookieservice.get_user(cookie)

def get_login_url(uri):
    return '/do-pocket-oauth2' + '?post_redirect=' + uri
    #return users.create_login_url(uri)

def get_logout_url(uri):
    return 'logout?post_redirect=' + uri
    #return users.create_logout_url(uri)