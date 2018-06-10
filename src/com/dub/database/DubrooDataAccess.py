from collections import defaultdict
from datetime import datetime
import json
import logging
import uuid

from com.dub.objects.Audio import Audio
from com.dub.objects.AudioChunk import AudioChunk
from com.dub.objects.User import User
from com.dub.objects.Video import Video
from google.appengine.ext import ndb


# import UserDetailsAccess
class DubrooDataAccess:
    
    parentPFList = ""
    
    def __init__(self):
#         self.connection=ConnectionManager().get_connection()
        return 
    
    
    def tree(self):
        return defaultdict(self.tree)

    def VideoLink(self, videoLink):
        """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
        return ndb.Key('Video', videoLink)
    
    def AudioLink(self, audioKeys):
        """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
        return ndb.Key('Audio', audioKeys)

    def UserKey(self, uniqueID):
        return ndb.Key('User', uniqueID)
    
    def AudioChunkKey(self, audioKey):
        return ndb.Key('AudioChunk', audioKey)
        
    def AddSrtToVideo(self, name, videoLink, uniqueID, srtBlobKey):
        vidKeys = Video.query(ancestor=self.VideoLink(videoLink)).fetch(1, keys_only=True)
        if(len(vidKeys) == 0):
            logging.info("Reaching AddSrtToVideo none: ")
            post = dict()
            post["error"] = "Video Not Found"
            return json.dumps(post)
        else:
            vidKey = vidKeys[0]
            vid = vidKey.get()
            vid.srtBlobKey = srtBlobKey
            vid.put()
            post = dict()
            logging.info("Reaching AddSrtToVideo after put: " + srtBlobKey + " videolink: " + videoLink)
            post["result"] = "Added new Srt file"
            return json.dumps(post)
        
    def AddNewVideo(self, name, videoLink, videocat, uniqueID):
        
#         v = self.VideoLink(videoLink)
        
        vidquery = Video.query(ancestor=self.VideoLink(videoLink))
        
        videos = vidquery.get()
        if(videos != None):
            # logging.info(str(videos.videolink))
                
            if(str(videos.videolink) == videoLink):
                post = dict()
                post["error"] = "Already Exists"
                return json.dumps(post)
        else:
            # userQuery=User.query(ancestor=self.UserKey(uniqueID))
            # user = userQuery.get()
            # response = dict()
            # if(user != None):
            #     # logging.info(str(user.uniqueID))
            #     videosByUser = []
            #     videosByUser = user.addedVideos
            #     videosByUser.append(videoLink)            
            #     user.addedVideos = videosByUser
            #     user.put()

            vid = Video(parent=self.VideoLink(videoLink))
    #         name="sample",videolink=videoLink,audiolink="",videoCategory="Entertainment"
            vid.name = str(name.encode('utf-8').lower())
            vid.videolink = videoLink
            vid.audiolink = ""
            vid.videoCategory = videocat
            vid.dubsCount = 0
            vid.addedDate = datetime.now()
            vid.addedUser = uniqueID
            vid.put()
            post = dict()
            post["result"] = "Added new video"
            return json.dumps(post)
        
        
    def GetVideoLinks(self, category, sortBy, offset, limit):
        # logging.info(category)
        if(sortBy == "time"):
            if(category == "all"):
                vidquery = Video.query().order(-Video.addedDate)
            else:
                vidquery = Video.query(Video.videoCategory == str(category)).order(-Video.addedDate)
                
        elif(sortBy == "dubscount"):
            if(category == "all"):
                vidquery = Video.query().order(-Video.dubsCount)
            else:
                vidquery = Video.query(Video.videoCategory == str(category)).order(-Video.dubsCount)
                
        if(limit == "" or limit == None):
            videos = vidquery.fetch(100)
        else:
            videos = vidquery.fetch(int(limit), offset=int(offset))
        
        Videos = []
        for video in videos:
            vidobj = dict()
            vidobj["videoname"] = str(video.name.encode('utf-8'))
            vidobj["videolink"] = str(video.videolink)
            vidobj["videocat"] = str(video.videoCategory)
            vidobj["dubscount"] = str(video.dubsCount)
            vidobj["addeddate"] = str(video.addedDate)
            vidobj["videoGAEID"] = str(video.key.id())
            addedUser = video.addedUser
            if(addedUser != None and addedUser != ""):
                userQuery = User.query(ancestor=self.UserKey(addedUser))
                user = userQuery.get()
                if(user != None):
                    vidobj["userDisplayName"] = user.userDisplayName
            # vidobj["videoAddedBy"] = str(video.addedUser)

            # logging.info(video.key.id())
            Videos.append(vidobj)
        return json.dumps(Videos)
    
    def GetAudioChunk(self, audioLink, chunkIndex):
        
        audChunkQuery = AudioChunk.query(AudioChunk.audiolink == audioLink).filter(AudioChunk.chunkIndex == chunkIndex)
        audioChunk = audChunkQuery.get()
       
        aud = dict()
        aud["blobkey"] = audioChunk.audioblobkey
        aud["starttime"] = audioChunk.starttime
        aud["endtime"] = audioChunk.endTime

        return audioChunk  
           
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
            
            if(audio.audiolink in upVotedList):
                aud["voted"] = "up" 
            elif(audio.audiolink in downVotedList):
                aud["voted"] = "down"
            else:
                aud["voted"] = "none"
            Audios.append(aud)
        return Audios
        
    def AddNewAudio(self, audioname, audioLink, videoLink, composer, composeremail, starttime, language, uniqueID):
       
        vid = Video.query(Video.videolink == videoLink)
        v = vid.get()
        v.dubsCount = int(v.dubsCount) + 1
        v.put()

        # Generating a new UUID as the audio link
        aud = Audio(parent=self.AudioLink(videoLink))
        aud.audiolink = audioLink
        aud.videolink = videoLink
        aud.name = audioname
        aud.upvotes = 0
        aud.downvotes = 0
        aud.composer = composer
        aud.composerEmail = composeremail
        aud.recordeddate = datetime.now()
        aud.starttime = starttime
        aud.language = language
        aud.viewCount = 0
        aud.put()
        post = dict()
        post["result"] = audioLink
        return json.dumps(post)
        
    def AddNewAudioChunk(self, audioLink, blobkey, chunkIndex, starttime, endtime):
        aud = AudioChunk(parent=self.AudioChunkKey(blobkey))
        aud.audiolink = audioLink
        aud.audioblobkey = blobkey
        aud.starttime = starttime
        aud.endTime = endtime
        aud.chunkIndex = chunkIndex
        aud.put()
        post = dict()
        post["result"] = blobkey
        return json.dumps(post)
            
    def GetAudioDetails(self, audkey, uniqueID):
            
        upVotedList = []
        downVotedList = []
        if(str(uniqueID) != ""):
            userQuery = User.query(ancestor=self.UserKey(uniqueID))
            user = userQuery.get()
            
            if(user != None):
                upVotedList = user.upVotedAudios
                downVotedList = user.downVotedAudios

        q = Audio.query(Audio.audiolink == audkey)
