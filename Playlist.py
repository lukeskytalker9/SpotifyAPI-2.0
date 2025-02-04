import json
from Song import Song

class Playlist(json.JSONEncoder):

    __slots__ = [
        '__id',
        '__name',
        '__imgURL',
        '__snapshotID',
        '__songSet',
    ]

    def __init__(self , id:str , name:str = None , imgURL:str = None , snapshotID:str = None):
        self.setID(id)
        self.setName(name)
        self.setImgURL(imgURL)
        self.setSnapshotID(snapshotID)

        self.__songSet = set()


    def __hash__(self) -> int:
        return hash(self.getID())


    def __eq__(self , other) -> bool:
        #If other is not a playlist
        if ( not isinstance(other , Playlist) ):
            return False
        
        return self.getID() == other.getID()
    

    def __dict__(self) -> dict:
        return {
            "id": self.getID(),
            "name": self.getName(),
            "imgURL": self.getImgURL(),
            "snapshotID": self.getSnapshotID(),
        }
    
    def __repr__(self) -> str:
        return str(self.getID()) + " - " + str(self.getName())
    

    def __sub__(self , other) -> set:
        if ( not isinstance(other , Playlist) ):
            raise TypeError("Can only add Playlist objects")
            
        return self.getSongSet() - other.getSongSet()    


    def addSong(self , songs:Song | set[Song]) -> None:
        if (type(songs) == Song):
            self.__songSet.add(songs)
        else:
            self.__songSet = self.__songSet.union(songs)

    
    """
    Simple Getters and Setters
    """
    def getID(self) -> str:
        return self.__id
    
    def setID(self , id:str) -> None:
        self.__id = id

    def getName(self) -> str:
        return self.__name
    
    def setName(self , name:str) -> None:  
        self.__name = name

    def getImgURL(self) -> str:
        return self.__imgURL
    
    def setImgURL(self , imgURL:str) -> None:
        self.__imgURL = imgURL

    def getSnapshotID(self) -> str:
        return self.__snapshotID
    
    def setSnapshotID(self , snapshotID:str) -> None:
        self.__snapshotID = snapshotID

    def getSongSet(self) -> set[Song]:
        return self.__songSet
    
    def setSongSet(self , songSet:set[Song]) -> None:
        self.__songSet = songSet
    

    