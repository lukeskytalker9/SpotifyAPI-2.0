import pytest
from datetime import date

from SQLObject import SQLObject
from Authority import Authority
from Song import Song


class TestSQLObject:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:

        self.testObject = SQLObject()


    def test_TestSingleton(self) -> None:
        sql2 = SQLObject()
        assert self.testObject is sql2


    def test_getUserDataFromSQL(self) -> None:

        sql = self.testObject

        userID = "px1a3vhak2udchyl4dcug9s4y"

        expectedResults = {
           "authority": Authority.ADMIN, 
           "genPlaylist": "2GtskDWgwsdsVC6cFTnEH4",
           "databasePlaylist": "6ZSB6xaQx2piHdInhVHOeJ",
        }

        result = sql.getUserDataFromSQL(userID)

        assert result == expectedResults

    def test_getUnwantedPlaylistIDs(self) -> None:

        sql = self.testObject

        userID = "px1a3vhak2udchyl4dcug9s4y"

        expectedResults = ["2moFFFfrTnzHoznOjWeMag" , "7duqrK1ZecXNWbderKzd0n"]

        result = sql.getUnwantedPlaylistIDs(userID)

        assert result == expectedResults

    def test_getPlaylistDataFromSQL(self) -> None:
        """
        Basic Examample that pulls from Feels.
        """
        sql = self.testObject

        playlistID = "3kv8ehqVxfUVnZEkyflwjF"

        expectedResults = {
            "playlistID": "3kv8ehqVxfUVnZEkyflwjF",
            "playlistName": "Feels",
            "playlistImage": "https://mosaic.scdn.co/640/ab67616d00001e02a9929deb093a6617d2493b03ab67616d00001e02b11bdc91cb9ac6b14f5c1daeab67616d00001e02e1d47c00ddecbfb810c807edab67616d00001e02e6d489d359c546fea254f440",
            "snapshotID": "AAAAkAMw89qmxbe4wd4lbyYjdwVHaq/R",
        }

        result = sql.getPlaylistDataFromSQL(playlistID)

        assert result == expectedResults

    def test_getPlaylistDataFromSQLUnwantedPlaylist(self) -> None:
        """
        This case of testign getPlaylistDataFromSQL is for an unwanted playlist which
        should still work.
        """
        sql = self.testObject

        #Syd / Jack Playlist
        playlistID = "2moFFFfrTnzHoznOjWeMag"

        expectedResults = {
            "playlistID": "2moFFFfrTnzHoznOjWeMag",
            "playlistName": "Syd and Jack songs that are sad but sometimes happy",
            "playlistImage": "https://mosaic.scdn.co/640/ab67616d00001e02318443aab3531a0558e79a4dab67616d00001e024b292ed7c7360a04d3d6b74aab67616d00001e02bd2de84891eed55a6a82368bab67616d00001e02c985bcc18dd81da80839e5a9",
            "snapshotID": "AAABF095ckUN4dZA6jo7qioyX98iH4h9",
        }

        result = sql.getPlaylistDataFromSQL(playlistID)

        assert result == expectedResults

    def test_getSongSetFromSQL(self) -> None:
        """
        This basic test case uses the Chill Playlist
        """
        sql = self.testObject

        playlistID = "3qStVWjWcNzOK0JXroierU"

        expectedResults = {
            Song("4BdGO1CaObRD4La9l5Zanz"),
            Song("21jGcNKet2qwijlDFuPiPb"),
            Song("4V3VshJLUTCIWa77YiAkvM")
        }

        results = sql.getSongSetFromSQL(playlistID)

        assert isinstance(results , set)

        for result in results:
            assert isinstance(result , Song)

        assert len(results) == len(expectedResults)
        
        assert results == expectedResults



    def test_getSongSetFromSQL2(self) -> None:
        """
        This test case uses the Feels Playlist
        """
        
        sql = self.testObject

        playlistID = "3kv8ehqVxfUVnZEkyflwjF"

        expectedResults = {
            Song("1SKPmfSYaPsETbRHaiA18G"),
            Song("42bbDWZ8WmXTH7PkYAlGLu"),
            Song("5MKfqLrtXhoq4zZu86BPzA")
        }

        results = sql.getSongSetFromSQL(playlistID)

        for result in results:
            assert isinstance(result.getName() , str)
            assert isinstance(result.getDateMade() , date)
            assert isinstance(result.getImgLink() , str)    
            assert isinstance(result.getDateAdded() , date)  

        assert results == expectedResults
    
    def test_getSongSetFromSQLNothing(self) -> None:
        """
        This test case uses a playlist that does not exist.
        """
        
        sql = self.testObject

        playlistID = "11111111111111"

        expectedResults = set()

        results = sql.getSongSetFromSQL(playlistID)

        assert results == expectedResults



        