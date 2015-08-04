import collections
import logging
import json
from datetime import date


class ArticleParser:
    #TODO refactor
    def get_json_data(self, article, item_id, video_ids):
        return {
            'item_id': item_id,
            'video_ids': video_ids,
            'url': article['resolved_url'],
            'resolved_title': article['resolved_title'],
            # 'excerpt': article['excerpt'],
            'time_added': str(date.fromtimestamp(float(article['time_added']))),
            'time_updated': str(date.fromtimestamp(float(article['time_updated']))),
            'total_videos': str(len(video_ids))
        }

    def add_videoid_and_info(self, article, videos):

        item_id = article['item_id']
        article['resolved_id']

        #is a video has_video == 2
        #contains videos has_video == 1

        if 'videos' in article:
            vids_in_article = article['videos']
            #functional programming -
            video_ids = [vids_in_article[x]['vid'] for x in vids_in_article if 'youtube' in vids_in_article[x]['src']]
            videos.append(
                self.get_json_data(article, item_id, video_ids))

    def get_videos(self, data):
        jsonData = json.loads(data, object_pairs_hook=collections.OrderedDict)
        articleList = jsonData['list']
        logging.info('no articles with videos: ' + str(len(articleList.keys())))
        videos = []
        for x in articleList.keys():
            article = articleList[x]
            url = article['resolved_url']
            hasVideo = 'has_video' in article
            #2 is a video, 1 has videos in it
            if hasVideo and article['has_video'] != '0':
                self.add_videoid_and_info(article, videos)
                #addVideoId(url, videos)
        return videos

    def get_video_articles(self, data):
        return self.get_videos(data)


    def getVideoAndInfo(data):
        return None

def extracts_vids():

    json = [ { "video_ids": [ "PNu_-deVemE" ], "time_added": "2014-03-24", "time_updated": "2014-03-24", "total_videos": "1", "item_id": "576844317", "resolved_title": "Lady Gaga en el v\u00eddeo de G.U.Y.: por el camino del exceso", "url": "http://www.hipersonica.com/videos/lady-gaga-en-el-video-de-g-u-y-por-el-camino-del-exceso?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+hipersonica+%28Hipers%C3%B3nica%29" }, { "video_ids": [ "Zq40vTdaa2w", "iZZUY32iCzU" ], "time_added": "2014-03-24", "time_updated": "2014-03-24", "total_videos": "2", "item_id": "576939981", "resolved_title": "Turn Blue es el nuevo disco de The Black Keys y Fever su primer single: lo bailar\u00e1 hasta Mike Tyson", "url": "http://www.hipersonica.com/adelantos-y-mp3/turn-blue-es-el-nuevo-disco-de-the-black-keys-y-fever-su-primer-single-lo-bailara-hasta-mike-tyson" }]

    articles = json
    #[x for b in a for x in b]


vec = [[1,2,3], [4,5,6], [7,8,9]]
print [num for elem in vec for num in elem]

print extracts_vids()

