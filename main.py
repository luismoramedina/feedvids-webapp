#!/usr/bin/env python
import mimetypes
import logging
import os
import json
import os

from paste.urlparser import StaticURLParser
from paste.cascade import Cascade
import webapp2
import jinja2

from httpcli import httpcli
from pocket import pocketcli
from pocket.articleparser import ArticleParser
from service import accesstokenservice, userservice, cookieservice, youtubecatcher


template_dir = os.path.join(os.path.dirname(__file__), './views/')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=False)

logging.error(os.environ)

app_uri = 'http://feedvids.herokuapp.com/'
if 'ENVIRONMENT' in os.environ and os.environ['ENVIRONMENT'].startswith('Dev'):
    print 'We are developing...'
    #app_uri = 'http://localhost:5000/'
    app_uri = 'http://localhost:8080/'
else:
    print 'WE ARE ON PRODUCTION'

redirect_uri = app_uri + 'do-callback' + '?post_redirect='

consumer_key = os.environ['CONSUMER_KEY']
code = ''


class Handler(webapp2.RequestHandler):
    # *a is a list of parameters
    # **kw 
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_logged(self, template, **kw):
        user = None
        try:
            user = userservice.get_logged_username(self.request)
        except Exception:
            logging.debug(Exception.message)

        #TODO cache login url and logout url for each page
        login_url = userservice.get_login_url(self.request.uri)
        logout_url = userservice.get_logout_url(self.request.uri)

        kw['user'] = user
        kw['logout_url'] = logout_url
        kw['login_url'] = login_url
        logging.info('user: ' + str(user))
        return self.write(self.render_str(template, **kw))


class LoginHandler(Handler):

    def get(self):
        username = userservice.get_logged_username(self.request)

        if username:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Hello, ' + username)
        else:
            logging.info("uri: " + self.request.uri)
            login_url = userservice.get_login_url(self.request.uri)
            self.redirect(login_url)


class LogoutHandler(Handler):

    def get(self):
        self.response.set_cookie('user', '', path='/')
        self.redirect(self.request.get('post_redirect'))


class PlaylistHandler(Handler):
    """From form"""

    def get(self):
        vids = self.request.get("vids")
        logging.info('vids:' + vids)
        vids = vids.split(",")
        logging.info('vids json:' + json.dumps(vids))
        self.render("youtube.html", vids=json.dumps(vids))


class PocketOAuthCallbackHandler(Handler):
    def post(self):
        self.response.write(code)

    def get(self):
        logging.debug('get -> %s' % code)
        (access_token, pocket_user) = httpcli.doAuthorize(consumer_key, code)

        logging.info('pocket_user %s' % pocket_user)
        logging.info('access_token %s' % access_token)
        logging.info('nickname %s' % pocket_user)


        accesstokenservice.put_token(username=pocket_user, access_token=access_token, service='pocket')
#        self.write('pu: ' + pocket_user + ', a: ' + access_token)


        logging.info("Saved access_token on datastore" + access_token)
        self.response.set_cookie('user', cookieservice.get_cookie(pocket_user), path='/')
        self.redirect(self.request.get('post_redirect'))


def get_video_list(access_token):
    articles = get_video_articles(access_token)
    vids = [x['video_ids'] for x in articles]
    vids = [x for y in vids for x in y]
    return vids


def get_video_articles(access_token):
    data = pocketcli.retrieve(consumer_key, access_token)
    article_parser = ArticleParser()
    videos = article_parser.get_video_articles(data)
    return videos


class CastHandler(Handler):
    def get(self):
        access_token = accesstokenservice.get_token(userservice.get_logged_username(self.request))
        if access_token:
            self.render("./cast/feedvids-cast-sender.html", vids=json.dumps(get_video_list(access_token)))
        else:
            self.write('No token')


class PocketVideoListJsonHandler(Handler):
    """From pocket to JSON"""

    def get(self):
        access_token = accesstokenservice.get_token(userservice.get_logged_username(self.request))
        if access_token:
            if self.request.get('list'):
                json_vids = get_video_list(access_token)
                self.write(json_vids)
            else:
                self.write(json.dumps(get_video_articles(access_token), indent=3))
        else:
            self.write('No token')


