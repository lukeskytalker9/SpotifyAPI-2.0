from Playlist import Playlist
from SQLObject import SQLObject

class DatabasePlaylist(Playlist):

    def __init__(self , playlistShell: Playlist):  
        super().__init__(playlistShell.getID() , None , None , None)
        self.loadIDData()


    def loadIDData(self) -> None:
        sql = SQLObject()
        sqlDataDict = sql.getPlaylistDataFromSQL(self.getID())

        self.setName(sqlDataDict['playlistName'])
        self.setImgURL(sqlDataDict['playlistImage'])
        self.setSnapshotID(sqlDataDict['snapshotID'])


    def loadSongs(self) -> None:

        sql = SQLObject()

        songSet = sql.getSongSetFromSQL(self.getID())

        self.setSongSet(songSet)
