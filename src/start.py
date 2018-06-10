import json
import logging
import os
import urllib

from com.dub.api.AdminApi import AdminApi
from com.dub.api.DubrooApi import DubrooApi
from com.dub.api.UsersApi import UsersApi
from com.dub.api.YTDetailsFetcher import YTDetailsFetcher
from com.dub.api.session_module import BaseSessionHandler
from google.appengine.ext import blobstore
from google.appengine.ext.blobstore.blobstore import BlobReader
from google.appengine.ext.webapp import blobstore_handlers
import jinja2
import webapp2


# import time
# from com.dub.api.YTDetailsFetcher import YTDetailsFetcher
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'dub123',
}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class LoadMainPage(BaseSessionHandler):
    def get(self):
        # with open(os.path.join(os.getcwd(),'dist/header.html'), 'r') as content_file:
        #     header = content_file.read()
        # with open(os.path.join(os.getcwd(),'dist/footer.html'), 'r') as content_file:
        #     footer = content_file.read()
#         logging.info(str(header))
        uniqueID = self.session.get("uniqueID")
        if(str(uniqueID) == "" or str(uniqueID) == "None"):
            loginDisplay = "block"
            logoutDisplay = "none"
        else:
            loginDisplay = "none"
            logoutDisplay = "block"
        template_values = {
            "loginDisplay":loginDisplay,
            "logoutDisplay":logoutDisplay
            # "footer":footer
        }
        template = JINJA_ENVIRONMENT.get_template('dist/gallery.html')
        self.response.write(template.render(template_values))

class LoadStudioPage(webapp2.RequestHandler):
    def get(self):
        videoLink = self.request.get("li")

        # with open(os.path.join(os.getcwd(),'dist/header.html'), 'r') as content_file:
        #     header = content_file.read()
        # with open(os.path.join(os.getcwd(),'dist/footer.html'), 'r') as content_file:
        #     footer = content_file.read()

        template_values = {
            # "header":header,
            # "footer":footer,
            "video":videoLink
        }
        template = JINJA_ENVIRONMENT.get_template('dist/studio.html')
        self.response.write(template.render(template_values))

class LoadOtherPages(webapp2.RequestHandler):
    def get(self, page):
        videoLink = self.request.get("li")

        # with open(os.path.join(os.getcwd(),'dist/header.html'), 'r') as content_file:
        #     header = content_file.read()
        # logging.info(str(header))

        template_values = {
            # "header":header,
        }
        template = JINJA_ENVIRONMENT.get_template('dist/' + str(page) + '.html')
        self.response.write(template.render(template_values))


class UserLogsIn(BaseSessionHandler):
    def get(self):
        uniqueID = self.request.get("uniqueID")
        userName = self.request.get("userName")
        response = dict()
        loggedInUserID = self.session.get("uniqueID")
        logging.info(str(loggedInUserID) + " -- " + str(uniqueID))
        
        
#         if(str(loggedInUserID) != "None" ):
        if(str(uniqueID) == str(loggedInUserID)):
            response["loginSuccess"] = "Logged In Successfully"
        else:
            # check if user exists
            u = UsersApi()
            userStatus = u.checkIfUserExists(uniqueID, userName)
            logging.info(userStatus)
            
            if(userStatus.get("valid") != None):
                self.session["uniqueID"] = uniqueID
                self.session["userName"] = userName
                self.session["userDisplayName"] = userStatus.get("userDisplayName")
                response["userDisplayName"] = userStatus.get("userDisplayName")
                response["loginSuccess"] = "Logged In Successfully"
#     #                 response = dict()
#                     response["registerSuccess"]="Welcome to Dubroo"
            else:
                userStatus = u.RegisterNewUser(uniqueID, userName)
#         logging.info(userStatus.get("exists"))
                if(userStatus.get("exists") == None):
                    self.session["uniqueID"] = uniqueID
                    self.session["userName"] = userName
                    self.session["userDisplayName"] = userName.replace(" ", "_")
                    
                    # send an automated Mail to thank , for reg



                response["userDisplayName"] = userName.replace(" ", "_")
                response["loginSuccess"] = "Logged In Successfully"
                    
                    

            
        response = json.dumps(response)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(response)



