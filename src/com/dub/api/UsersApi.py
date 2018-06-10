
from com.dub.database.UserDetailsAccess import UserDetailsAccess


# from com.dub.database.BrandReportDataAccess import BrandReportDataAccess
class UsersApi:
    
    

    def getTimestamp(self):
#        midnight = datetime.combine((datetime.now()+ root.timedelta(hours=5,minutes=30)), time.max)
#        return mktime(midnight.timetuple())
        return 7200
    
    
    def __init__(self):
        return
    
    def checkIfUserExists(self, uniqueID, userName):
#         responseData = dict()
        uda = UserDetailsAccess()
        responseData = uda.checkIfUserExists(uniqueID, userName)
        return responseData


    def RegisterNewUser(self, uniqueID, userName):
        uda = UserDetailsAccess()
        responseData = uda.RegisterNewUser(uniqueID, userName)
        return responseData
    
    def UserVotesAnAudio(self, audioKeys, direction, uniqueID):
        uda = UserDetailsAccess()
        responseData = uda.UserVotesAnAudio(audioKeys, direction, uniqueID)
        return responseData

    def UserHandleAvailability(self, handle, uniqueID):
        uda = UserDetailsAccess()
        responseData = uda.UserHandleAvailability(handle, uniqueID)
        return responseData

    def UpdateUserDisplayName(self, uniqueID, newName):
        uda = UserDetailsAccess()
        responseData = uda.UpdateUserDisplayName(uniqueID, newName)
        return responseData        

    def GetUserDetailsByHandle(self, handle):
        uda = UserDetailsAccess()
        responseData = uda.GetUserDetailsByHandle(handle)
        return responseData    

    def UpdateUserLanguages(self, uniqueID, langs):
        uda = UserDetailsAccess()
        responseData = uda.UpdateUserLanguages(uniqueID, langs)
        return responseData                    
