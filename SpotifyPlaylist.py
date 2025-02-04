from Playlist import Playlist
from Song import Song
from Artist import Artist
from SpotifyAccessor import SpotifyAccessor



class SpotifyPlaylist(Playlist):
    """
    This is a subclass of Playlist that is used to pull data of a given playlist from
    the Spotify API.
    """

    __slots__ = []

    def __init__(self , playlistShell: Playlist):
        """
        Constructor for SpotifyPlaylist.

        Parameters:
        ----------
        playlistShell : Playlist
            The playlistShell is a Playlist object that is used to get 
            the ID of the playlist that is to be loaded. This playlist 
            should be a shell containing ID, Name, ImgURL, and SnapshotID.
        """
        

        super().__init__(playlistShell.getID(), 
                         playlistShell.getName(), 
                         playlistShell.getImgURL(), 
                         playlistShell.getSnapshotID())


            
    def loadSongs(self , spotifyAccessor: SpotifyAccessor) -> None:
        """
        Loads in songs from playlist with artist that do not have their imagesURL on them.
        (Doing that needs another request)
        """

        data = spotifyAccessor.playlist_tracks(self.getID())

        def getSongData(songData) -> Song:
            addedDate = songData['added_at']
            song = songData['track']
            songID = song['id']
            songName = song['name']
            songDateMade = song['album']['release_date']
            songImgLink = song['album']['images'][0]['url']

            artistData = song['artists']
            artistList = []
            for artist in artistData:
                artistID = artist['id']
                artistName = artist['name']
                #artistImgLink = artist['images'][0]['url']
                artistList.append(Artist(artistID , name=artistName))



            return Song(songID , name = songName , dateMade=songDateMade , imgLink=songImgLink , dateAdded=addedDate , artistList=artistList)

        songSet = spotifyAccessor.iterateThroughPagination(data, getSongData)
        self.setSongSet(songSet)    



if (__name__ == "__main__"):

    # chillSongsID = "3qStVWjWcNzOK0JXroierU"
    
    # sP = SpotifyPlaylist(Playlist(chillSongsID))
    # spotAccessor = SpotifyAccessor(None)
    # sP.loadSongs(spotAccessor)

    sA = SpotifyAccessor(None)
    sA.input_to_json(sA.playlist_tracks("3qStVWjWcNzOK0JXroierU") , "playlist_tracks.json")


    pass