class UserLogsOut(BaseSessionHandler):
    def get(self):
        self.session["uniqueID"] = ""
        self.session["userName"] = ""
        self.session["userDisplayName"] = ""
        response = dict()
        response["logoutSuccess"] = "Logged out successfully"
        response = json.dumps(response)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(response)

class UserRegisters(BaseSessionHandler):
    def get(self):
        uniqueID = self.request.get("uniqueID")
        userName = self.request.get("userName")
        
        u = UsersApi()
        userStatus = u.RegisterNewUser(uniqueID, userName)
#         logging.info(userStatus.get("exists"))
        if(userStatus.get("exists") == None):
            self.session["uniqueID"] = uniqueID
            self.session["userName"] = userName
            
        
        response = userStatus
        response = json.dumps(response)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(response)

class UserVotesAnAudio(BaseSessionHandler):
    def get(self):
        audioKey = self.request.get("audiokey")
        direction = self.request.get("direction")
        u = UsersApi()
        uniqueID = self.session.get("uniqueID")
        
        responseData = u.UserVotesAnAudio(audioKey, direction, uniqueID)
        logging.info(responseData)

        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class GetAudioChunksList(BaseSessionHandler):
    def get(self):
        audioLink = self.request.get("audiolink")
       
        br = DubrooApi()
        responseData = br.GetAudioChunksList(audioLink)
        
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)        

class GetAudiosList(BaseSessionHandler):
    def get(self):
        videoLink = self.request.get("videolink")
        language = self.request.get("lang")
        offset = self.request.get("offset")
        limit = self.request.get("limit")
        byUser = self.request.get("byUser")
        uniqueID = self.session.get("uniqueID")
        handle = self.request.get("handle")

        if(uniqueID == None):
            uniqueID = ""
        
        logging.info(uniqueID)
        br = DubrooApi()
        responseData = br.GetAudiosList(videoLink, language, offset, limit, uniqueID, byUser, handle)
        
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)        
                
class AddNewVideo(BaseSessionHandler):
    def get(self):
        videoLink = self.request.get("videolink")
        videocat = self.request.get("videocat")

        if("gfycat" in videoLink):
            videoname = self.request.get("videoname")
        else:
            ytID = videoLink.split("/embed/")[1]
            ytDetailsFetcher = YTDetailsFetcher()
            videoDetails = ytDetailsFetcher.get_details(ytID)
            videoname = videoDetails.get("name")
            if(videoname == None):
                videoname = "Anonymous"
            # blob = self.get_uploads("blob")
            blobKey = ""
        br = DubrooApi()
        uniqueID = self.session.get("uniqueID")
        responseData = br.AddNewVideo(videoname, videoLink, videocat, uniqueID)
        logging.info(responseData)

        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)


class GetVideoLinks(webapp2.RequestHandler):
    def get(self):
        category = self.request.get("cat")
        sortBy = self.request.get("sortBy")
        offset = self.request.get("offset")
        limit = self.request.get("limit")
        br = DubrooApi()
        responseData = br.GetVideoLinks(category, sortBy, offset, limit)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        return self.response.write(responseData)

class GetYoutubeVideoDetails(webapp2.RequestHandler):
    def get(self):
        ytId = self.request.get("ytId")
        ytDetailsFetcher = YTDetailsFetcher()
        videoDetails = ytDetailsFetcher.get_details(ytId)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(json.dumps({
            'name': videoDetails.name,
            'ytId': videoDetails.ytId
            }))

