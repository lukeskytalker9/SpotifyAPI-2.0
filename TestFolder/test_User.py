import pytest

from User import User

class TestUser:
    
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        
        #Need to be replaced with correct access token
        access_token = None

        self.testUser = User(access_token)


    def test_getUserData(self) -> None:
        """
        Test the getUserData method.
        """
        user = self.testUser

        expectedResults = {
            "userID": "px1a3vhak2udchyl4dcug9s4y",
            "username": "Jack Biggins",
            "profilePhotoURL": "https://i.scdn.co/image/ab6775700000ee851e786fad48b376c096933f7d",
            "authority":
                {
                "authorityDescription": "admin",
                "isLoggedIn": True,
                "isAdministrator": True,
                },
        }

        result = user.getUserData()
    
        assert result == expectedResults
