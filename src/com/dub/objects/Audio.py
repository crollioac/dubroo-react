'''
Created on 03-Jan-2015

@author: kiran
'''

from google.appengine.ext import ndb


class Audio(ndb.Model):
    name = ndb.StringProperty(required=True)
    videolink = ndb.StringProperty(required=True)
    audiolink = ndb.StringProperty(required=True)
    upvotes = ndb.IntegerProperty()
    downvotes = ndb.IntegerProperty()
    composer = ndb.StringProperty(required=True)
    composerEmail = ndb.StringProperty()
    recordeddate = ndb.DateProperty()
    starttime = ndb.StringProperty()
    language = ndb.StringProperty()
    viewCount = ndb.IntegerProperty()
    status = ndb.StringProperty()
    
    
    