class AddNewSrt(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        videoLink = self.request.get("videolink")
        blob = self.get_uploads("blob")
        uniqueID = self.request.get("uniqueID")
        logging.info(videoLink)
        videoname = self.request.get("name")
        blobStr = str(blob[0].key())
        logging.info("Reaching AddSrtToVideo: " + blobStr)
        br = DubrooApi()
        responseData = br.AddSrtToVideo(videoname, videoLink, uniqueID, blobStr)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        return self.response.write(responseData)

class AddNewAudioChunk(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        audioLink = self.request.get("audiolink")
        blob = self.get_uploads("blob")
        chunkIndex = int(self.request.get("chunkindex"))
        starttime = self.request.get("starttime")
        endtime = self.request.get("endtime")
        blobStr = str(blob[0].key())
        br = DubrooApi()
        responseData = br.AddNewAudioChunk(audioLink, blobStr, chunkIndex, starttime, endtime)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        return self.response.write(responseData)    
    
class AddNewAudio(BaseSessionHandler):
    def post(self):
        videoLink = self.request.get("videolink")
        audioname = self.request.get("audioname")
        composer = self.request.get("composer")
        composeremail = self.request.get("composeremail")
        starttime = self.request.get("starttime")
        language = self.request.get("language")
        uniqueID = self.request.get("uniqueID")
        audioLink = self.request.get("audiolink")
        br = DubrooApi()
        logging.info("............... Reaching the AddNewAudio")
        responseData = br.AddNewAudio(audioname, audioLink, videoLink, composer, composeremail, starttime, language, uniqueID)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class GetAudioBlobByKey(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        audioblobkey = self.request.get("abk")
        resource = str(urllib.unquote(audioblobkey))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

class GetSrtBlobByKey(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        srtblobkey = self.request.get("sbk")
        resource = str(urllib.unquote(srtblobkey))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
        
class GetSrtBlobByVideoURL(webapp2.RedirectHandler):
    def get(self):
        videoUrl = self.request.get("videoUrl")
        br = DubrooApi()
        responseData = br.GetVideoDetails(videoUrl)
        logging.info(responseData)
        dataMap = json.loads(responseData)
        logging.info("dataMap: .....")
        key = dataMap['srtblobkey']
        logging.info("Key: " + key)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "text/plain"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        data = BlobReader(key).read()
        logging.info("................... " + data)    
        self.response.write(data)
        
class DownLoadAudio(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        audioblobkey = self.request.get("abk")
        resource = str(urllib.unquote(audioblobkey))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info, save_as="AudioFile.ogg")
        
class redirectToStudio(webapp2.RedirectHandler):
    def get(self):
        link = self.request.get("link")
        self.redirect("/studio?li=" + link)

class GetAudioDetails(BaseSessionHandler):
    def get(self):
        audiokey = self.request.get("abk")
        br = DubrooApi()
        uniqueID = self.session.get("uniqueID")
        
        if(uniqueID == None):
            uniqueID = "";
        
        responseData = br.GetAudioDetails(audiokey, uniqueID)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class GetAudioChunkDetails(BaseSessionHandler):
    def get(self):
        audiolink = self.request.get("audiolink")
        chunkIndex = self.session.get("chunkindex")
        br = DubrooApi()
        
        responseData = br.GetAudioChunkDetails(audiolink, chunkIndex)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)
    

class IncreaseViewCount(webapp2.RedirectHandler):
    def get(self):
        audiokey = self.request.get("abk")
        viewcount = self.request.get("viewcount")
        br = DubrooApi()
        responseData = br.IncreaseViewCount(audiokey, viewcount)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class GetVideoDetails(webapp2.RedirectHandler):
    def get(self):
        videoUrl = self.request.get("videoUrl")

        br = DubrooApi()
        responseData = br.GetVideoDetails(videoUrl)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class GetVideoSearch(webapp2.RedirectHandler):
    def get(self):
        searchterm = self.request.get("term")
        br = DubrooApi()
        responseData = br.getVideoSearch(searchterm)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)
    
class GetAudioSearch(webapp2.RedirectHandler):
    def get(self):
        searchterm = self.request.get("term")
        videoLink = self.request.get("videoLink")
        br = DubrooApi()
        
        responseData = br.GetAudioSearch(searchterm, videoLink)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class GetBlobUrl(webapp2.RedirectHandler):
    def get(self):
        logging.info("Received Call to GetBlobUrl...")
        upload_url = blobstore.create_upload_url('/addNewAudioChunk')
        self.response.headers["Content-Type"] = "application/text"
        host = self.request.headers.get("Origin")
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        return self.response.write(upload_url)

class GetSrtUrl(webapp2.RedirectHandler):
    def get(self):
        logging.info("Received Call to GetSrtUrl...")
        upload_url = blobstore.create_upload_url('/addNewSrt')
        self.response.headers["Content-Type"] = "application/text"
        host = self.request.headers.get("Origin")
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        return self.response.write(upload_url)

class UserLoginStatus(BaseSessionHandler):
    def get(self):
        user = dict()
        uniqueID = self.session.get("uniqueID")
        logging.info(uniqueID)
        if(uniqueID != "" and uniqueID != None):
            userName = self.session.get("userName")
            userDisplayName = self.session.get("userDisplayName")
            user["uniqueID"] = uniqueID
            user["userName"] = userName
            user["userDisplayName"] = userDisplayName
            user["status"] = "loggedin"
        else:
            user["status"] = "loggedout"
        
        user = json.dumps(user)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(user)

class UserHandleAvailability(BaseSessionHandler):
    def get(self):
        handle = self.request.get("handle")    
        uniqueID = self.session.get("uniqueID")
        logging.info(uniqueID)
        if(uniqueID == None):
            uniqueID = ""
        ua = UsersApi()
        responseData = ua.UserHandleAvailability(handle, uniqueID)


        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class UpdateUserDisplayName(BaseSessionHandler):
    def get(self):
        handle = self.request.get("handle")
        uniqueID = self.session.get("uniqueID")
        logging.info(uniqueID)
        if(uniqueID == None):
            uniqueID = ""
        ua = UsersApi()
        responseData = ua.UpdateUserDisplayName(uniqueID, handle)

        if(responseData.get("newName") != None):
            self.session["userDisplayName"] = responseData.get("newName")
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class GetUserDetailsByHandle(BaseSessionHandler):
    def get(self):
        handle = self.request.get("handle")
        ua = UsersApi()
        responseData = ua.GetUserDetailsByHandle(handle)
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        return self.response.write(responseData)


class GetAudiosListByDate(BaseSessionHandler):
    def get(self):
        offset = self.request.get("offset")
        limit = self.request.get("limit")
        startdate = self.request.get("startdate")
        enddate = self.request.get("enddate")

#         if( uniqueID == None):
#             uniqueID = ""
        
        
# #         uniqueID2 = self.session.get("uniqueID")
#         logging.info(uniqueID)
        aa = AdminApi()
        responseData = aa.GetAudiosListByDate(offset, limit, startdate, enddate)
        
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)    

class GetVideoLinksBydate(BaseSessionHandler):
    def get(self):
        offset = self.request.get("offset")
        limit = self.request.get("limit")
        startdate = self.request.get("startdate")
        enddate = self.request.get("enddate")

#         if( uniqueID == None):
#             uniqueID = ""
        
        
# #         uniqueID2 = self.session.get("uniqueID")
#         logging.info(uniqueID)
        aa = AdminApi()
        responseData = aa.GetVideoLinksBydate(offset, limit, startdate, enddate)
        
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)


