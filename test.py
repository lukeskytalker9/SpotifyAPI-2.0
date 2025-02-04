from SpotifyAccessor import SpotifyAccessor

sA = SpotifyAccessor(None)

# sA.input_to_json(sA.current_user_top_artists(limit=10 , time_range="long_term") , "current_user_top_artists.json")
# sA.input_to_json(sA.current_user_top_tracks(limit=10 , time_range="long_term") , "current_user_top_tracks.json")

kanyeID = "5K4W6rqBFWDnAN6FQUkS6x"
zachID = "40ZNYROS4zLfyyBSs2PGe2"


# sA.input_to_json(sA.artists(kanyeID) , "kanye.json")

print(type(None))

x = """
SELECT DISTINCT TOP 750
    s.songID,
    s.songName
FROM 
    songs s
JOIN 
    artistSongLink asl ON s.songID = asl.songID
JOIN 
    playlistSongLink psl ON s.songID = psl.songID
JOIN 
    playlists pl ON psl.playlistID = pl.playlistID
WHERE 
    pl.userID = 'px1a3vhak2udchyl4dcug9s4y'
	AND pl.isUnwanted = 0
    AND asl.artistID in ('5K4W6rqBFWDnAN6FQUkS6x' , '40ZNYROS4zLfyyBSs2PGe2')
    --AND psl.dateAdded > '2025-01-01'
    --AND s.dateMade < '2020-01-01';
"""

print(x)
