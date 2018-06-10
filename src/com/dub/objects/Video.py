'''
Created on 03-Jan-2015

@author: kiran
'''

import datetime

from google.appengine.api import users
from google.appengine.ext import ndb


class Video(ndb.Model):
    name = ndb.StringProperty(required=True)
    videolink = ndb.StringProperty(required=True)
    videoCategory = ndb.StringProperty()
    dubsCount = ndb.IntegerProperty()
    addedDate = ndb.DateTimeProperty()
    addedUser = ndb.StringProperty(required=True)
    dubbedLanguages = ndb.StringProperty(repeated=True)
    status = ndb.StringProperty()
    srtBlobKey = ndb.StringProperty()
    
    
    
    
    
    
