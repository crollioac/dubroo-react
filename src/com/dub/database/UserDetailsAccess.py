import json
import logging

from com.dub.objects.Audio import Audio
from com.dub.objects.User import User
from google.appengine.ext import ndb


# from com.dub.database.DubrooDataAccess import DubrooDataAccess
class UserDetailsAccess:
	def __init__(self):
		return

# Constructs a Datastore key for a Guestbook entity with guestbook_name.
	def UserKey(self, uniqueID):
		return ndb.Key('User', uniqueID)
	
# 	def AudioLink(self,audioKey):
# 		return ndb.Key('Audio', audioKey)
	
	def checkIfUserExists(self, uniqueID, userName):
		userQuery = User.query(ancestor=self.UserKey(uniqueID))
		user2 = userQuery.get()
		response = dict()
		if(user2 != None):
			# logging.info(str(user2.uniqueID))
			if(str(user2.uniqueID) == uniqueID):
				response["valid"] = "Valid User"
				response["userDisplayName"] = user2.userDisplayName
		else:
			response["invalid"] = "User not Registered"
		return response
	
	def RegisterNewUser(self, uniqueID, userName):
		userQuery = User.query(ancestor=self.UserKey(uniqueID))
		user = userQuery.get()
		response = dict()
		if(user != None):
			logging.info(str(user.uniqueID))
			if(str(user.uniqueID) == uniqueID):
				response["exists"] = "User already Exists"
		else:
			user = User(parent=self.UserKey(uniqueID))
			user.uniqueID = uniqueID
			user.userName = userName
			user.userDisplayName = str(userName.replace(" ", "_"))
			user.upVotedAudios = []
			user.downVotedAudios = []
			user.addedVideos = []
			user.put()
			response["registered"] = "New user Added"
		return response
	
	def UpdateUserDisplayName(self, uniqueID, newName):
		userQuery = User.query(ancestor=self.UserKey(uniqueID))
		user = userQuery.get()
		response = dict()
		if(user != None):
			audquery = Audio.query(Audio.composerEmail == uniqueID)

			audios = audquery.fetch()
			for audio in audios:
				audio.composer = newName
				audio.put()
			user.userDisplayName = newName
			user.put()
			response["newName"] = newName
			
		return response
	
	
	def UserVotesAnAudio(self, audioKey, direction, uniqueID):
		userQuery = User.query(ancestor=self.UserKey(uniqueID))
		user = userQuery.get()
		response = dict()
		if(user != None):
			if(direction == "up"):
				upVotedList = []
				upVotedList = user.upVotedAudios
				q = Audio.query(Audio.audiolink == audioKey)
				aud = q.get()
	# 			if(upVoteStatus == "1"):
				upvotecount = aud.upvotes
				upvotecount = int(upvotecount) + 1
				aud.upvotes = upvotecount
				upVotedList.append(audioKey)
				response["result"] = "Upvoted Successfully"
				user.upVotedAudios = upVotedList
			else:
				downVotedList = []
				downVotedList = user.downVotedAudios
				q = Audio.query(Audio.audiolink == audioKey)
				aud = q.get()
				downvotecount = aud.downvotes
				downvotecount = int(downvotecount) + 1
				aud.downvotes = downvotecount
				downVotedList.append(audioKey)
				response["result"] = "Downvoted Successfully"
				user.downVotedAudios = downVotedList
			user.put()
			aud.put()
			
			return json.dumps(response)
		
	
	def UserUpVotesAnAudio(self, audioKey, upVoteStatus, uniqueID):
		userQuery = User.query(ancestor=self.UserKey(uniqueID))
		user = userQuery.get()
		response = {}
		if(user != None):
			upVotedList = []
			upVotedList = user.upVotedAudios
			q = Audio.query(Audio.audiolink == audioKey)
			aud = q.get()
