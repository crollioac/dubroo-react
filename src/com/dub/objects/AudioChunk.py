'''
Created on Dec 22, 2016

@author: mahesh.yemmanuru
'''
from google.appengine.ext import ndb


class AudioChunk(ndb.Model):
    chunkIndex = ndb.IntegerProperty(required=True)  # chunk number of this recording
    audiolink = ndb.StringProperty(required=True)
    audioblobkey = ndb.StringProperty(required=True)
    starttime = ndb.StringProperty()
    endTime = ndb.StringProperty()
