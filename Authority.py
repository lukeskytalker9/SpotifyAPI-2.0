from enum import Enum

"""
This is a way of storing more complex data into the enum
"""
class AuthorityData():
    __slots__ = [
        "__description",
        "__isLoggedIn",
        "__isAdministrator",
    ]

    def __init__(self , description:str , isLoggedIn:bool , isAdministrator:bool):
        self.__description: str = description
        self.__isLoggedIn: str = isLoggedIn
        self.__isAdministrator: str = isAdministrator

    def getDescription(self) -> str:
        return self.__description
    
    def isLoggedIn(self) -> bool:
        return self.__isLoggedIn
    
    def isAdministrator(self) -> bool:
        return self.__isAdministrator
    


class Authority(Enum):
    GUEST = AuthorityData("guest" , False , False)
    USER = AuthorityData("user" , True , False)
    ADMIN = AuthorityData("admin" , True , True)

    def __repr__(self) -> dict:
        return self.getPackage().__str__()
    
    def __str__(self) -> str:
        return str(self.getDescription())
    
    def getPackage(self) -> dict:
        package = {
            "authorityDescription": self.getDescription(),
            "isLoggedIn": self.isLoggedIn(),
            "isAdministrator": self.isAdministrator(),
        }
        return package

    def getDescription(self) -> str:
        return self.value.getDescription()
    
    def isLoggedIn(self) -> bool:
        return self.value.isLoggedIn()
    
    def isAdministrator(self) -> bool:
        return self.value.isAdministrator()


if (__name__ == "__main__"):
    print("Now Beginning Tests For Authority.py")

    print(Authority.USER)

    for authority in Authority:
        print("/////////////////////")
        print("getPackage" , authority.getPackage())
        print("getDescription" , authority.getDescription())
        print("isLoggedIn" , authority.isLoggedIn())   
        print("isAdministrator" , authority.isAdministrator())

        print("Dict test" , authority.getPackage()["authorityDescription"])

    print("Tests Completed For Authority.py")
