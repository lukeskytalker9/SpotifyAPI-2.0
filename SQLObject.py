from __future__ import annotations
import pyodbc

from Authority import Authority
from Song import Song
from Artist import Artist
from Playlist import Playlist
from Logger import Logger
from ListeningHistoryStripper import ListeningHistoryStripper

from dotenv import load_dotenv
import os

load_dotenv()

"""
This is a wrapper to the SQL Database that is a singleton
This singlton format will be implemented as a pool if expanding

Simple methods will be added here that just involve the database
"""
class SQLObject:

    __instance:SQLObject = None

    """
    This code limits the class to only be made in a 
    singlton format

    !WARNING!
    I don't understand this code entirely expecially
    the cls argument and why it is passed in a second
    time.
    """
    def __new__(cls):
        if ( cls.__instance == None ):
            cls.__instance = super(SQLObject , cls).__new__(cls)

        return cls.__instance
    


    """
    Atributes list
    """
    __slots__ = ["__cursor" , "__queryManager"]

    def __init__(self):
        self.__cursor = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                f'Server={self.__getServer()};'
                f'Database={self.__getDatabase()};'
                'Trusted_Connection=yes;')
        
    
    def __call__(self , command:str , variables:tuple) -> list:
        return self.__cursor.execute(command , variables)
    
    def commit(self) -> None:
        self.__getCursor().commit()
    
    def rollback(self) -> None:
        self.__getCursor().rollback()

    def close(self):
        self.__getCursor().close()
        self.__instance = None


    def __getCursor(self) -> pyodbc.Cursor:
        return self.__cursor

    def getUserDataFromSQL(self , userID) -> dict:
        command = "SELECT * FROM users WHERE userID = ?"
        
        sqlUserData = self(command , (userID,)).fetchone()

        authorityStr = sqlUserData[1]

        returnDict = {
           "authority": None, 
           "genPlaylist": sqlUserData[2],
           "databasePlaylist": sqlUserData[3],
        }
        
        for authority in Authority:
            if (authorityStr == str(authority)):
                returnDict["authority"] = authority
                break
        
        return returnDict

    def getUnwantedPlaylists(self , userID) -> set[str]:
        command = "SELECT playlistID FROM playlists WHERE userID = ? and isUnwanted = 1"

        funckyPlaylistList = self(command , (userID,)).fetchall()

        playlistIDSet = {Playlist(playlistID[0]) for playlistID in funckyPlaylistList}

        return playlistIDSet
    
    def getWantedPlaylists(self , userID) -> set[str]:
        command = "SELECT playlistID FROM playlists WHERE userID = ? and isUnwanted = 0"

        funckyPlaylistList = self(command , (userID,)).fetchall()

        playlistIDSet = {Playlist(playlistID[0]) for playlistID in funckyPlaylistList}

        return playlistIDSet

    def getPlaylistDataFromSQL(self , playlistID) -> dict:
        command = "SELECT * FROM playlists WHERE playlistID = ?"
        #print(playlistID)
        playlistData = self(command , (playlistID,)).fetchone()
        #print(playlistData)
        return {
            "playlistID": playlistData[0],
            "playlistName": playlistData[2],
            "playlistImage": playlistData[3],
            "snapshotID": playlistData[4],
        }
    
    def getSongSetFromSQL(self , playlistID) -> set[Song]:

        command = "SELECT s.songID, s.songName, s.dateMade, s.imgLink, psl.dateAdded FROM songs s INNER JOIN playlistSongLink psl ON s.songID = psl.songID WHERE psl.playlistID = ?;"

        songSet = self(command , (playlistID,)).fetchall()

        returnSet = set()

        for item in songSet:
            returnSet.add(Song(item[0] , name=item[1] , dateMade=item[2] , imgLink=item[3] , dateAdded=item[4]))


        return returnSet
    
    def addPlaylistToSQL(self , userID: str , playlists:Playlist | list[Playlist] | set[Playlist]) -> None:
        """
        Adds playlists to the SQL database.
        
        Parameters
        ----------
            userID : (str) The spotify userID of the user which can be found in database or spotify.
            param2 : (Playlist | list[Playlist] | set[Playlist]) The playlist or playlists to be added to the database.
        
        Exceptions
        ----------       
        """
        command = "INSERT INTO playlists (playlistID , userID , playlistName , playlistImgURL , playlistSnapshotID) VALUES (? , ? , ? , ? , ?)"
        
        if (type(playlists) == Playlist):
            playlists = [playlists]
        
        try:
            for playlist in playlists:
                playlist: Playlist
                self(command , (playlist.getID() , userID , playlist.getName() , playlist.getImgURL() , playlist.getSnapshotID()))
            
            self.commit()
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when adding playlist: " + playlist.getID() + " to SQL:\n" + str(e))

    def removePlaylistFromSQL(self , playlists:Playlist | list[Playlist] | set[Playlist]) -> None:
        
        removingLinkCommand = "DELETE FROM playlistSongLink WHERE playlistID = ?"
        removingPlaylistCommand = "DELETE FROM playlists WHERE playlistID = ?"
        
        if (type(playlists) == Playlist):
            playlists = [playlists] 

        try:    
            for playlist in playlists:

                playlist: Playlist

                #Remove songPlaylistLink (but not songs in playlist)
                self(removingLinkCommand , (playlist.getID(),))

                #Remove playlist Data (This has to go second becasue keys)
                self(removingPlaylistCommand , (playlist.getID(),))
            
            self.commit()
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when removing playlist: " + playlist.getID() + " from SQL:\n" + str(e))

    def addSongToSQL(self , playlistID:str , songs:Song | list[Song] | set[Song]) -> None:
        """
        This method adds songs to the SQL database.
        """
        
        if (len(songs) == 0):
            return
        
        if (type(songs) == Song):
            songs = [songs]

        checkSongInSQLCommand = "SELECT COUNT(1) FROM songs WHERE songID = ?;"
        addSongToSongsCommand = "INSERT INTO songs (songID , songName , dateMade , imgLink) VALUES (? , ? , ? , ?);"
        addSongPlaylisLinkCommand = "INSERT INTO playlistSongLink (playlistID , songID , dateAdded) VALUES (? , ? , ?);"
        
        try:
            for song in songs:
                song: Song

                numberOfInstances = self(checkSongInSQLCommand , (song.getID(),)).fetchone()[0]
                #If song is not already in db add to songs not just playlistSongLink
                if (numberOfInstances < 1):
                    self(addSongToSongsCommand , (song.getID() , song.getName() , song.getDateMade() , song.getImgLink()))
                    
                    self.__addArtistToSQL(song.getID() , song.getArtistList())


                #If song has multiple instances throw warning to review later
                if (numberOfInstances > 1):
                    Logger().warn(f"Song: {song.getID()} already in database is being added to playlist: {playlistID}")


                #At this point song is in songs table so add to playlistSongLink
                self(addSongPlaylisLinkCommand , (playlistID , song.getID() , song.getDateAdded()))
                    
            
            self.commit()
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when adding song: " + song.getName() + " (" + song.getID() + "), DateTime: " + str(type(song.getDateAdded())) + " " + song.getDateMade() + " SQL:\n" + str(e))

    def removeSongFromSQL(self , playlistID:str , songs:Song | list[Song] | set[Song]) -> None:
        """
        This method removes songs from the SQL database.
        
        **Note:** This only removes the song from the playlistSongLink table. Not the songs data.
        """
        if (len(songs) == 0):
            return
        
        if (type(songs) == Song):  
            songs = [songs]
        
        removingLinkCommand = "DELETE FROM playlistSongLink WHERE playlistID = ? AND songID = ?"
        
        try:
            for song in songs:
                song: Song

                self(removingLinkCommand , (playlistID , song.getID()))
                    
            
            self.commit()
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when removing song: " + song.getID() + " from SQL:\n" + str(e))
    
    def updateGenPlaylist(self , userID:str , genPlaylistID:str) -> None:
        
        updateUserGenPlaylistCommand = "UPDATE users SET genPlaylistID = ? WHERE userID = ?;"

        try:
            self(updateUserGenPlaylistCommand , (genPlaylistID , userID))
            self.commit()
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when updating genPlaylistID for user: " + userID + " in SQL:\n" + str(e))

    def updateDatabasePlaylist(self , userID:str , databasePlaylistID:str) -> None:
        
        updateUserDatabasePlaylistCommand = "UPDATE users SET databasePlaylistID = ? WHERE userID = ?;"

        try:
            self(updateUserDatabasePlaylistCommand , (databasePlaylistID , userID))
            self.commit()
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when updating databasePlaylistID for user: " + userID + " in SQL:\n" + str(e))
        
    def updatePlaylistData(self , playlistID:str , playlistName:str , playlistImgURL:str , playlistSnapshotID:str) -> None:
        """
        This updates database playlist data to be up to date with spotify including snapshotID
        """
        updatePlaylistCommand = "UPDATE playlists SET playlistName = ? , playlistImgURL = ? , playlistSnapshotID = ? WHERE playlistID = ?;"

        try:
            self(updatePlaylistCommand , (playlistName , playlistImgURL , playlistSnapshotID , playlistID))
            self.commit()
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when updating playlist: " + playlistID + " in SQL:\n" + str(e))

    def makePlaylistUnwanted(self , userID:str , playlists:Playlist | list[Playlist] | set[Playlist] ) -> None:

        if (type(playlists) == Playlist):
            playlists = [playlists]

        try:
            for playlist in playlists:
                playlist: Playlist

                #Check if playlist is already in playlists
                numberOfInstancesCommand = "SELECT COUNT(1) FROM playlists WHERE playlistID = ?;"
                numberOfInstances = self(numberOfInstancesCommand , (playlist.getID(),)).fetchone()[0]
                # print("playlistID: " , playlist.getID())
                # print("playlistName: " , playlist.getName())
                # print("number of instances: " , str(numberOfInstances))
                # print("/////////////////////")

                if (numberOfInstances > 1):
                    Logger().fatal(f"Playlist: {playlist.getName()} ({playlist.getID()}) is in database more than once. Please review.")
                elif (numberOfInstances == 1):
                    makePlaylistUnwantedCommand = "UPDATE playlists SET isUnwanted = 1 WHERE playlistID = ?;"
                    self(makePlaylistUnwantedCommand , (playlist.getID(),))
                    
                else:
                    insertPlaylistCommand = "INSERT INTO playlists (playlistID , userID , playlistName , playlistImgURL , playlistSnapshotID , isUnwanted) VALUES (? , ? , ? , ? , ? , 1);"
                    self(insertPlaylistCommand , (playlist.getID() , userID , None , None , None))

                self.commit()
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when making playlist unwanted in SQL:\n" + str(e))

    def updatePlaylistDetails(self , playlists:Playlist | list[Playlist] | set[Playlist]) -> None:
        """
        Updates playlist details in the SQL database without influencing songs. 
        This code is being written to update unwanted playlist names, image, and other details
        to be accuratly visible to user when pulled so they know the playlist blocked.
        """
        if (type(playlists) == Playlist):
            playlists = [playlists]
        
        try:
            for playlist in playlists:
                playlist: Playlist

                updateCommand = "UPDATE playlists SET playlistName = ? , playlistImgURL = ? , playlistSnapshotID = ? WHERE playlistID = ?;"
                self(updateCommand , (playlist.getName() , playlist.getImgURL() , playlist.getSnapshotID() , playlist.getID()))
                self.commit()
        
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when updating playlist details in SQL:\n" + str(e))

    def addListeningHistoryToSQL(self , lH:ListeningHistoryStripper) -> None:

        if (lH.length() == 0):
            Logger().warn("ListeningHistoryStripper is empty. No history to add to SQL.")
            return
        
        if (lH.peek().isFiller()):
            pass

        userID = lH.getUserID()

        sessionID = self( "SELECT MAX(sessionID) FROM listeningHistory WHERE userID = ?;" , (userID,)).fetchone()[0]
        sessionID = 0 if sessionID == None else sessionID
        
        numberInSession = self( "SELECT MAX(numberInSession) FROM listeningHistory WHERE userID = ? AND sessionID = ?;" , (userID , sessionID)).fetchone()[0]
        numberInSession = 0 if numberInSession == None else numberInSession
        try:
            for _ in range(lH.length()):
                song = lH.pop()
                numberInSession += 1

                #If song is filler then a new session starts
                if (song.isFiller()):
                    sessionID += 1
                    numberInSession = 0

                addingFillerCommand = "INSERT INTO listeningHistory (sessionID , numberInSession , timeListened , userID , songID , isInDatabase , isFiller) VALUES (? , ? , ? , ? , ? , ? , ?);"
                if (song.getID() == None):
                    isInDatabase = 0
                else:
                    isInDatabase = 1 if self.isSongInSQL(song.getID()) else 0
                
                isFiller = 1 if song.isFiller() else 0
                self(addingFillerCommand , (sessionID , numberInSession , song.getTimeListened() , userID , song.getID() , isInDatabase , isFiller))
            
            self.commit()
        except pyodbc.Error as e:
            self.rollback()
            raise pyodbc.Error("Error when adding history to listeningHistory to SQL:\n" + str(e))
        

    def isSongInSQL(self , songID:str) -> bool:
        command = "SELECT COUNT(1) FROM songs WHERE songID = ?;"
        return self(command , (songID,)).fetchone()[0] > 0

    def getLastHistoryTime(self , userID:str) -> str:
        command = "SELECT MAX(timeListened) FROM listeningHistory WHERE userID = ?;"
        return self(command , (userID,)).fetchone()[0]

    def __addArtistToSQL(self , songID:str , artists:Artist | list[Artist] | set[Artist]) -> None:
        """
        Warning
        -------
        This method does not commit() after completion. This is because it is mainly just run in
        addSongToSQL which commits after all songs are added. This is to prevent multiple commits.

        Because it does not commit it does not rollback on error. This is because it is run in addSongToSQL
        """
        if (len(artists) == 0):
            return

        if (type(artists) == Artist):
            artists = [artists]

        
        checkArtistInSQLCommand = "SELECT COUNT(1) FROM artists WHERE artistID = ?;"    
        addArtistToArtistsCommand = "INSERT INTO artists (artistID , artistName) VALUES (? , ?);"
        addArtistSongLinkCommand = "INSERT INTO artistSongLink (songID , artistID) VALUES (? , ?);"
        try:    
            for artist in artists:  
                artist: Artist

                numberOfInstances = self(checkArtistInSQLCommand , (artist.getID(),)).fetchone()[0]

                if (numberOfInstances < 1):
                    self(addArtistToArtistsCommand , (artist.getID() , artist.getName()))
                
                if (numberOfInstances > 1):
                    Logger().warn(f"Artist: {artist.getID()} already in database is being added to song: {songID}")

                self(addArtistSongLinkCommand , (songID , artist.getID()))

        except pyodbc.Error as e:
            raise pyodbc.Error("Error when adding artist: " + artist.getName() + " (" + artist.getID() + ") to SQL:\n" + str(e))
            

    def __getServer(self) -> str:
        #return 'JEBPROJECTCOMP'
        return os.getenv("SQL_SERVER")
    
    def __getDatabase(self) -> str:
        return os.getenv("SQL_DATABASE")
    
        




if (__name__  == "__main__"):

    print("Now Beginning Tests For SQLObject.py")
    sql = SQLObject()
    sql2 = SQLObject()
    print(sql is sql2)

    #test getUserData
    print(sql.getUserDataFromSQL('px1a3vhak2udchyl4dcug9s4y'))

    userID = 'px1a3vhak2udchyl4dcug9s4y'
    sessionNumber = sql( "SELECT MAX(sessionID) FROM listeningHistory WHERE userID = ?;" , (userID,)).fetchone()[0]
    numberInSession = sql( "SELECT MAX(numberInSession) FROM listeningHistory WHERE userID = ? AND sessionID = ?;" , (userID , sessionNumber)).fetchone()[0]
        
    print(sessionNumber)

    print(numberInSession)
