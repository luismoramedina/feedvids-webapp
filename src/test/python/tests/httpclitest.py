#set http_proxy=xIS16578:******@172.31.219.20:8080
import urllib
#import urllib.parse
#import urllib.request
from urlparse import *

a = 'http://m.youtube.com/#/watch?v=od7GUy9XS7c&desktop_uri=%2Fwatch%3Fv%3Dod7GUy9XS7c&gl=ES'
data = urlparse(a, None, True)
data = parse_qs(data.query)
if data.has_key('v'):
    data['v']

data = urllib.parse.urlencode({'q' : 'hola'})
req = urllib.request.Request("http://www.google.com", data.encode('UTF-8'))
response = urllib.request.urlopen(req)
the_page = response.read()