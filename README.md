# feedvids webapp

## app on production
check http://feedvids.herokuapp.com/
NOTE: not working in https yet

## install

- pip install Paste
- pip install webapp2
- pip install webob
- pip install jinja2
- pip install pymongo

## configure

- create a src/main/pyhton/config.py with this content:

```python
app_config = {
    'consumer_key' : '$pocket_consumer_key',
    'mongo_url' : '$mongo_database_url'
}
```

- create the mongo collection 'users' with columns: 'user', 'access_token', 'service'

## run

NOTE: Use python 2.x

python src/main/python/main.py

## known bugs

- no urlencoding on share urls... twitter + # -> bad
