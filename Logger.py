from __future__ import annotations
from typing import TextIO
import datetime
import warnings

class Logger:


    __instance:Logger = None

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
            cls.__instance = super(Logger , cls).__new__(cls)

        return cls.__instance
    


    __slots__ = ["__file"]

    def __init__(self):
        self.__file: TextIO
        self.__file = open("warningsLog.txt" , "a")
    
    def warn(self , message:str) -> None:
        self.__getFile().write(f"[{datetime.datetime.now()}] WARNING: {message}\n")

    def fatal(self , message:str) -> None:
        self.__getFile().write(f"[{datetime.datetime.now()}] FATAL: {message}\n")

    def close(self) -> None:
        self.__getFile().close()
        self.__instance = None

    #* BASIC GETTERS AND SETTERS *#
    def __getFile(self) -> TextIO:
        return self.__file
    

if (__name__ == "__main__"):
    log = Logger()
    
    log.warn("This is a warning") 
    log.fatal("This is a fatal error")
    log.fatal("The world is going to end abandon hope")
    
    # for a in range(100):
    #     for b in range(100):
    #         print(a*b)
    #     log.warn("This is a warning2")