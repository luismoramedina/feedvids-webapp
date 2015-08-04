from google.appengine.ext import db


class AccessToken(db.Model):
    """An AccessToken related to username"""
    username = db.StringProperty(required=True)
    token = db.StringProperty(required=True)
    #TODO make choice
    service = db.StringProperty(required=True)