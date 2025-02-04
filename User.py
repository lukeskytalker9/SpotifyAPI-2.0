from SpotifyAccessor import SpotifyAccessor
from SQLObject import SQLObject
from Authority import Authority

from Playlist import Playlist
from SpotifyPlaylist import SpotifyPlaylist
from PlaylistComparator import PlaylistComparator


class User(SpotifyAccessor):

    __slots__  = [
        '__userID',
        '__username',
        '__profilePhotoURL',

        '__authority',

        '__genPlaylist',
        '__databasePlaylist',

        '__authorizationsToken',
    ]

    def __init__(self , access_token):
        super().__init__(access_token)

        userData = self.getUserDataFromSpot()

        self.__setUserID(userData['userID'])
        self.__setUsername(userData['username'])
        self.__setProfilePhotoURL(userData['profilePhotoURL'])


        sql = SQLObject()
        sqlUserData = sql.getUserDataFromSQL(self.getUserID())

        self.__setAuthority(sqlUserData['authority'])

        self.setGenPlaylist(Playlist(sqlUserData['genPlaylist']))
        self.setDatabasePlaylist(Playlist(sqlUserData['databasePlaylist']))
       
        self.setAccessToken(access_token)


    def getValidPlaylist(self) -> set[Playlist]:

        sql = SQLObject()
        unwantedPlaylistIDs = sql.getUnwantedPlaylists(self.getUserID())

        def iterationFunction(x):
            if (x['images'] == None):
                return Playlist(x['id'] , x['name'] , None , x['snapshot_id'])
            return Playlist(x['id'] , x['name'] , x['images'][0]['url'] , x['snapshot_id'])
    
        #Get Playlists FROom SPotify
        setOfPlaylists = self.iterateThroughPagination(self.current_user_playlists() , iterationFunction)
        
        setOfPlaylists = setOfPlaylists - unwantedPlaylistIDs
        
        #This is to see if removing gen/database was even there
        setOfPlaylists.discard(self.getGenPlaylist())
        setOfPlaylists.discard(self.getDatabasePlaylist())

        return setOfPlaylists


    def __repr__(self) -> dict:
        return self.getUserData()
    

    def getUserData(self) -> dict:
        package = {
            "userID": self.getUserID(),
            "username": self.getUsername(),
            "profilePhotoURL": self.getProfilePhotoURL(),
            "authority": self.getAuthority().getPackage(),
        }
        return package
    
    def updateData(self , additionalUnwantedPlaylists: list[str] = []) -> None:

        validPlaylistSet = self.updatePlaylists(additionalUnwantedPlaylists = additionalUnwantedPlaylists)
        
        #Remove Playlists
        #sql = SQLObject()
        #sql.getPLa

        for playlist in validPlaylistSet:
            comparator = PlaylistComparator(playlist , self.getAccessToken())
            
            if (comparator.needsUpdate()):
                comparator.updateDatabase(self.getAccessToken())
        

    def updatePlaylists(self , additionalUnwantedPlaylists: list[str] = []) -> None:
        """
        Updates the playlists of the user. With all infromation from the Spotify API.
        """
        sql = SQLObject()
        if (len(additionalUnwantedPlaylists) > 0):
            additionalUnwantedPlaylists = [Playlist(playlistID) for playlistID in additionalUnwantedPlaylists]
            sql.makePlaylistUnwanted(self.getUserID() , additionalUnwantedPlaylists)


        #Get Playlists From SQL
        unwantedPlaylistsSet = sql.getUnwantedPlaylists(self.getUserID())
        wantedPlaylistsSet = sql.getWantedPlaylists(self.getUserID())

        # self.input_to_json(self.current_user_playlists() , "current_user_playlists.json")
        #Get Playlists From Spotify

        # print("Getting Playlists")
        # test1 = self.current_user_playlists()["items"][0]
        # self.input_to_json(test1 , "current_user_playlists.json")
        # print("x['id']" , test1['id'])
        # print("x['name']" , test1['name'])
        # print("x['images']" , test1['images'])
        # print("x['images'][0]['url']" , test1['images'][0]['url'])
        # print("x['snapshot_id']" , test1['snapshot_id'])
        # print("Ending ")

        def iterationFunction(x):
            if (x['images'] == None):
                return Playlist(x['id'] , x['name'] , None , x['snapshot_id'])
            return Playlist(x['id'] , x['name'] , x['images'][0]['url'] , x['snapshot_id'])
        
        setOfPlaylists = self.iterateThroughPagination(
            self.current_user_playlists() , 
            iterationFunction)

        #* Deal with gen and database playlists existing *#
        if (self.getGenPlaylist() in setOfPlaylists):
            setOfPlaylists.remove(self.getGenPlaylist())
        else:
            self.__createNewGenPlaylist()
        
        if (self.getDatabasePlaylist() in setOfPlaylists):
            setOfPlaylists.remove(self.getDatabasePlaylist())
        else:
            self.__createNewDatabasePlaylist()

        
        unwantedPlaylistsToDelete = unwantedPlaylistsSet - setOfPlaylists
        sql.removePlaylistFromSQL(unwantedPlaylistsToDelete)

        """
        Ok this for loop is stupid but here it is...

        I wanted to do:
        unwantedPlaylistsToUpdate =  setOfPlaylists & unwantedPlaylistsSet
        
        I want this to be the intersection between setOfPlaylists and unwantedPlaylistsSet with the objects
        in the setOfPlaylist Playlist objects as they have the spotify data. But the intersection function is 
        not order dependent. Meaning the order of intersecting a & b vs b & a does not change what objects are
        selected. What determines that is what set is smaller. So because unwantedPlaylist set is always smnaller
        because it is a subset of setOfPlaylists, the intersection will always be unwantedPlaylistsSet. So I have to
        add to unwantedPlaylistSet to make it larger as setOfPlaylists. I do this by adding a bunch of meaningless 
        playlists with IDS being the index of the loop. This is a hacky solution but it works.

        I hate this feature so much but I understand its for efficiency!
        
        """
        for i in range(len(setOfPlaylists) - len(unwantedPlaylistsSet)):
            unwantedPlaylistsSet.add(Playlist(str(i)))
        unwantedPlaylistsToUpdate =  unwantedPlaylistsSet & setOfPlaylists #unwantedPlaylistsSet - unwantedPlaylistsToDelete 
        
        # print("unwantedPlaylistSet" , unwantedPlaylistsSet)
        # print("unwantedPlaylistsToDelete" , unwantedPlaylistsToDelete)
        # print("unwantedPlaylistsToUpdate" , unwantedPlaylistsToUpdate)
        # print("len(unwantedPlaylistsToUpdate)" , len(unwantedPlaylistsToUpdate))
        
        sql.updatePlaylistDetails(unwantedPlaylistsToUpdate)

        
        
        #Remove unwanted playlists
        setOfPlaylists = setOfPlaylists - unwantedPlaylistsSet


        

        #At this point all unwanted playlists/ gen and database playlists have been removed
        playlistsToAdd = setOfPlaylists - wantedPlaylistsSet
        playlistsToRemove = wantedPlaylistsSet - setOfPlaylists

        # print("wantedPlaylistsSet" , wantedPlaylistsSet)
        # print("playlistsToAdd" , playlistsToAdd)
        # print("playlistsToRemove" , playlistsToRemove)
        
    
        self.__addPlaylist(playlistsToAdd)
        sql.removePlaylistFromSQL(playlistsToRemove)

        return setOfPlaylists

    def __createNewGenPlaylist(self) -> None:
        """
        Creates a new Gen Playlist
        """
        newPlaylistID = self.createNewGenplaylist(self.getUserID())

        sql = SQLObject()
        sql.updateGenPlaylist(self.getUserID() , newPlaylistID)

    def __createNewDatabasePlaylist(self) -> None:
        """
        Creates a new Database Playlist
        """
        newPlaylistID = self.createNewDatabasePlaylist(self.getUserID())

        sql = SQLObject()
        sql.updateDatabasePlaylist(self.getUserID() , newPlaylistID)

    def __addPlaylist(self , playlists: Playlist | set[Playlist | list[Playlist]]) -> None:
        """
        Adds a playlist to the SQL database and populates the playlists
        """
        sql = SQLObject()
        sql.addPlaylistToSQL(self.getUserID() , playlists)

        if (type(playlists) == Playlist):
            playlists = [playlists]

        for playlist in playlists:
            sp = SpotifyPlaylist(playlist)
            sp.loadSongs(self)

            sql.addSongToSQL(sp.getID() , sp.getSongSet())

    def addSongsToGenPlaylist(self, songIDList):
        return super().addSongsToGenPlaylist(self.getGenPlaylist().getID(), songIDList)



    """
    Simple Getters and Setters
    """
    def getUserID(self) -> str:
        return self.__userID
    
    def __setUserID(self , newUserID: str):
        self.__userID = newUserID

    def getUsername(self) -> str:
        return self.__username
    
    def __setUsername(self , newUsername: str):
        self.__username = newUsername

    def getProfilePhotoURL(self) -> str:
        return self.__profilePhotoURL
    
    def __setProfilePhotoURL(self , newProfilePhotoURL: str):
        self.__profilePhotoURL = newProfilePhotoURL

    def getAuthority(self) -> Authority:
        #return self.__authority
        return self.__authority

    def __setAuthority(self , newAuthority: Authority):
        self.__authority = newAuthority 

    def getGenPlaylist(self) -> Playlist:
        return self.__genPlaylist
    
    def setGenPlaylist(self , newGenPlaylist: Playlist):
        self.__genPlaylist = newGenPlaylist
    
    def getDatabasePlaylist(self) -> Playlist:
        return self.__databasePlaylist
    
    def setDatabasePlaylist(self , newDatabasePlaylist: Playlist):
        self.__databasePlaylist = newDatabasePlaylist
    
    def getAccessToken(self) -> dict:
        return self.__authorizationsToken
    
    def setAccessToken(self , newAccessToken: dict):
        self.__authorizationsToken = newAccessToken






