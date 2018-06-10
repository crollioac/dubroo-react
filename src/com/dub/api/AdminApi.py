import logging

from com.dub.database.AdminDataAccess import AdminDataAccess
from google.appengine.api import memcache


class AdminApi:
	def __init__(self):
		return

	def GetAudiosListByDate(self, offset, limit, startdate, enddate):
		ada = AdminDataAccess()
		responseData = ada.GetAudiosListByDate(offset, limit, startdate, enddate)
		return responseData

	def GetVideoLinksBydate(self, offset, limit, startdate, enddate):
		ada = AdminDataAccess()
		responseData = ada.GetVideoLinksBydate(offset, limit, startdate, enddate)
		return responseData        
	
	def ModifyVideoMetadata(self, vidUrl, VideoCat):
		ada = AdminDataAccess()
		responseData = ada.ModifyVideoMetadata(vidUrl, VideoCat)
		return responseData

	def ModifyAudioMetadata(self, audioKeys, AudioName, AudioLang, starttime):
		ada = AdminDataAccess()
		responseData = ada.ModifyAudioMetadata(audioKeys, AudioName, AudioLang, starttime)
		return responseData
	# update APIS

	def UpdateVideosObject(self):
		ada = AdminDataAccess()
		responseData = ada.UpdateVideosObject()
		return responseData

	def UpdateAudiosObject(self):
		ada = AdminDataAccess()
		responseData = ada.UpdateAudiosObject()
		return responseData


	def UpdateUserObject(self):
		ada = AdminDataAccess()
		responseData = ada.UpdateUserObject()
		return responseData

    # deleteApis
	def DeleteVideosObject(self, vidUrl):
		ada = AdminDataAccess()
		responseData = ada.DeleteVideosObject(vidUrl)
		return responseData		
