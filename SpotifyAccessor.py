import spotipy  
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler


from datetime import datetime 

import json
from CustomEncoder import CustomEncoder
import math
import base64


from dotenv import load_dotenv
import os

load_dotenv()


class SpotifyAccessor(spotipy.Spotify):
    

    def __init__(self, access_token):
        # Create a CacheFileHandler instance
        handler = CacheFileHandler(cache_path = "__pycache__/spotifyCache.json", 
                                   username = os.getenv("SPOTIFY_USERNAME"))

        # Pass the CacheFileHandler instance to SpotifyOAuth
        auth_manager = SpotifyOAuth(client_id = os.getenv("SPOTIFY_CLIENT_ID"),
                                   client_secret = os.getenv("SPOTIFY_CLIENT_SECRET"),
                                   redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI"),
                                   scope = 'user-library-read user-read-playback-state user-modify-playback-state user-read-recently-played playlist-modify-public playlist-modify-private',
                                   cache_handler = handler)
        
        super().__init__(auth_manager=auth_manager)

    def getUserDataFromSpot(self) -> dict:

        userRequest = self.current_user()
        # print(userRequest)
        returnDict = {
            "userID": userRequest['id'],
            "username": userRequest['display_name'],
            "profilePhotoURL": userRequest['images'][-1]['url']
        }

        return returnDict
    


    def updateDatabaseDescription(self) -> None:

        dateAndTime = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        newDescription = 'Updated: ' + dateAndTime
        
        self.playlist_change_details("6ZSB6xaQx2piHdInhVHOeJ" , description = newDescription)
        
    
    
    def input_to_json(self, dic: dict , jsonName: str ):
        """
        This is used to print complex json requests usually from spotify. This will place them
        in the JsonStorage by default.
        """

        #Check if name ends with .json
        splitName = jsonName.split(".")
        if (len(splitName) == 1 or splitName[-1] != "json"):
            jsonName += ".json"

        jsonName = "JsonStorage/" + jsonName
        json_file = open(jsonName, '+w')
        json_object = json.dumps(dic , indent = 4 , cls = CustomEncoder)
        json_file.write(json_object)
        json_file.close()
        return
    

    def iterateThroughPagination(self , dic: dict , func) -> set:

        totalItems = dic['total']
        limit = dic['limit']

        returnSet = set()
        #self.input_to_json(dic , "iterateThroughPagination.json")

        iterationNumber = math.ceil(totalItems/limit)

        for i in range(iterationNumber):

            for item in dic['items']:
                returnSet.add(func(item))

            if (i != iterationNumber - 1): 
                # print("here")
                dic = self.next(dic)
                #self.input_to_json(dic , "iterateThroughPagination.json")


        return returnSet



    def createNewGenplaylist(self , userID: str) -> str:
        """
        Returns
        -------
        str
            The playlistID of the newly created playlist.
        """
        name = "Generated Playlist"
        # descriptin = "A playlist that holds generated playlists"
        imgDir = "Assets\OnButtonReduced.jpg"
        self.__createNewPlaylist(userID , name , imgDir)


    def createNewDatabasePlaylist(self, userID:str) -> str:
        """
        Returns
        -------
        str
            The playlistID of the newly created playlist.
        """

        name = "Database Playlist"
        # descriptin = "A playlist that contains all the songs in the database."
        imgDir = "Assets\MountainSunriseReduced.jpg"
        self.__createNewPlaylist(userID , name , imgDir)

    def __createNewPlaylist(self , userID:str , name:str , imgDir:str , description:str = '') -> str:
        """
        Returns
        -------
        str
            The playlistID of the newly created playlist.
        """
        playlist = self.user_playlist_create(user = userID , name=name, description=description)
        
        playlist_id = playlist['id']
        print("Playlist ID: ", playlist_id)

        image_data = None
        # Upload a cover image for the playlist
        with open(imgDir, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            print("length of image data: ", len(image_data))
        
        # self.playlist_upload_cover_image(playlist_id, image_data)
        
        
        
        return playlist_id

    def removeAllSongsFromPlaylist(self , playlistID: str) -> None:
        """
        Removes all songs from a playlist.
        """
        while True:
            dic = self.playlist_tracks(playlistID)
            
            # Extract track IDs from the current batch of tracks
            songIDList = [item['track']['id'] for item in dic['items']]
            
            if songIDList:
                # Remove the tracks in the current batch
                self.playlist_remove_all_occurrences_of_items(playlistID, songIDList)
            else:
                break
        

    def addSongsToGenPlaylist(self , genPlaylistID: str , songIDList: list[str]) -> None:
        
        self.removeAllSongsFromPlaylist(genPlaylistID)

        for i in range(0, len(songIDList), 100):
            self.playlist_add_items(genPlaylistID, songIDList[i:i+100])

    def getArtistID(self , artistName: str) -> str:
        """
        Returns
        -------
        str
            The artistID of the artist with the given name.
        """
        artist = self.search(q=artistName, type='artist')['artists']['items'][0]
        return artist['id']

    
    

#Write Test Functions In Here
if (__name__ == '__main__'):

    sp = SpotifyAccessor("")
    #print(sp.current_user())
    #sp.input_to_json(sp.current_user() , "current_user.json")

    sp.input_to_json(sp.current_user_playlists() , "current_user_playlists.json")
    sp.input_to_json(sp.playlist("3qStVWjWcNzOK0JXroierU") , "playlist(Chill).json")
    
    # sp.input_to_json(sp.current_user_playing_track() , "current_user_playing_track.json")
    sp.input_to_json(sp.current_user_recently_played() , "current_user_recently_played.json")
    
    sp.input_to_json(sp.artist("718COspgdWOnwOFpJHRZHS") , "artist('lukeCombs').json") #Luke Combs
    
    sp.input_to_json(sp.track("0Zm4ZDBtiZCDp69Cxs5TaB") , "track('TheManHeSeesInME').json") #The man he sees in me by Luke Combs   
    # sp.input_to_json(sp.audio_analysis(["0Zm4ZDBtiZCDp69Cxs5TaB"]) , "audio_analysis('n95').json") #The man he sees in me by Luke Combs
    # sp.input_to_json(sp.audio_features("0Zm4ZDBtiZCDp69Cxs5TaB") , "audio_features('n95').json") #The man he sees in me by Luke Combs

    sp.input_to_json(sp.current_playback() , "current_playback.json")
    # sp.input_to_json(sp.current_user_recently_played(after = "2025-01-14T01:29:23.454Z") , "current_user_recently_played(after=2025-01-14T01:29:23.454Z).json")


    print(len(sp.current_user_recently_played(limit = 50)["items"]))
    

    L2L9 = "32sgrn4S4vU6kQtHLXYsNx"
    Chill = '3qStVWjWcNzOK0JXroierU'
    Feels = '3kv8ehqVxfUVnZEkyflwjF'
    #sp.input_to_json(sp.playlist(Feels) , "playlistFeels.json")

    #SnapshotID = "AAAARRelEIFzZYVgyJooEoIuxGL2ieCN" 131 songs
    #             "AAAARqcerjWf6SKbQV9obkO+ILQvPhKr" 132 songs
    
