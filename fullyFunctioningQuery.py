from User import User
from Query import Query

#This file is just temporary to use existing querying methods
#If you with to update database update unwanted playlist and then run the user file

if (__name__ == "__main__"):

    user = User(None)

    #This dict is uneeded but good for personal reference
    queryDict = {
        "dateMadeAfter": None,
        "dateMadeBefore": None,
        "artistList": [],
        "dateAddedAfter": None,
        "dateAddedBefore": None,
    }

    artistNameList = ["Travis Scott"]
    if (artistNameList != None or len(artistNameList) != 0):
        for artistName in artistNameList:
            queryDict["artistList"].append(user.getArtistID(artistName))
    
    print(queryDict)

    q = Query(user.getUserID() , **queryDict)
    songIDList = q.execute()

    user.addSongsToGenPlaylist(songIDList)
    #user.removeAllSongsFromPlaylist(user.getGenPlaylist().getID())