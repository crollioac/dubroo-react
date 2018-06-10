'''
Created on 22-Apr-2014

@author: tousif
'''
from collections import defaultdict
from datetime import datetime
import json
import logging

from com.dub.objects.Audio import Audio
from com.dub.objects.Video import Video
from google.appengine.ext import ndb


class BrandReportDataAccess:
    
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
        
    def AddNewVideo(self, name, videoLink, videocat):
        
#         v = self.VideoLink(videoLink)
        
        vidquery = Video.query(ancestor=self.VideoLink(videoLink))
        
        videos = vidquery.get()
        if(videos != None):
            logging.info(str(videos.videolink))
                
            if(str(videos.videolink) == videoLink):
                post = dict()
                post["error"] = "Already Exists"
                return json.dumps(post)
        else:
            vid = Video(parent=self.VideoLink(videoLink))
    #         name="sample",videolink=videoLink,audiolink="",videoCategory="Entertainment"
            vid.name = name
            vid.videolink = videoLink
            vid.audiolink = ""
            vid.videoCategory = videocat
            vid.dubsCount = 0
            vid.addedDate = datetime.now()
            vid.put()
            post = dict()
            post["result"] = "Added new video"
            return json.dumps(post)
        
        
    def GetVideoLinks(self, category, sortBy):
        logging.info(category)
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
        videos = vidquery.fetch(100)
#         logging.info(str(videos))
        
        
        Videos = []
        
        for video in videos:
            vidobj = dict()
            vidobj["videoname"] = str(video.name)
            vidobj["videolink"] = str(video.videolink)
            vidobj["videocat"] = str(video.videoCategory)
            vidobj["dubscount"] = str(video.dubsCount)
            vidobj["addeddate"] = str(video.addedDate)
            Videos.append(vidobj)
            
            
        return json.dumps(Videos)
     
            
    def GetAudioByLink(self, videoLink):
        audquery = Audio.query(ancestor=self.AudioLink(videoLink)).order(-Audio.viewCount)
        audios = audquery.fetch(100)
        Audios = []
        for audio in audios:
            aud = dict()
            aud["audname"] = audio.name
            aud["audkey"] = str(audio.audiolink)
            aud["composer"] = audio.composer
            aud["starttime"] = str(audio.starttime)
            aud["viewcount"] = str(audio.viewCount)
            aud["language"] = str(audio.language)
#             aud["audname"]=audio.name
            
            logging.info(audio.audiolink)
            Audios.append(aud)
        return json.dumps(Audios)    
        
    
    def AddNewAudio(self, blobkeys, audioname, videoLink, composer, composeremail, starttime, language):
        
#         logging.info(str(blob))
        
        
        vid = Video.query(Video.videolink == videoLink)
        v = vid.get()
        v.dubsCount = int(v.dubsCount) + 1
        v.put()
        
        
        audioKeys = blobkeys
        aud = Audio(parent=self.AudioLink(videoLink))
        aud.audiolink = audioKeys[0]
        aud.videolink = videoLink
        aud.name = audioname
        aud.audioblobkey = audioKeys
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
        post["result"] = audioKeys
        return json.dumps(post)
        
    def GetAudioDetails(self, audkey):
            
#         audquery = Audio.query(ancestor=self.AudioLink(videoLink))
        q = Audio.query(Audio.audiolink == audkey)
#         q  = ndb.gql("Select * from Audio where audioblobkey = :1",audBlobkey)
        Audios = []
        audio = q.get()
        logging.info(audio)
        if(audio != None):
            aud = dict()
            aud["audname"] = audio.name
            aud["audkey"] = str(audio.audiolink)
            aud["composer"] = audio.composer
            aud["starttime"] = str(audio.starttime)
            aud["viewcount"] = str(audio.viewCount)
            aud["language"] = str(audio.language)
    #             aud["audname"]=audio.name
            
            Audios.append(aud)
        else:
            aud = dict()
            aud["error"] = "Url contains in valid audio key"
            Audios.append(aud)
        return json.dumps(Audios)
        

    
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
        vidobj["videoname"] = str(video.name)
        vidobj["videolink"] = str(video.videolink)
        vidobj["videocat"] = str(video.videoCategory)
        vidobj["dubscount"] = str(video.dubsCount)
        vidobj["addeddate"] = str(video.addedDate)
        return json.dumps(vidobj)
     
    def getVideoSearch(self, searchterm):
        vidquery = Video.query(ndb.AND(Video.name >= searchterm, Video.name <= searchterm + u'\ufffd'))
        videos = vidquery.fetch(100)
#         logging.info(str(videos))
        
        
        Videos = []
        
        for video in videos:
            vidobj = dict()
            vidobj["videoname"] = str(video.name)
            vidobj["videolink"] = str(video.videolink)
            vidobj["videocat"] = str(video.videoCategory)
            vidobj["dubscount"] = str(video.dubsCount)
            vidobj["addeddate"] = str(video.addedDate)
            Videos.append(vidobj)
            
            
        return json.dumps(Videos)
        
    
    
    