class UpdateVideosObject(BaseSessionHandler):
    def get(self):

        aa = AdminApi()
        responseData = aa.UpdateVideosObject()
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        return self.response.write(responseData)


class UpdateAudiosObject(BaseSessionHandler):
    def get(self):

        aa = AdminApi()
        responseData = aa.UpdateAudiosObject()
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        return self.response.write(responseData)



class UpdateUserObject(BaseSessionHandler):
    def get(self):

        aa = AdminApi()
        responseData = aa.UpdateUserObject()
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"
        return self.response.write(responseData)

class UpdateVideo(BaseSessionHandler):
    def post(self):
        VideoCat = self.request.get("cat")
        vidUrl = self.request.get("vidurl")
        aa = AdminApi()
        responseData = aa.ModifyVideoMetadata(vidUrl, VideoCat)
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class UpdateAudio(BaseSessionHandler):
    def post(self):
        audioKey = self.request.get("audkey")
        AudioName = self.request.get("audName")
        AudioLang = self.request.get("audLang")
        starttime = self.request.get("starttime")
        logging.info(audioKey)
        aa = AdminApi()
        responseData = aa.ModifyAudioMetadata(audioKey, AudioName, AudioLang, starttime)
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class UpdateUserLangauges(BaseSessionHandler):
    def get(self):
        langs = self.request.get("langs")
        handle = self.request.get("handle")
        uniqueID = self.session.get("uniqueID")
        logging.info(langs)
        if(uniqueID == None):
            uniqueID = ""
        ua = UsersApi()
        responseData = ua.UpdateUserLanguages(uniqueID, langs)

        # if(responseData.get("newName") != None):
        #     self.session["userDisplayName"] = responseData.get("newName")
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)