if (__name__ == "!!__main__"):
    print("Now Beginning Tests For User.py")

    user = User(None)

    print("User.getUserData()" , user.getUserData())
    print(type(user.getAuthority()))

    #print("/////////////////Testing __getValidPlaylist/////////////////")
    #validPlaylistList = user.getValidPlaylist()
    #user.input_to_json(validPlaylistList , "getValidPlaylist.json")
    #print(len(validPlaylistList))


if (__name__ == "__main__"):
    user = User(None)

    
    
    print("user.getUserData()" , user.getUserData())
    print("user.getValidPlaylist()" , [playlist.getID() for playlist in user.getValidPlaylist()])
    
    ## L2L#1 , L2L#2 , L2L#3 , L2L#4 , L2L#5 , L2L#6 , L2L#7 , L2L#8 , L2L#9 , L2L#10 , L2L#11, L2L#12
    generalUnwantedPLaylists = ["4TjzxhnkEVeuHluwRxcTjK", 
                                "2lr5WAKVUih78U3uAwVANK", 
                                "6m5NFn4obowHqouRcwuvWz",
                                "4n32bH9cjghdYqupNPFgi4", 
                                "71VWfO07IkVh5RenBgPxTB", 
                                "4Fih0nG0y1bDpHxhdi2YhE", 
                                "6gKIdDIswcHqeQeq5oqf59",
                                "70ygsIiRD0ArRuyMi5Di7q", 
                                "32sgrn4S4vU6kQtHLXYsNx", 
                                "7Drs4yW3iJNMLbk0TZu8n4", 
                                "7HI1SXk32pncvIoiC14M5t",
                                "3WYaAD1KZ7N5vZY1hsR06N"]
    
    #Syd and Jack songs that are sad but sometimes happy
    generalUnwantedPLaylists.append("2moFFFfrTnzHoznOjWeMag")
    #Songs that strangely remind me of you… huh
    generalUnwantedPLaylists.append("4wGOSeNyEyTvJY3C5v97h9")
    #Little Insignificant Speck
    generalUnwantedPLaylists.append("7duqrK1ZecXNWbderKzd0n")
    
    

    user.updateData(generalUnwantedPLaylists)
    
    
    