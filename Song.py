from datetime import date

from Logger import Logger
from Artist import Artist 


class Song:
    """
    This class is used to s`tore the data of a song.
    """

    __slots__ = ["__id" , "__name" , "__dateMade" , "__imgLink" , "__dateAdded" , "__artistList"]

    def __init__(self , id:str, 
                 name:str = None, 
                 dateMade: str|date = None,
                 imgLink:str = None,
                 dateAdded: str|date = None,
                 artistList: list[Artist] = None):
        
        self.setID(id)
        self.setName(name)
        
        self.setDateMade(dateMade)
        self.setImgLink(imgLink)
        self.setDateAdded(dateAdded)

        self.setArtistList(artistList)

    def __repr__(self) -> str:
        if (self.getName() == None):
            return f"Song: {self.getID()}"
        return f"Song: {self.getName()} , ID: {self.getID()}"

    def __hash__(self) -> int:
        return hash(self.getID())
    
    def __eq__(self , other) -> bool:
        if ( not isinstance(other , Song) ):
            return False
        
        return self.getID() == other.getID()
    
    def __dict__(self) -> dict:
        return {
            "id": self.getID(),
            "name": self.getName(),
            "dateMade": self.getDateMade(),
            "imgLink": self.getImgLink(),
            "dateAdded": self.getDateAdded()
        }


    #* BASIC GETTERS AND SETTERS *#
    def getID(self) -> str:
        return self.__id
    
    def setID(self , id:str) -> None:
        self.__id = id

    def getName(self) -> str:
        return self.__name
    
    def setName(self , name:str | None) -> None:
        if (name and len(name) > 255):
            name = name[:255]
        self.__name = name

    def getDateMade(self) -> str:
        return self.__dateMade  
    
    def setDateMade(self , dateMade:str | date) -> None:
        if (type(dateMade) == str):
            splitDate = dateMade.split("T")
            if (len(splitDate) == 2):
                dateMade = splitDate[0]

            splitDateWithoutTime = dateMade.split("-")
            if (len(splitDateWithoutTime) == 2):

                dateMade = f"{splitDateWithoutTime[0]}-{splitDateWithoutTime[1]}-01"
                
        self.__dateMade = dateMade

    def getImgLink(self) -> str:
        return self.__imgLink
    
    def setImgLink(self , imgLink:str|None) -> None:
        if (imgLink and len(imgLink) > 200):
            imgLink = None
            Logger().warn(f"Image link for {self.getName()} is too long. Setting to None.")

        self.__imgLink = imgLink

    def getDateAdded(self) -> str:
        return self.__dateAdded
    
    def setDateAdded(self , dateAdded:str | date) -> None:

        if (type(dateAdded) == str):
            splitDate = dateAdded.split("T")
            if (len(splitDate) == 2):
                dateAdded = splitDate[0]

        self.__dateAdded = dateAdded

    def getArtistList(self) -> list[Artist]:
        return self.__artistList
    
    def setArtistList(self , artistList:list[Artist]) -> None: 
        self.__artistList = artistList
    


    