'''
Created on 22-Apr-2014

@author: tousif
'''
import ConfigParser
from datetime import datetime, date, time
import json
import logging
import sys
from time import mktime

from com.dub.api.session_module import BaseSessionHandler
from com.dub.database.BrandReportDataAccess import BrandReportDataAccess
import datetime as root
from google.appengine.api import memcache, users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class BrandReport:
    
    

    def getTimestamp(self):
#        midnight = datetime.combine((datetime.now()+ root.timedelta(hours=5,minutes=30)), time.max)
#        return mktime(midnight.timetuple())
        return 7200   
    def __init__(self):
        return
    
    def GetAudioByLink(self, videoLink):
#         responseData = dict()
        brUserDA = BrandReportDataAccess()
        responseData = brUserDA.GetAudioByLink(videoLink)
        
        return responseData
    
    
    def AddNewVideo(self, name, videoLink, videocat, srtBlobKey):
        brUserDA = BrandReportDataAccess()
        responseData = brUserDA.AddNewVideo(name, videoLink, videocat, srtBlobKey)
        return responseData
    
    def AddNewAudio(self, blobkeys, audioname, videoLink, composer, composeremail, starttime, language):
        brUserDA = BrandReportDataAccess()
        responseData = brUserDA.AddNewAudio(blobkeys, audioname, videoLink, composer, composeremail, starttime, language)
        return responseData
    
    def GetVideoLinks(self, category, sortBy):
        brUserDA = BrandReportDataAccess()
        responseData = brUserDA.GetVideoLinks(category, sortBy)
        return responseData    
    
    def GetAudioDetails(self, audBlobkey):
        brUserDA = BrandReportDataAccess()
        responseData = brUserDA.GetAudioDetails(audBlobkey)
        return responseData    
    
    
    def IncreaseViewCount(self, audioblobkey, viewcount):
        brUserDA = BrandReportDataAccess()
        responseData = brUserDA.IncreaseViewCount(audioblobkey, viewcount)
        return responseData
    
    def GetVideoDetails(self, videoUrl):
        brUserDA = BrandReportDataAccess()
        responseData = brUserDA.GetVideoDetails(videoUrl)
        return responseData
    
    def getVideoSearch(self, searchterm):
        brUserDA = BrandReportDataAccess()
        responseData = brUserDA.getVideoSearch(searchterm)
        return responseData
        
#             time=self.getTimestamp()
            
#             mc = memcache.Client()
#             key=str(brandProductID)+"|"+"brandreport"+"|"+str(startdate)+"|"+str(enddate)+"|"+str(datatype)
#             if(mc.get(key)!=None):
#                 responseData=mc.get(key)
#             else:
#                 brandInsight=BrandReportDataAccess()
#                 responseData=brandInsight.
#                 brandInsight.closeConnection()
#                 try:
#                     mc.set(key,responseData,time)
#                 except:
#                     logging.info(sys.exc_info()[1])
                    
            
        
    
        
