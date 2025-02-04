# SpotifyAPI-2.0
This is a generalized API version of my Spotify application



# For Observer
This code is currently contains a couple of tracer bullets of the main functionality contained in the files: fullyFunctioningListeningHistory.py and fullyFunctioningQuery.py instead of AppMain.py.
- **fullyFunctioningQuery.py:** This file searches through the database for songs mathing the inputted criteria and adds it to my spotify as a playlist. This will be the main functionality of the final product
- **fullyFunctioningListeningHistory.py:** This file updates the database to match spotify and then adds my listening history to a table to be used in the future and a dataset to test out song prediction ML models for personal use.


Additionally, I deleted the listening history as it contained private keys. These are now stored in environmental variables so I could make the code public. Older website of this was written with poor practices (I was a beginner) so they will not be made public. 



# Personal Notes For My Own Development
## Things to note
These are important landmarks, concerns, and where to continue tips for efficient program development.
- Make sure the flow of the spotify accessor is dependant on beginning
    - Currently the authorization token in SpotifyAccessor when passed in does nothing so later in development we need to make sure that this gets fizxed so thjat argument is used.
    - Cannot assign images to playlists when created (genPlaytlist , databasePlaylist)



## Moving forwards (Temp):
Here are things i want this pro 
- Collect song data (and order played) to make ai to predeict next best song. Data that should be collected for ai:
    Artist / Genre: Embeded with the following data (Difficult)
        -Genre maybe
    Length: discoraging long songs
    Danceability
    Energy
    Key
    Tempo
    Valence
    Instrumentalness

- Be able to query based on (NEW, Artist, Date Made(before and after), Maybe also Playlist to have new songs from playlist)
    - If get chatpgt to rate emotions then maybe sort on that
    


