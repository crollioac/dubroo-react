import datetime

from google.appengine.api import users
from google.appengine.ext import ndb


class User(ndb.Model):
    userName = ndb.StringProperty(required=True)
    uniqueID = ndb.StringProperty(required=True)
    userDisplayName = ndb.StringProperty()
    upVotedAudios = ndb.StringProperty(repeated=True)
    downVotedAudios = ndb.StringProperty(repeated=True)
    addedVideos = ndb.StringProperty(repeated=True)
    recordedAudios = ndb.StringProperty(repeated=True)
    knownlanguages = ndb.StringProperty()
    userAbused = ndb.StringProperty()
    userRating = ndb.StringProperty()  # based on views,upvotes,downvotes and num of audios dubbed
    userLocation = ndb.StringProperty()
    userAddress = ndb.StringProperty()
    userRatingFluency = ndb.StringProperty()
    userRatingClarity = ndb.StringProperty()
    userRatingVoiceQuality = ndb.StringProperty()
    userRatingContent = ndb.StringProperty()
    userPicUrl = ndb.StringProperty()

    
