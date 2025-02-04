/*
USE spotifyAPI2;
*/


CREATE TABLE users (

	userID VARCHAR(32) PRIMARY KEY,
	
	/*Could be 'admin' or 'user' or 'guest'*/
	authority VARCHAR(10) DEFAULT 'user', 

	genPlaylistID VARCHAR(25),
	databasePlaylistID VARCHAR(25),
)



CREATE TABLE playlists (
	
	playlistID VARCHAR(25) PRIMARY KEY,
	userID VARCHAR(32) FOREIGN KEY REFERENCES users(userID),
	playlistName VARCHAR(255),
	playlistImgURL VARCHAR(200),
	playlistSnapshotID VARCHAR(32),
	isUnwanted BIT DEFAULT(0),

)


CREATE TABLE songs (

	songID VARCHAR(25) PRIMARY KEY,
	songName VARCHAR(255),
	dateMade Date,
	imgLink VARCHAR(200),
	updated BIT DEFAULT(0),

)


CREATE TABLE playlistSongLink (
	dataID INT IDENTITY(1,1) PRIMARY KEY,

	playlistID VARCHAR(25) FOREIGN KEY REFERENCES playlists(playlistID),
	songID VARCHAR(25) FOREIGN KEY REFERENCES songs(songID),

	dateAdded Date,

)

CREATE TABLE artists (
	artistID VARCHAR(25) PRIMARY KEY,

	artistName VARCHAR(75),
	imgLink VARCHAR(200) DEFAULT(null),

	
)

CREATE TABLE artistSongLink (

	dataID INT IDENTITY(1,1) PRIMARY KEY,

	songID VARCHAR(25) FOREIGN KEY REFERENCES songs(songID),
	artistID VARCHAR(25) FOREIGN KEY REFERENCES artists(artistID),
 
)

CREATE TABLE listeningHistory (

	dataID INT IDENTITY(1,1) PRIMARY KEY,

	sessionID INT,
	numberInSession INT, 
	timeListened DATETIME NOT NULL,

	userID VARCHAR(32) FOREIGN KEY REFERENCES users(userID),
	songID VARCHAR(25),
	isInDatabase BIT DEFAULT(1),
	isFiller BIT DEFAULT(0),

)



/*THIS IS FOR users TABLE */
INSERT users VALUES ('px1a3vhak2udchyl4dcug9s4y' , 'admin' , '2GtskDWgwsdsVC6cFTnEH4' , '6ZSB6xaQx2piHdInhVHOeJ');


/*

/*(columns 1, column 2)*/
INSERT INTO playlists
VALUES 
	/*Insignificant Speck*/
	('7duqrK1ZecXNWbderKzd0n' , 'px1a3vhak2udchyl4dcug9s4y' , 'Little Insignificant Speck' , 'https://image-cdn-ak.spotifycdn.com/image/ab67706c0000da84ad5952f98dcca2158f0c2cb3' , 'AAAALy6A+iZNCW3jF39JGMOTzvqLd4lK' , 1),
	/*Syd and Jack songs that are...*/
	('2moFFFfrTnzHoznOjWeMag' , 'px1a3vhak2udchyl4dcug9s4y' , 'Syd and Jack songs that are sad but sometimes happy' , 'https://mosaic.scdn.co/640/ab67616d00001e02318443aab3531a0558e79a4dab67616d00001e024b292ed7c7360a04d3d6b74aab67616d00001e02bd2de84891eed55a6a82368bab67616d00001e02c985bcc18dd81da80839e5a9' , 'AAABF095ckUN4dZA6jo7qioyX98iH4h9' , 1),
	/* Chill Updated 7:06 5/31/2024 */
	('3qStVWjWcNzOK0JXroierU' , 'px1a3vhak2udchyl4dcug9s4y' , 'Chill' , 'https://mosaic.scdn.co/640/ab67616d00001e024158fe41143182ec16ead070ab67616d00001e027582716b3666a5235d5af4eaab67616d00001e02ca02f2ecba4a803b191c7eabab67616d00001e02e2e352d89826aef6dbd5ff8f',  'AAAAjSk+4MpE5MuMSKkHP0s82dqp1xQ+' , 0),
    /* Feels Updated 7:06 5/31/2024 */
	('3kv8ehqVxfUVnZEkyflwjF' , 'px1a3vhak2udchyl4dcug9s4y' , 'Feels' , 'https://mosaic.scdn.co/640/ab67616d00001e02a9929deb093a6617d2493b03ab67616d00001e02b11bdc91cb9ac6b14f5c1daeab67616d00001e02e1d47c00ddecbfb810c807edab67616d00001e02e6d489d359c546fea254f440' , 'AAAAkAMw89qmxbe4wd4lbyYjdwVHaq/R' , 0);




