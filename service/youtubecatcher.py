import logging
import re
import urllib2
#from pocket.articleparser import ArticleParser

__author__ = 'mora'


def find_urls(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()
    print data
    return re.findall('[http[s]?:]?//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)

def parse_youtube_url(url):
    url = url.replace('feature=player_embedded&', '')
    regexp = (
        r'((http(s)?:)?//)?(www\.|m\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)([^&=%\?]{11})')
    match = re.match(regexp, url, re.IGNORECASE)
    if match and match.group(6):
        return match.group(6)
        logging.error('Url ok: ' + url)
#    else:
#        logging.error('problems with this video url: ' + url)



if __name__ == '__main__':
    vids = []
    #url = 'http://www.hipersonica.com/monograficos/black-sabbath-heaven-and-hell-a-grandes-males-grandes-remedios'
    url = 'http://www.mondosonoro.com/Noticia/Wire-en-16-canciones/227554.aspx'
    for u in find_urls(url):
        a = parse_youtube_url(u)
        if a:
            vids.append(a)
    print vids

#    print ArticleParser().parse_youtube_url("http://plus.google.com/u/0/104460920643790249554?rel=author")
#    print ArticleParser().parse_youtube_url("http://www.youtube.com/watch?v=-wtIMTCHWuI")
#    print ArticleParser().parse_youtube_url("http://www.youtube.com/v/-wtIMTCHWuI?version=3&autohide=1")
#    print ArticleParser().parse_youtube_url("http://youtu.be/-wtIMTCHWuI")
#    print ArticleParser().parse_youtube_url("Youtu.be/c6K9P58Yf7E")
#    print ArticleParser().parse_youtube_url('http://m.youtube.com/#/watch?v=od7GUy9XS7c&desktop_uri=%2Fwatch%3Fv%3Dod7GUy9XS7c&gl=ES')