class PocketDeleteHandler(Handler):
    def get_logged_token(self):
        return accesstokenservice.get_token(userservice.get_logged_username(self.request))

    def get(self):
        item = self.request.get("item")
        pocketcli.delete(consumer_key, self.get_logged_token(), item)


class PocketArchiveHandler(PocketDeleteHandler):
    def get(self):
        item = self.request.get("item")
        pocketcli.archive(consumer_key, self.get_logged_token(), item)


class PocketPlaylistHandler(PocketVideoListJsonHandler):
    """From pocket to player"""

    def get(self):
        access_token = accesstokenservice.get_token(userservice.get_logged_username(self.request))

        if access_token:
            videos = get_video_articles(access_token)
            vids_for_cast = get_video_list(access_token)
            offset = None
            if self.request.get('offset'):
                logging.info('we got offset')
                offset = self.request.get('offset')

                #TODO create a function

            self.render_logged(
                "youtube.html",
                vids=json.dumps(videos),
                vids_for_cast=json.dumps(vids_for_cast),
                offset=offset)
        else:
            #TODO pass parameter to redirect to
            self.redirect('/do-pocket-oauth2' + '?post_redirect=' + '/pocket-playlist')


class PocketOAuthHandler(Handler):
    """Get access token from pocket"""

    def get(self):
        #user must be logged with google credentials
        user = userservice.get_logged_username(self.request)

        global code
        redirect_uri_redirect = redirect_uri + self.request.get('post_redirect')
        code = httpcli.doRequest(consumer_key, redirect_uri_redirect)
        logging.info('code: ' + code)

        login_url = httpcli.getLoginUrl(redirect_uri_redirect, code)

        logging.info('login_url: ' + login_url)

        return self.redirect(login_url)


class IndexHandler(Handler):
    def get(self):
        self.render_logged("main.html")

class AboutHandler(Handler):
    def get(self):
        self.render_logged("about.html")


class FormHandler(Handler):
    def get(self):
        self.render("form.html")


class TestHandler(Handler):
    def get(self):
        self.render("test-info.html")

class WebpageVidCatcherHandler(Handler):
    def get(self):
        url = self.request.get('url')
        print url
        if url:
            urls = youtubecatcher.find_urls(url)

            vids = [{'url': url, 'video_ids': [], 'resolved_title': ''}]
            for u in urls:
                vid = youtubecatcher.parse_youtube_url(u)
                if vid:
                    vids[0]['video_ids'].append(vid)

            self.render_logged("youtube.html", vids=json.dumps(vids))
            #self.write(vids)
        else:
            self.render_logged('form.html')


class StaticView(webapp2.RequestHandler):
    def get(self, path):
        print path
        path = path.replace('/', os.sep)
        path = 'static' + os.sep  + path
        print path
        try:
            f = open(path, 'r')
            self.response.headers.__delitem__('Content-Type')
            if path.endswith('svg'):
                self.response.headers.add_header('Content-Type', 'image/svg+xml')
            else:
                self.response.headers.add_header('Content-Type', mimetypes.guess_type(path)[0])
            self.response.out.write(f.read())
            f.close()
        except Exception, e:
            print 'Problem in StaticView:', e
            self.response.set_status(404)


web_app = webapp2.WSGIApplication(
    [
        ('/login', LoginHandler),
        ('/logout', LogoutHandler),
        ('/pocket-json-list', PocketVideoListJsonHandler),
        ('/do-playlist', PlaylistHandler),
        ('/pocket-playlist', PocketPlaylistHandler),
        ('/pocket/delete', PocketDeleteHandler),
        ('/pocket/archive', PocketArchiveHandler),
        ('/do-callback', PocketOAuthCallbackHandler),
        ('/do-pocket-oauth2', PocketOAuthHandler),
        ('/scrap', WebpageVidCatcherHandler),
        ('/', IndexHandler),
        ('/form', FormHandler),
        ('/test', TestHandler),
        ('/cast', CastHandler),
        ('/static/(.+)', StaticView),
        ('/about', AboutHandler)

    ], debug=True)

# Create an app to serve static files
# Choose a directory separate from your source (e.g., "static/") so it isn't dl'able
static_app = StaticURLParser("static/")

# Create a cascade that looks for static files first, then tries the webapp
app = Cascade([static_app, web_app])

#f_app = Flask(__name__)

def main():
    from paste import httpserver
    httpserver.serve(web_app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()