import logging
import os
from httpcli.httpcli import doPost

__author__ = 'mora'


def retrieve(consumer_key, access_token):
    post_data = {'consumer_key': consumer_key,
                 'access_token': access_token,
                 'contentType': 'video',
                 'sort': 'newest',
                 'detailType': 'complete'}

    #TODO
    post_data['count'] = 100

    logging.info('Before doPost retrieve')
    data = doPost('https://getpocket.com/v3/get', post_data)
    logging.info('After doPost retrieve')
    return data


def modify(consumer_key, access_token, action, item):
    #https://getpocket.com/v3/send?actions=[{"action":"archive","time":1348853312,"item_id":229279689}]&access_token=[ACCESS_TOKEN]&consumer_key=[CONSUMER_KEY]
    action = str('[{"action": \"' + action + '\", "item_id": \"' + str(item) + '\"}]')
    data = doPost('https://getpocket.com/v3/send',
                  {'consumer_key': consumer_key,
                   'access_token': access_token,
                   'actions': action})
    logging.info("result: " + data)
    return data


def archive(consumer_key, access_token, item):
    logging.info("archive from pocket: " + item)
    return modify(consumer_key, access_token, 'archive', item)


def delete(consumer_key, access_token, item):
    logging.info("delete from pocket: " + str(item))
    logging.info(consumer_key + " + " + access_token)
    return modify(consumer_key, access_token, 'delete', item)

