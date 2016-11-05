from pocket.articleparser import ArticleParser
from pocket.pocketcli import delete
from pocket.pocketcli import retrieve

__author__ = 'mora'


def main():
    #f = open('c:/Users/xIS16578/Dropbox/test_get_pocket.txt', 'r')
    #f = open('/Users/mora/Dropbox/yuvids/test_get_pocket.txt', 'r')
    #data = f.read()

    access_token = 'dbdf64ab-40af-b04d-e454-d37e8f'
    consumer = '20429-a9fccf51b4b023714d2a5409'
#    access_token = 'aa'
#    consumer = 'aaa'

    #print archive(consumer, access_token, 471013191)
    print delete(consumer, access_token, 1111111111)
    data = retrieve(consumer, access_token)
    articleparser = ArticleParser()
    videos = articleparser.get_videos(data)
    print videos
    v2 = [x['url'] for x in videos]
    for v in v2:
        print v
    #print json.dumps(videos, indent=3)

main()

