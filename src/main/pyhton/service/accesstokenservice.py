import pymongo
import config

__author__ = 'mora'

print config.app_config
MONGO_URL = config.app_config['mongo_url']

cache = {}


def get_token(current_user):
    """return a token like this dbdf64ab-blablalblaa"""

    if not current_user:
        return None

    cached_token = get_cached_token(current_user)
    if not cached_token:
        client = pymongo.MongoClient(MONGO_URL)
        db = client.get_default_database()
        client.close()

        users_cursor = db['users'].find({'user': current_user})

        if users_cursor.count() > 0:
            token = users_cursor.next()['access_token']
            users_cursor.close()
            cache_token(current_user, token)
            return token
        return None
    else:
        return cached_token


def cache_token(username, access_token):
    global cache
    cache['accesstoken_' + username] = access_token


def get_cached_token(username):
    global cache
    if 'accesstoken_' + username in cache:
        return cache['accesstoken_' + username]

#    memcache.set_multi({'' + username: access_token}, key_prefix='access_token_')


def put_token(username, access_token, service):
    client = pymongo.MongoClient(MONGO_URL)
    db = client.get_default_database()

    query = {'user': username}

    document = db['users'].find_one(query)

    if document:
        db['users'].update(
            query,
            {'$set': {'user': username, 'access_token': access_token, 'service': service}},
            multi=True)
    else:
        db['users'].insert({'user': username, 'access_token': access_token, 'service': service})

    client.close()


if __name__ == '__main__':
    cache_token('luismoramedina', 'bla1')
    cache_token('mora', 'bla2')
    cache_token('luis', 'bla3')
    print cache
    print get_cached_token('luismoramedina')
    print get_cached_token('a')
    print get_token('a')