#         q  = ndb.gql("Select * from Audio where audioblobkey = :1",audBlobkey)
        Audios = []
        audio = q.get()
        # logging.info(audio)
        if(audio != None):
            aud = dict()
            aud["audname"] = audio.name
            aud["audkey"] = str(audio.audiolink)
            aud["composer"] = audio.composer
            aud["starttime"] = str(audio.starttime)
            aud["viewcount"] = str(audio.viewCount)
            aud["language"] = str(audio.language)
            aud["upvotes"] = str(audio.upvotes)
            aud["downvotes"] = str(audio.downvotes)
            aud["recordeddate"] = str(audio.recordeddate)
            aud["audioGAEID"] = str(audio.key.id())
            
            if(audkey in upVotedList):
                aud["voted"] = "up"
            elif(audkey in downVotedList):
                aud["voted"] = "down"
            else:
                aud["voted"] = "none"
    #             aud["audname"]=audio.name
            
            Audios.append(aud)
        else:
            aud = dict()
            aud["error"] = "Url contains in valid audio key"
            Audios.append(aud)
        return json.dumps(Audios)
        
    def GetAudioChunkDetails(self, audkey, chunkIndex):
        logging.info("...... audkey: " + audkey)
        q = AudioChunk.query(AudioChunk.audiolink == audkey)
        AudioChunks = []
        audioChunk = q.get()
        if(audioChunk != None):
            logging.info("...... not none : " + audioChunk.audioblobkey)
            audChunk = dict()
            audChunk["audchunkkey"] = audioChunk.audioblobkey
            audChunk["chunkindex"] = str(audioChunk.chunkIndex)
            AudioChunks.append(audChunk)
        else:
            logging.info("...... none")
            audChunk = dict()
            audChunk["error"] = "Url contains in valid audio key"
            AudioChunks.append(audChunk)
        return json.dumps(AudioChunks)
    
    def IncreaseViewCount(self, audiokey, viewcount):
        q = Audio.query(Audio.audiolink == audiokey)
        aud = q.get()
        aud.viewCount = int(viewcount)
        aud.put()
        post = dict()
        post["result"] = "View count Incresed by 1"
        return json.dumps(post)
    
    def GetVideoDetails(self, videoUrl):
        vid = Video.query(Video.videolink == videoUrl)
        video = vid.get()
        vidobj = dict()
        vidobj["videoname"] = str(video.name.encode('utf-8'))
        vidobj["videolink"] = str(video.videolink)
        vidobj["videocat"] = str(video.videoCategory)
        vidobj["dubscount"] = str(video.dubsCount)
        vidobj["addeddate"] = str(video.addedDate)
        vidobj["videoGAEID"] = str(video.key.id())
        vidobj["srtblobkey"] = str(video.srtBlobKey)
        return json.dumps(vidobj)
     
    def getVideoSearch(self, searchterm):
        vidquery = Video.query(ndb.AND(Video.name >= searchterm, Video.name <= searchterm + u'\ufffd'))
        videos = vidquery.fetch(100)
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
            Videos.append(vidobj)
            
            
        return json.dumps(Videos)
        
    def GetAudioSearch(self, searchterm, videoLink):
        audquery = Audio.query(ancestor=self.AudioLink(videoLink)).filter(ndb.AND(Audio.name >= searchterm, Audio.name <= searchterm + u'\ufffd'))
        
#         audquery=Audio.query()
        audios = audquery.fetch(100)
#         logging.info(str(videos))
        
        
        Audios = []
        
        for audio in audios:
            audobj = dict()
            audobj["audioname"] = str(audio.name)
            audobj["audiokey"] = str(audio.audiolink)
            audobj["viewcount"] = str(audio.viewCount)
            audobj["language"] = str(audio.language)
            audobj["upvotes"] = str(audio.upvotes)
            audobj["downvotes"] = str(audio.downvotes)
            audobj["recordeddate"] = str(audio.recordeddate)
            audobj["audioGAEID"] = str(audio.key.id())

            Audios.append(audobj)
    
        return json.dumps(Audios)
    
