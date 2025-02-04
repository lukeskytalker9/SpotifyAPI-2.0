from Logger import Logger

class Artist:

    
    __slots__ = ["__id" , "__name" , "__imgURL"]

    __logger = Logger()

    def __init__(self , id:str , name:str = None , imgURL:str = None):
        
        self.__id: str
        self.__name: str 
        self.__imgURL: str 
        
        self.setID(id)
        self.setName(name)
        self.setImgURL(imgURL)


    #* BASIC GETTERS AND SETTERS *#
    def getID(self) -> str:
        return self.__id
    
    def setID(self , id:str) -> None:
        
        if (len(id) > 25):
            self.__getLogger().fatal(f"ID ({id}) is longer than 25 characters. Truncating.")
            
        self.__id = id

    def getName(self) -> str:
        return self.__name
    
    def setName(self , name:str|None) -> None:
        if (type(name) == str and len(name) > 75):
            name = name[:75]
            self.__getLogger().warn(f"Name ({name}) is longer than 75 characters. Truncating.")
        self.__name = name

    def getImgURL(self) -> str:
        return self.__imgURL
    
    def setImgURL(self , imgURL:str | None) -> None:

        if (type(imgURL) == str and len(imgURL) > 200):
            imgURL = imgURL[:200]
            self.__getLogger().warn(f"ImgURL ({imgURL}) is longer than 255 characters. Truncating.")
        self.__imgURL = imgURL
    
    def __getLogger(self) -> Logger:
        return self.__logger



if (__name__ == "__main__"):
    pass

