from StringIO import StringIO
import json
from urllib2 import urlopen, URLError


# from VideoDetails import VideoDetails
class YTDetailsFetcher(object):

    """
    Class the fetch the video details from youtube
    """
    YT_ID_PLACEHOLDER = "{ytid}"

    GOOGLE_API_KEY = "AIzaSyBDXFQuMlnhWE_wRP04KWxny4HlPM8N8EQ"

    def __init__(self, \
        customYTDetailsEndpoint="https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ytid}&key="):
        self._yt_details_endpoint = customYTDetailsEndpoint


    def get_details(self, ytId):
        request = self._yt_details_endpoint.replace(self.YT_ID_PLACEHOLDER, ytId) + self.GOOGLE_API_KEY
        print request
        try:
            response = urlopen(request).read()
            data = json.load(StringIO(response))
            video_details = {}
            item = data['items'][0]
            print item
            video_details["name"] = item['snippet']['title']
            video_details["ytID"] = ytId
            print video_details
            return video_details

        except URLError, error:
            print 'Error fetching details to youtube:', error
            raise Exception("Youtube isn't talking to us :( ")
