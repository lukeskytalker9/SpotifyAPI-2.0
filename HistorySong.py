from Song import Song

class HistorySong(Song):

    __slots__ = [
        "__timeListened",
        "__isFiller",
        "__isShort"

    ]


    def __init__(self , id:str , timeListened:str , isFiller:bool = False , isShort:bool = False):
        """
        Constructor for the HistorySong class.
        
        Parameters
        ----------
        - id : str
            The id of the song. If none is passed then it is treated as a skipping song
        - timeListened : str
            The time the song was listened to. If this is filler then this will be time of the first song 
            in listening session (becasue stack)
        - isFiller : bool
            True if the song is a filler song, False otherwise.
        - isShort : bool
            True if the song is a short song, False otherwise.

        """
        super().__init__(id)
        self.__timeListened: str = timeListened
        self.__isFiller: bool = isFiller
        self.__isShort: bool = isShort



    def isFiller(self) -> bool:
        """
        Returns
        -------
        bool
            True if the song is a filler song, False otherwise.
        """
        return self.getID() == None
    
    def __repr__(self) -> str:
        if (self.isFiller()):
            return f"HistorySong: !FILLER! Time: {self.getTimeListened()}"
        
        if (self.isShort()):
            return f"HistorySong: !SHORT! Time: {self.getTimeListened()}"
        
        return f"HistorySong: {self.getID()} , Time: {self.getTimeListened()}"
    
    """
    BASIC GETTERS AND SETTERS
    """
    def getTimeListened(self) -> str:
        return self.__timeListened
    
    def isFiller(self) -> bool:
        return self.__isFiller
    
    def isShort(self) -> bool:
        return self.__isShort
    
        
if (__name__ == "__main__"):
    h = HistorySong(None , "2024-12-01")