# 			if(upVoteStatus == "1"):
			upvotecount = aud.upvotes
			upvotecount = int(upvotecount) + 1
			aud.upvotes = upvotecount
			upVotedList.append(audioKey)
			response["upvoteIncreased"] = "Upvoted Successfully"
			user.upVotedAudios = upVotedList
			user.put()
			aud.put()
			
	def UserDownVotesAnAudio(self, audioKey, downVoteStatus, uniqueID):
		userQuery = User.query(ancestor=self.UserKey(uniqueID))
		user = userQuery.get()
		response = dict()
		if(user != None):
			downVotedList = []
			downVotedList = user.downVotedAudios
			q = Audio.query(Audio.audiolink == audioKey)
			aud = q.get()
			if(downVoteStatus == "1"):
				downvotecount = aud.downvotes
				downvotecount = int(downvotecount) + 1
				aud.downvotes = downvotecount
				downVotedList.append(audioKey)
				response["downvoteIncreased"] = "downvoted Successfully"
			else:
				downvotecount = aud.downvotes
				downvotecount = int(downvotecount) - 1
				aud.downvotes = downvotecount
				downVotedList.remove(audioKey)
				response["downvoteReduced"] = "downvote Reduced Successfully"
			user.downVotedAudios = downVotedList
			user.put()
			aud.put()
			
	def UserHandleAvailability(self, handle, uniqueID):
		userQuery = User.query(User.userDisplayName == handle.lower())
		user = userQuery.get()
		available = {}

		if(user == None):
			available["available"] = "true"
		else:
			available["available"] = "false"

		
		return json.dumps(available)
	
	def GetUserDetailsByHandle(self, handle):
		userQuery = User.query(User.userName == handle)
		user = userQuery.get()
		userObj = {}
		if(user != None):
			userObj["userName"] = str(user.userName)
			userObj["userDisplayName"] = str(user.userDisplayName)
			userObj["uniqueID"] = str(user.uniqueID)

			userObj["knownlanguages"] = user.knownlanguages

			# dda = DubrooDataAccess()
			audioList = self.GetAudiosList("", "", 0, 10, user.uniqueID, "true", handle)
			userObj["audioList"] = audioList



		else:
			userObj["error"] = "User not found"

		return userObj



	def GetAudiosList(self, videoLink, language, offset, limit, uniqueID, byUser, handle):
		if(language != ""):
			audquery = Audio.query(ancestor=self.AudioLink(videoLink)).filter(Audio.language == str(language)).order(-Audio.viewCount)
		elif(byUser == "true"):
			audquery = Audio.query(Audio.composer == handle).order(-Audio.recordeddate)
		else:
			audquery = Audio.query(ancestor=self.AudioLink(videoLink)).order(-Audio.viewCount)
		audios = audquery.fetch(int(limit), offset=int(offset))
		Audios = []
		upVotedList = []
		downVotedList = []
		if(uniqueID != ""):
			userQuery = User.query(ancestor=self.UserKey(uniqueID))
			user = userQuery.get()
			response = dict()
			if(user != None):
				upVotedList = user.upVotedAudios
				downVotedList = user.downVotedAudios
		for audio in audios:
			aud = dict()
			aud["audname"] = audio.name
			aud["audkey"] = str(audio.audiolink)
			aud["composer"] = audio.composer
			aud["starttime"] = str(audio.starttime)
			aud["viewcount"] = str(audio.viewCount)
			aud["language"] = str(audio.language)
			aud["upvotes"] = str(audio.upvotes)
			aud["downvotes"] = str(audio.downvotes)
			aud["videolink"] = str(audio.videolink)
			aud["recordeddate"] = str(audio.recordeddate)
			aud["audioGAEID"] = str(audio.key.id())
			# logging.info(upVotedList)
			if(audio.audiolink in upVotedList):
				aud["voted"] = "up"
			elif(audio.audiolink in downVotedList):
				aud["voted"] = "down"
			else:
				aud["voted"] = "none"
				#             aud["audname"]=audio.name
				# logging.info(audio.audiolink)
			Audios.append(aud)
		return Audios

	def UpdateUserLanguages(self, uniqueID, langs):
		userQuery = User.query(ancestor=self.UserKey(uniqueID))
		user = userQuery.get()
		response = dict()
		if(user != None):
			user.knownlanguages = langs
			user.put()
			response["langList"] = langs
			response["result"] = "success"
		return response

			





    	
		