/* Somewhere only we know*/
INSERT INTO songs
VALUES 
	/*Somewhere only we know*/
	('1SKPmfSYaPsETbRHaiA18G' , 'Somewhere Only We Know' , '2004-05-10' , 'https://i.scdn.co/image/ab67616d0000b2737d6cd95a046a3c0dacbc7d33' , 0),
	/*Hold my girl*/
	('42bbDWZ8WmXTH7PkYAlGLu' , 'Hold My Girl' , '2018-03-23' , 'https://i.scdn.co/image/ab67616d0000b273103045cd1c29dd16a469f808' , 0),

	/*Sit next to me*/
	('4BdGO1CaObRD4La9l5Zanz' , 'Sit Next to Me' , '2017-07-21' , 'https://i.scdn.co/image/ab67616d0000b273ca02f2ecba4a803b191c7eab' , 0),
	/*Circles*/
	('21jGcNKet2qwijlDFuPiPb' , 'Circles' , '2019-09-06' , 'https://i.scdn.co/image/ab67616d0000b2739478c87599550dd73bfa7e02' , 0),
	/*Winter*/
	('4V3VshJLUTCIWa77YiAkvM' , 'Winter' , '2017-04-27' , 'https://i.scdn.co/image/ab67616d0000b273988ede5e1276e758b5f9e577' , 0),
	/*Sugar in a Bowl*/
	('5MKfqLrtXhoq4zZu86BPzA' , 'Sugar in a Bowl' , '2021-10-29' , 'https://i.scdn.co/image/ab67616d0000b273051b87b2ee1ff378a3874c58' , 0);



INSERT INTO playlistSongLink (playlistID , songID , dateAdded)
VALUES
	/*Somewhere only we know in Feels*/
	('3kv8ehqVxfUVnZEkyflwjF' , '1SKPmfSYaPsETbRHaiA18G' , '2021-12-02'),
	/*Hold my girl in Feels*/
	('3kv8ehqVxfUVnZEkyflwjF' , '42bbDWZ8WmXTH7PkYAlGLu' , '2022-12-11'),
	
	/*Sit next to me in Chill*/
	('3qStVWjWcNzOK0JXroierU' , '4BdGO1CaObRD4La9l5Zanz' , '2021-11-27'),
	/*Circles in Chill*/
	('3qStVWjWcNzOK0JXroierU' , '21jGcNKet2qwijlDFuPiPb' , '2021-12-22'),
	/*Winter in Chill*/
	('3qStVWjWcNzOK0JXroierU' , '4V3VshJLUTCIWa77YiAkvM' , '2022-07-21'),
	/*Sugar in a Bowl in Feels*/
	('3kv8ehqVxfUVnZEkyflwjF' , '5MKfqLrtXhoq4zZu86BPzA' , '2024-08-12');


*/

SELECT * FROM users;
SELECT * FROM playlists;
SELECT * FROM songs;
SELECT * FROM playlistSongLink;
SELECT * FROM artists;
SELECT * FROM artistSongLink;
SELECT * FROM listeningHistory;

SELECT * 
FROM listeningHistory
ORDER BY timeListened;

SELECT 
    lh.dataID,
    lh.sessionID,
    lh.numberInSession,
    lh.timeListened,
    lh.userID,
    lh.songID,
    lh.isInDatabase,
    lh.isFiller,
    s.songName,
    s.dateMade,
    s.imgLink,
    s.updated
FROM 
    listeningHistory AS lh
LEFT JOIN 
    songs AS s
ON 
    lh.songID = s.songID
ORDER BY lH.timeListened;

/*
DELETE FROM listeningHistory
WHERE dataID IN (
    SELECT TOP 6 dataID
    FROM listeningHistory
    ORDER BY dataID DESC
);
*/

/*

DROP TABLE listeningHistory;

DROP TABLE artistSongLink;
DROP TABLE artists;

DROP TABLE playlistSongLink;

DROP TABLE songs;
DROP TABLE playlists;
DROP TABLE users;

*/
/*
8/19/2024 Testing joining songs and songsPlaylistLink

SELECT 
    s.songID,
    s.songName,
    s.dateMade,
    psl.dateAdded
FROM 
    songs s
INNER JOIN 
    playlistSongLink psl ON s.songID = psl.songID
WHERE 
    
	ps1.dateAdded > '2025-01-01';

	/*psl.userID = 'px1a3vhak2udchyl4dcug9s4y'AND*/
*/

/*
8/20/2024 Checking if song in songs
SELECT COUNT(1)
FROM songs
WHERE songID = '42bbDWZ8WmXTH7PkYAlGLu';
*/

/*
Chatgpt query

SELECT DISTINCT TOP 500 
    s.songID,
    s.songName
FROM 
    songs s
JOIN 
    artistSongLink asl ON s.songID = asl.songID
JOIN 
    playlistSongLink psl ON s.songID = psl.songID
JOIN 
	playlists pl ON pl.playlistID = ps1.playlistID
WHERE 
	p1.userID = 'px1a3vhak2udchyl4dcug9s4y'
	AND p1.
    AND asl.artistID = '5K4W6rqBFWDnAN6FQUkS6x'
    AND psl.dateAdded > '2024-01-01'
    AND s.dateMade < '2020-01-01'


SELECT DISTINCT TOP 500 songID, songName
FROM (
    SELECT
        s.songID,
        s.songName
    FROM 
        songs s
    JOIN 
        artistSongLink asl ON s.songID = asl.songID
    JOIN 
        playlistSongLink psl ON s.songID = psl.songID
    WHERE 
		asl.artistID = '3OfiFNgFbJAwuQnVvOL2bh'
		AND psl.dateAdded > '2024-01-01'
		AND s.dateMade < '2020-01-01'
	ORDER BY NEWID()
) filtered_data



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

*/