class DeleteVideosObject(BaseSessionHandler):
    def post(self):
        # VideoCat = self.request.get("cat")
        vidUrl = self.request.get("vidurl")
        aa = AdminApi()
        responseData = aa.DeleteVideosObject(vidUrl)
        responseData = json.dumps(responseData)
        host = self.request.headers.get("Origin")
        self.response.headers["Content-Type"] = "application/json"
        if(host != None):
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Credentials"] = "true"

        return self.response.write(responseData)


application = webapp2.WSGIApplication([

#   (r'/ui/gallery',LoadMainPage),
#   (r'/ui/studio',LoadStudioPage),
# User activity APIs
  (r'/user/loginnStatus', UserLoginStatus),
  (r'/user/logsIn', UserLogsIn),
  (r'/user/logsOut', UserLogsOut),
  (r'/user/registers', UserRegisters),
  (r'/user/votes', UserVotesAnAudio),
  # (r'/user/uploadsAnAudio',UserUploadsAnAudio),
  # (r'/user/addsVideo',UserAddsVideo),
  (r'/getAudiosList', GetAudiosList),
  (r'/getAudioChunksList', GetAudioChunksList),
  
  (r'/getVideoLinks', GetVideoLinks),
  (r'/getYoutubeVideoDetails', GetYoutubeVideoDetails),
#   (r'/postAudio',PostAudio),
#   (r'/VoteAudio',VoteAudio),
  (r'/addNewVideo', AddNewVideo),
  (r'/addNewAudio', AddNewAudio),
  (r'/addNewAudioChunk', AddNewAudioChunk),
  (r'/addNewSrt', AddNewSrt),
  (r'/getAudioBlobByKey', GetAudioBlobByKey),
  (r'/getSrtBlobByKey', GetSrtBlobByKey),
  (r'/getaudiodetails', GetAudioDetails),
  (r'/getaudiochunkdetails', GetAudioChunkDetails),
  (r'/increaseviewcount', IncreaseViewCount),
  (r'/getVideoDetails', GetVideoDetails),
  (r'/getSrtBlobByVideoURL', GetSrtBlobByVideoURL),
  (r'/searchvideo', GetVideoSearch),
  (r'/searchaudio', GetAudioSearch),
  
  (r'/getburl', GetBlobUrl),
  (r'/getSrtUrl', GetSrtUrl),
  (r'/redirect', redirectToStudio),
  (r'/downloadaudio', DownLoadAudio),
  (r'/audio/update', UpdateAudio),
  (r'/video/update', UpdateVideo),


  # user profile apis
  (r'/user/checkUserHandleAvailability', UserHandleAvailability),
  (r'/user/updateUserName', UpdateUserDisplayName),
  (r'/user/userDetailsByhandle', GetUserDetailsByHandle),
  (r'/user/updateuserlangauges', UpdateUserLangauges),
  

   
  # admin apis
  (r'/getAudiosListByDate', GetAudiosListByDate),
  (r'/getVideoLinksBydate', GetVideoLinksBydate),
  # (r'/modifyVideoMetadata',ModifyVideoMetadata),
  # (r'/modifyAudioMetadata',ModifyAudioMetadata),

  

  
  # updateApis  ,ENABLE ONLY WHEN NEEDED

  (r'/updateVideos', UpdateVideosObject),
  (r'/updateAudios', UpdateAudiosObject),
  (r'/updateUser', UpdateUserObject),


  # delete Apis
  (r'/deleteVideos', DeleteVideosObject),
  # (r'/deleteAudios',DeleteAudiosObject),



  # (r'/user/recordedAudioList',UserAudioList),
#   (r'/(\w+)',LoadOtherPages),

], config=config, debug=False)




