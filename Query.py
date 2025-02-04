from datetime import date

from Logger import Logger
from SQLObject import SQLObject

from Artist import Artist


class Query:
    
    slots = [
        "__userID",
        "__dateAddedAfter",
        "__dateAddedBefore",

        "__artistList",

        "__dateMadeAfter",
        "__dateMadeBefore"
        ]
    
    def __init__(self , userID: str , dateAddedAfter = None , dateAddedBefore = None, artistList = [], dateMadeAfter = None, dateMadeBefore = None):

        self.__userID: str = userID
        
        dateAddedAfter: str
        dateAddedBefore: str

        artistList: list[Artist] 
        
        dateMadeAfter: str
        dateMadeBefore: str

        self.setDateAddedAfter(dateAddedAfter)
        self.setDateAddedBefore(dateAddedBefore)
        self.setArtistList(artistList)
        self.setDateMadeAfter(dateMadeAfter)
        self.setDateMadeBefore(dateMadeBefore)


    def standardizeDate(self, date: str | date) -> str:
        if (type(date) == str):
            splitDate = date.split("T")
            if (len(splitDate) == 2):
                date = splitDate[0]

            splitDateWithoutTime = date.split("-")
            if (len(splitDateWithoutTime) == 2):

                date = f"{splitDateWithoutTime[0]}-{splitDateWithoutTime[1]}-01"
                
        return date

    def isDateAddedConstraint(self) -> bool:
        return self.getDateAddedAfter() != None or self.getDateAddedBefore() != None

    def isArtistConstraint(self) -> bool:
        return len(self.getArtistList()) != 0
    
    def isDateMadeConstraint(self) -> bool:
        return self.getDateMadeAfter() != None or self.getDateMadeBefore() != None

    """
    Getters and Setters
    """
    def getUserID(self) -> str:
        return self.__userID

    def getDateAddedAfter(self) -> str:
        return self.__dateAddedAfter
    
    def setDateAddedAfter(self, dateAddedAfter: str | date) -> None:
        self.__dateAddedAfter = self.standardizeDate(dateAddedAfter)

    def getDateAddedBefore(self) -> str:
        return self.__dateAddedBefore
    
    def setDateAddedBefore(self, dateAddedBefore: str | date) -> None:
        self.__dateAddedBefore = self.standardizeDate(dateAddedBefore)



    def getArtistList(self) -> list[Artist]:
        return self.__artistList

    def setArtistList(self , artistList: list[Artist|str]) -> None:
        """
        Caution
        -------
            - This will override any previouse list
        """
        self.__artistList = []
        for artist in artistList:
            if (type(artist) == Artist):
                self.__artistList.append(artist)
                continue

            if (type(artist) == str):
                self.__artistList.append(Artist(artist))
                continue

            Logger().warn(f"Query.setArtistList() had incorrect type of {type(artist)}")
        
    def getDateMadeAfter(self) -> str:
        return self.__dateMadeAfter
    
    def setDateMadeAfter(self, dateMadeAfter: str | date) -> None:
        self.__dateMadeAfter = self.standardizeDate(dateMadeAfter)

    def getDateMadeBefore(self) -> str:
        return self.__dateMadeBefore
    
    def setDateMadeBefore(self, dateMadeBefore: str | date) -> None:
        self.__dateMadeBefore = self.standardizeDate(dateMadeBefore)

    def execute(self) -> list:

        #Check if null query and stop it
        if (not self.isDateAddedConstraint() and not self.isArtistConstraint() and not self.isDateMadeConstraint()):
            Logger().warn("Query.execute() has no constraints")
            return []


        queryTuple = (self.getUserID(),)
        #s.songName, (Only for debugging)(Uncommenting this will make the query only print names)
        query: str = """
        SELECT DISTINCT TOP 750
            s.songID
        FROM 
            songs s
        JOIN 
            artistSongLink asl ON s.songID = asl.songID
        JOIN 
            playlistSongLink psl ON s.songID = psl.songID
        JOIN 
            playlists pl ON psl.playlistID = pl.playlistID
        WHERE 
            pl.userID = ?
            AND pl.isUnwanted = 0"""


        """
            AND asl.artistID in ('5K4W6rqBFWDnAN6FQUkS6x' , '40ZNYROS4zLfyyBSs2PGe2')
            --AND psl.dateAdded > '2025-01-01'
            --AND s.dateMade < '2020-01-01';
        """

        #Check if date added constraint
        if (self.isDateAddedConstraint()):
            if (self.getDateAddedAfter() != None):
                query += "\nAND psl.dateAdded > ?"
                queryTuple += (self.getDateAddedAfter(),)

            if (self.getDateAddedBefore() != None):
                query += "\nAND psl.dateAdded < ?"
                queryTuple += (self.getDateAddedBefore(),)

            pass

        if (self.isArtistConstraint()):
            
            artistIDTuple = ()
            listOfArtistIDs = []
            for artist in self.getArtistList():
                artistIDTuple += (artist.getID(),)
                listOfArtistIDs.append('?')

            query += "\nAND asl.artistID in " + str(listOfArtistIDs).replace("'" , "").replace("[" , "(").replace("]" , ")")
            queryTuple += artistIDTuple

        if (self.isDateMadeConstraint()):
            if (self.getDateMadeAfter() != None):
                query += "\nAND s.dateMade > ?"
                queryTuple += (self.getDateMadeAfter(),)

            if (self.getDateMadeBefore() != None):
                query += "\nAND s.dateMade < ?"
                queryTuple += (self.getDateMadeBefore(),)

        #Add final semi colon
        query += ";"

        sql = SQLObject()
        # print("query:" , query)
        # print("queryTuple" , queryTuple)
        data = sql(query , queryTuple)

        return [row[0] for row in data.fetchall()]
        


if (__name__ == "__main__"):
    #q = Query("px1a3vhak2udchyl4dcug9s4y" , artistList=["5K4W6rqBFWDnAN6FQUkS6x" , "40ZNYROS4zLfyyBSs2PGe2"])
    q = Query("px1a3vhak2udchyl4dcug9s4y" , dateMadeAfter = "2010-01-01", dateMadeBefore = "2020-01-01", artistList=["5K4W6rqBFWDnAN6FQUkS6x"])

    print(q.execute())


        
