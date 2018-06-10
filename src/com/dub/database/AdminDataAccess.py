from collections import defaultdict
from datetime import datetime
import json
import logging

from com.dub.objects.Audio import Audio
from com.dub.objects.User import User
from com.dub.objects.Video import Video
from google.appengine.ext import ndb


# import UserDetailsAccess
class AdminDataAccess:

	def __init__(self):
#         self.connection=ConnectionManager().get_connection()
		return

	def tree(self):
		return defaultdict(self.tree)

	def VideoLink(self, videoLink):
		return ndb.Key('Video', videoLink)

	def AudioLink(self, audioKeys):
		return ndb.Key('Audio', audioKeys)

	def UserKey(self, uniqueID):
		return ndb.Key('User', uniqueID)

	def GetAudiosListByDate(self, offset, limit, startdate, enddate):
		startdate = datetime.strptime(startdate, '%Y-%m-%d')
		enddate = datetime.strptime(enddate, '%Y-%m-%d')


		# logging.info(startdate)
		audquery = Audio.query(Audio.recordeddate >= startdate, Audio.recordeddate <= enddate)
		audios = audquery.fetch(int(limit), offset=int(offset))
		Audios = []
		# upVotedList=[]
		# downVotedList=[]

		# if(uniqueID != ""):
		#     userQuery=User.query(ancestor=self.UserKey(uniqueID))
		#     user = userQuery.get()
		#     response = dict()
		#     if(user != None):
		#         upVotedList = user.upVotedAudios
		#         downVotedList = user.downVotedAudios
		for audio in audios:
			aud = dict()
			aud["audname"] = audio.name
			aud["audkey"] = str(audio.audioblobkey)
			aud["userDisplayName"] = audio.composer
			aud["uniqueID"] = str(audio.composerEmail)
			uniqueID = audio.composerEmail
			userQuery = User.query(ancestor=self.UserKey(uniqueID))
			user = userQuery.get()
			if(user != None):
				aud["userName"] = user.userName


			aud["starttime"] = str(audio.starttime)
			aud["viewcount"] = str(audio.viewCount)
			aud["language"] = str(audio.language)
			aud["upvotes"] = str(audio.upvotes)
			aud["downvotes"] = str(audio.downvotes)
			aud["videolink"] = str(audio.videolink)
			aud["recordeddate"] = str(audio.recordeddate)

			aud["audioGAEID"] = str(audio.key.id())
			Audios.append(aud)
		return Audios
			# logging.info(upVotedList)

			# if(audio.audiolink in upVotedList):
			#     aud["voted"]="up" 
			# elif(audio.audiolink in downVotedList):
			#     aud["voted"]="down"
			# else:
			#     aud["voted"]="none"
			    
			#             aud["audname"]=audio.name

			# logging.info(audio.audiolink)


	def GetVideoLinksBydate(self, offset, limit, startdate, enddate):
        # logging.info(category)
		startdate = datetime.strptime(startdate, '%Y-%m-%d')
		enddate = datetime.strptime(enddate, '%Y-%m-%d')
		vidquery = Video.query(Video.addedDate >= startdate, Video.addedDate <= enddate).order(-Video.addedDate)
		videos = vidquery.fetch(int(limit), offset=int(offset))
    
#         logging.info(str(videos))
		Videos = []
		for video in videos:
			vidobj = dict()
			vidobj["videoname"] = str(video.name.encode('utf-8'))
			vidobj["videolink"] = str(video.videolink)
			vidobj["videocat"] = str(video.videoCategory)
			vidobj["dubscount"] = str(video.dubsCount)
			vidobj["addeddate"] = str(video.addedDate)
			vidobj["videoGAEID"] = str(video.key.id())
			uniqueID = video.addedUser
# logging.info(uniqueID)
			if(uniqueID != None):
				userQuery = User.query(ancestor=self.UserKey(uniqueID))
				user = userQuery.get()
				if(user != None):
					vidobj["userName"] = user.userName
					vidobj["userDisplayName"] = user.userDisplayName

				vidobj["userUniqueID"] = str(uniqueID)
				# logging.info(video.key.id())
			Videos.append(vidobj)
		return Videos

	def ModifyVideoMetadata(self, videoLink, VideoCat):
		video = Video.query(ancestor=self.VideoLink(videoLink)) 
		vidobj = video.get()

		if(VideoCat != "" and VideoCat != None):
			vidobj.videoCategory = VideoCat
		vidobj.put()
		resp = {}
		resp["response"] = "success"
		return resp

	def ModifyAudioMetadata(self, audioKey, AudioName, AudioLang, starttime):
		logging.info(audioKey)
		audio = Audio.query(Audio.audiolink == audioKey)
		audobj = audio.get()
		if(AudioName != "" and AudioName != None):
			audobj.name = AudioName
		
		if(AudioLang != "" and AudioLang != None):
			audobj.language = AudioLang
		
		if(starttime != "" and starttime != None):
			audobj.starttime = starttime

		audobj.put()

		resp = {}
		resp["response"] = "success"
		return resp



	    # update apis
	def UpdateVideosObject(self):
	    # goes through each video added by the user and assigns uniqueid to video

	    # userQuery = User.query().fetch(500)    #fetches all 500 users
    # videos = []

        # resp = {}
        # for user in userQuery:
        #     logging.info(user.uniqueID)
        #     userID = user.uniqueID
        #     videos = user.addedVideos
        #     for vid in videos: 

        #         video = Video.query(ancestor = self.VideoLink(vid))
        #         vidobj = video.get()
        #         if(vidobj != None):
        #             logging.info(" HHHH "+str(vidobj.addedUser))
        #             if(vidobj.addedUser == None):
        #                 vidobj.addedUser = userID
        #                 vidobj.put()
        #                 resp["result"] ="modified success"
            
        # return resp

        # goes through each video added by the user and assigns uniqueid to video
		vidquery = Video.query()
		videos = vidquery.fetch(200)
		resp = {}
		for vid in videos:
			# logging.info(" HHHH "+str(vid.addedUser))
			if(vid != None):
				# if(vid != None):
					# vidstatus = vid.status
					
					# if(vidstatus != None and vidname != ""):
				vid.status = "active"
				vid.put()
				resp["result"] = "modified success"
		return resp

	def UpdateAudiosObject(self):
		audquery = Audio.query()
		audios = audquery.fetch(200)
		resp = {}
		for aud in audios:
			# logging.info(" HHHH "+str(vid.addedUser))
			if(aud != None):
				aud.status = "active"
				aud.put()
				resp["result"] = "modified success"
		return resp


	def UpdateUserObject(self):
		userQuery = User.query().fetch(500)  # fetches all 500 users
		resp = {}
		for user in userQuery:
			logging.info(user.userDisplayName)
			userDisplayName = user.userDisplayName
			if(userDisplayName == None):
				user.userDisplayName = user.userName.replace(" ", "_")
				user.put()
				resp["result"] = "modified success"
			elif(" " in userDisplayName):
				user.userDisplayName = user.userDisplayName.replace(" ", "_")
				user.put()
				resp["result"] = "modified success"

		return resp


	# delete APIS


	def DeleteVideosObject(self, vidUrl):
		video = Video.query(ancestor=self.VideoLink(vidUrl)) 
		vidobj = video.get()
		vidobj.status = "deleted"
		audquery = Audio.query(ancestor=self.AudioLink(vidUrl))
		audios = audquery.fetch(100)
		for aud in audios:
			aud.status = "deleted"
		vidobj.put()





