from SQLObject import SQLObject
from SpotifyAccessor import SpotifyAccessor

from Playlist import Playlist  
from DatabasePlaylist import DatabasePlaylist
from SpotifyPlaylist import SpotifyPlaylist


class PlaylistComparator(SpotifyAccessor):

    __slots__ = [   
        '__databasePlaylist',
        '__spotifyPlaylist',
    ]

    def __init__(self , playlistShell: Playlist, authorizationToken):
        super().__init__(authorizationToken)

        databasePlaylist = DatabasePlaylist(playlistShell)

        self.__setDatabasePlaylist(databasePlaylist)

        spotifyPlaylist = SpotifyPlaylist(playlistShell)

        self.__setSpotifyPlaylist(spotifyPlaylist)


    def needsUpdate(self) -> bool:
        return self.__getDatabasePlaylist().getSnapshotID() != self.__getSpotifyPlaylist().getSnapshotID()
    


    def updateDatabase(self , authorizationToken: dict) -> None:
        """
        Method updates the database with all the important infromation from the spotify playlist
        """
        spotPlaylist = self.__getSpotifyPlaylist()
        spotPlaylist.loadSongs(SpotifyAccessor(authorizationToken))

        dataPlaylist = self.__getDatabasePlaylist()
        dataPlaylist.loadSongs()

        
        songsToRemove = dataPlaylist.getSongSet() - spotPlaylist.getSongSet()
        songsToAdd = spotPlaylist.getSongSet() - dataPlaylist.getSongSet()


        sql = SQLObject()
        sql.addSongToSQL(dataPlaylist.getID() , songsToAdd)
        sql.removeSongFromSQL(dataPlaylist.getID() , songsToRemove)

        #Here is where playlist data is updated (name, img, etc)
        sql.updatePlaylistData(dataPlaylist.getID() , spotPlaylist.getName() , spotPlaylist.getImgURL() , spotPlaylist.getSnapshotID())
    

    
    
    """
    Simple Getters and Setters
    """
    def __getDatabasePlaylist(self) -> DatabasePlaylist:
        return self.__databasePlaylist
    
    def __setDatabasePlaylist(self , playlistID: DatabasePlaylist):
        self.__databasePlaylist = playlistID

    def __getSpotifyPlaylist(self) -> SpotifyPlaylist:
        return self.__spotifyPlaylist
    
    def __setSpotifyPlaylist(self , playlistID: SpotifyPlaylist):
        self.__spotifyPlaylist = playlistID

    