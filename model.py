from google.appengine.ext import ndb

class Message(ndb.Model):
    text = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    delete = ndb.BooleanProperty(default=False)
    status = ndb.BooleanProperty(default=False)