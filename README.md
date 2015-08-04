# feedvids webapp

## configure

- create a src/main/pyhton/config.py with this content:

```json
app_config = {
    'consumer_key' : '$pocket_consumer_key',
    'mongo_url' : '$mongo_database_url'
}
```

- create the mongo collection 'users' with columns: 'user', 'access_token', 'service'

## run

NOTE: Use python 2.x

python src/main/python/main.py