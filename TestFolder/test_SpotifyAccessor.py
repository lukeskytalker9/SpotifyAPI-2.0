import pytest

from SpotifyAccessor import SpotifyAccessor
from Song import Song


class TestSpotifyAccessor:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:

        access_token = None

        self.testObject = SpotifyAccessor(access_token)


    def test_getUserDataFromSpot(self) -> None:
        """
        This test assumes user is a single example user (currently set to Jack Biggins user not Test).
        """

        testObject = self.testObject

        userData = testObject.getUserDataFromSpot()

        assert type(userData) == dict
        
        assert len(userData) == 3

        assert type(userData['userID']) == str
        assert type(userData['username']) == str
        assert type(userData['profilePhotoURL']) == str 

        assert userData['userID'] == "px1a3vhak2udchyl4dcug9s4y"
        assert userData['username'] == "Jack Biggins"  
        assert userData['profilePhotoURL'] == "https://i.scdn.co/image/ab6775700000ee851e786fad48b376c096933f7d"

    def test_iterateThroughPagination(self) -> None:
        """
        This test shows iterateThorughPagination working withsimple example
        """

        testObject = self.testObject

        def testFunction(x):
            return str(x['id'])

        returnValues = testObject.iterateThroughPagination(testObject.current_user_playlists() , testFunction)

        assert type(returnValues) == set

        #Assert that the return values are all strings
        for value in returnValues:
            assert type(value) == str
        
        #Assert Feels Playlist is in the return values
        assert "3kv8ehqVxfUVnZEkyflwjF" in returnValues
        #Assert Chill Playlist is in the return values
        assert "3qStVWjWcNzOK0JXroierU" in returnValues
        #Assert Little Speck is in the return values
        assert "7duqrK1ZecXNWbderKzd0n" in returnValues

    def test_iterateThroughPaginationSongPlaylist(self) -> None:
        """
        This example of iterateThroughPagination shows a differnt example
        of iterating through songs in a playlist
        """

        testObject = self.testObject

        feelsPlaylistID = "3kv8ehqVxfUVnZEkyflwjF"
        data = testObject.playlist_tracks(feelsPlaylistID)



        def getSongData(songData) -> Song:
            addedDate = songData['added_at']
            song = songData['track']
            songID = song['id']
            songName = song['name']
            songDateMade = song['album']['release_date']
            songImgLink = song['album']['images'][0]['url']
            return Song(songID , name = songName , dateMade=songDateMade , imgLink=songImgLink , dateAdded=addedDate)
        
        songSet = testObject.iterateThroughPagination(data, getSongData)

        assert type(songSet) == set
        
        for song in songSet:
            assert type(song) == Song

        #Assert Somewhere only we know is in feels
        assert Song("1SKPmfSYaPsETbRHaiA18G") in songSet
        #Assert Hold my girl is in feels
        assert Song("42bbDWZ8WmXTH7PkYAlGLu") in songSet
        #Assert Second page song ("Sugar in a bowl") is in feels
        assert Song("5MKfqLrtXhoq4zZu86BPzA") in songSet