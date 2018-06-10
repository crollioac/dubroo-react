'''
Created on 22-Apr-2014

@author: tousif
'''
import logging

from com.dub.database.DubrooDataAccess import DubrooDataAccess
from google.appengine.api import memcache


class DubrooApi:
    
    

    def getTimestamp(self):
#        midnight = datetime.combine((datetime.now()+ root.timedelta(hours=5,minutes=30)), time.max)
#        return mktime(midnight.timetuple())
        return 7200   
    def __init__(self):
        return
    
    def GetAudiosList(self, videoLink, language, offset, limit, uniqueID, byUser, handle):
        dda = DubrooDataAccess()
        responseData = dda.GetAudiosList(videoLink, language, offset, limit, uniqueID, byUser, handle)
        return responseData
    
    def GetAudioChunk(self, audioLink, chunkIndex):
        dda = DubrooDataAccess()
        responseData = dda.GetAudioChunk(audioLink, chunkIndex)
        return responseData
    
    def AddNewVideo(self, name, videoLink, videocat, uniqueID):
        dda = DubrooDataAccess()
        responseData = dda.AddNewVideo(name, videoLink, videocat, uniqueID)
        return responseData
    
    def AddSrtToVideo(self, name, videoLink, uniqueID, srtBlobKey):
        dda = DubrooDataAccess()
        responseData = dda.AddSrtToVideo(name, videoLink, uniqueID, srtBlobKey)
        return responseData
    
    def AddNewAudioChunk(self, audioLink, blobkey, chunkIndex, starttime, endtime):
        dda = DubrooDataAccess()
        responseData = dda.AddNewAudioChunk(audioLink, blobkey, chunkIndex, starttime, endtime)
        return responseData
    
    def AddNewAudio(self, audioname, audioLink, videoLink, composer, composeremail, starttime, language, uniqueID):
        dda = DubrooDataAccess()
        responseData = dda.AddNewAudio(audioname, audioLink, videoLink, composer, composeremail, starttime, language, uniqueID)
        return responseData
    
    def GetVideoLinks(self, category, sortBy, offset, limit):
        dda = DubrooDataAccess()
        responseData = dda.GetVideoLinks(category, sortBy, offset, limit)
        return responseData    
    
    def GetAudioDetails(self, audBlobkey, uniqueID):
        dda = DubrooDataAccess()
        responseData = dda.GetAudioDetails(audBlobkey, uniqueID)
        return responseData    
    
    def GetAudioChunkDetails(self, audioLink, chunkIndex):
        dda = DubrooDataAccess()
        responseData = dda.GetAudioChunkDetails(audioLink, chunkIndex)
        return responseData    
    
    def IncreaseViewCount(self, audioblobkey, viewcount):
        dda = DubrooDataAccess()
        responseData = dda.IncreaseViewCount(audioblobkey, viewcount)
        return responseData
    
    def GetVideoDetails(self, videoUrl):
        dda = DubrooDataAccess()
        responseData = dda.GetVideoDetails(videoUrl)
        return responseData
    
    def getVideoSearch(self, searchterm):
        dda = DubrooDataAccess()
        responseData = dda.getVideoSearch(searchterm)
        return responseData
    
    def GetAudioSearch(self, searchterm, videoLink):
        dda = DubrooDataAccess()
        responseData = dda.GetAudioSearch(searchterm, videoLink)
        return responseData
        
    
    








        
#             time=self.getTimestamp()
            
#             mc = memcache.Client()
#             key=str(brandProductID)+"|"+"brandreport"+"|"+str(startdate)+"|"+str(enddate)+"|"+str(datatype)
#             if(mc.get(key)!=None):
#                 responseData=mc.get(key)
#             else:
#                 brandInsight=DubrooDataAccess()
#                 responseData=brandInsight.
#                 brandInsight.closeConnection()
#                 try:
#                     mc.set(key,responseData,time)
#                 except:
#                     logging.info(sys.exc_info()[1])
                    
            
        
    
        
