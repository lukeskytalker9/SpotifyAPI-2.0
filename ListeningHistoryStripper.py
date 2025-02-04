from datetime import datetime

from SpotifyAccessor import SpotifyAccessor

from HistorySong import HistorySong

class ListeningHistoryStripper(SpotifyAccessor):
    """
    ListeningHistoryStripper is used to strip listening history data to then enter into the 
    listeningHistroy table to be used laster.
    This class is a stack in order for it to be endered into database in correct order.
    """
    __slots__ = [
        '__userID',
        '__songStack'
    ]  

    def __init__(self , access_token , userID: str):
        super().__init__(access_token)

        self.__userID: str = userID
        self.__songStack: list[HistorySong] = []


    def getRecentTracksOLD(self , limit: int = 300, stopAtTimestamp: datetime|None = None) -> None:
        """
        Retrieve the last `limit` tracks or stop when a track with the specified timestamp is found.

        :param limit: The maximum number of tracks to fetch.
        :param stopAtTimestamp: ISO 8601 timestamp to stop fetching tracks when encountered (string).
        :return: List of tracks retrieved.
        """
        next_url = None
        fetched = 0
        isFound = False
        while fetched < limit:
            # print("limit-fetched" , limit - fetched)

            formattedStopAtTimestamp = int(stopAtTimestamp.timestamp() * 1000) if stopAtTimestamp != None else None

            response = self.current_user_recently_played(limit=min(50, limit - fetched), before=None if next_url else formattedStopAtTimestamp)
            items = response.get("items", [])
            
            if not items:
                break
            
            # The Timestamp was found then break
            if (isFound := self.__addListSongDicsToStack(items , stopAtTimestamp)):
                break

            # Update the total fetched and next URL
            fetched += len(items)
            next_url = response.get("next")
            if not next_url:
                break
                
        # If the timestamp was not found then add the last song to the stack
        if (not isFound and self.length() > 0):
            self.add(HistorySong(None , self.peek().getTimeListened() , isFiller=True))

    def getRecentTracks(self , limit: int = 300, stopAtTimestamp: datetime|None = None) -> None:

        next_before = None
        fetched = 0
        isFound = False

        while fetched < limit:
            # Determine the timestamp to use for the 'before' parameter

            # Fetch recently played tracks
            response = self.current_user_recently_played(limit=min(50, limit - fetched), before=next_before)
            items = response.get("items", [])

            if not items:
                print("No items found durring request. Requested before:" + str(next_before))
                break

            # Process the items and check if the stopAtTimestamp is found
            if (isFound := self.__addListSongDicsToStack(items, stopAtTimestamp)):
                break

            # Update the total fetched count
            fetched += len(items)

            # Update the 'before' timestamp to the 'played_at' of the oldest item in this batch
            next_before = response['cursors']['before']
        
        # If the timestamp was not found then add the last song to the stack
        if (not isFound and self.length() > 0):
            self.add(HistorySong(None , self.peek().getTimeListened() , isFiller=True))


    def __addListSongDicsToStack(self , songList: list[dict] , stopAtTimestamp: datetime|None = None, ) -> bool:
        """
        This function will add the songs in the list of dictionaries to the stack of songs

        Parameters
        ----------
        - songList : list[dict]
            The list of songs in dictionary format
        - stopAtTimestamp : str
            The timestamp to stop at

        Returns
        -------
        bool
            True if the timestamp was found, False otherwise
        """


        for item in songList:
            track = item["track"]
            played_at: str = item["played_at"]  # Timestamp when the track was played
            
            #If played_at deos not contain millis seconds then use no millis seconds formatting
            if (len(played_at.split(".")) == 1):                
                playedAtDateTime = datetime.strptime(played_at , "%Y-%m-%dT%H:%M:%SZ")
            else:
                playedAtDateTime = datetime.strptime(played_at, "%Y-%m-%dT%H:%M:%S.%fZ")


            # print("playedAtDateTime" , playedAtDateTime)
            # print("stopAtTimestamp" , stopAtTimestamp)
            # print("playedAtDateTime <= stopAtTimestamp" , playedAtDateTime <= stopAtTimestamp)
            if stopAtTimestamp != None and playedAtDateTime.replace(microsecond=0) <= stopAtTimestamp.replace(microsecond=0):
                # print("Found the timestamp")
                return True
            # print("Not Found the timestamp")
            
            """
            !LOGIC!
            - If the current song is played within 45 seconds of the previous song then we will skip it and add the next
            - If the current song is played after 15 minutes of the previous song then we will add it to the stack after adding a ending peice
            - If its the first song then we will add it to the stack
            - Otherwise we will add it to the stack
            """

            if (self.length() == 0):
                self.add(HistorySong(track["id"] , played_at))

            elif (self.peek().isShort()):
                
                shortTrack = self.pop()

                if (self.isSecondDifferenceShort(played_at , shortTrack.getTimeListened())):
                    self.add(HistorySong(track["id"] , played_at , isShort=True))
                elif (self.isSecondDifferenceLong(played_at , shortTrack.getTimeListened())):
                    self.add(HistorySong(None , played_at , isFiller=True))
                    self.add(HistorySong(track["id"] , played_at))
                else:
                    self.add(HistorySong(track["id"] , played_at))

            else:
                #At this pount previouse song is normal
                if (self.isSecondDifferenceShort(played_at , self.peek().getTimeListened())):
                    self.add(HistorySong(track["id"] , played_at , isShort=True))
                elif (self.isSecondDifferenceLong(played_at , self.peek().getTimeListened())):
                    self.add(HistorySong(None , played_at , isFiller=True))
                    self.add(HistorySong(track["id"] , played_at))
                else:
                    self.add(HistorySong(track["id"] , played_at))


            # Stop if we've hit the desired timestamp

        return False




    def getSecondsDifference(self , time1:str , time2:str) -> int:
        """
        This function will return the difference in seconds between two timestamps
        """
        #If it doesnt have milliseconds
        if (len(time1.split(".")) == 1):
            dt1 = datetime.strptime(time1, "%Y-%m-%dT%H:%M:%SZ")
        else:
            dt1 = datetime.strptime(time1, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        if (len(time2.split(".")) == 1):
            dt2 = datetime.strptime(time2, "%Y-%m-%dT%H:%M:%SZ")
        else:
            dt2 = datetime.strptime(time2, "%Y-%m-%dT%H:%M:%S.%fZ")


        time_difference = dt1 - dt2

        return abs(time_difference.total_seconds())

    def isSecondDifferenceShort(self , time1:str , time2:str) -> bool:
        """
        This function will return True if the difference between the two timestamps is less than 15 minutes
        """
        return self.getSecondsDifference(time1 , time2) < (45)
    
    def isSecondDifferenceLong(self , time1:str , time2:str) -> bool:
        """
        This function will return True if the difference between the two timestamps is more than 15 minutes
        """
        return self.getSecondsDifference(time1 , time2) > (60 * 15)

    def add(self , song:HistorySong) -> None:
        """
        This function will add a song to the stack
        """
        self.__getSongStack().append(song)

    def pop(self) -> HistorySong:
        """
        This function will pop the last song from the stack
        """
        return self.__getSongStack().pop()
    
    def peek(self) -> HistorySong:
        """
        This function will return the last song from the stack
        """
        return self.__getSongStack()[-1]
    
    def length(self) -> int:
        """
        This function will return the length of the stack
        """
        return len(self.__getSongStack())
    
    def __repr__(self) -> str:
        return f"ListeningHistoryStripper: {self.__getSongStack()}"

    def __len__(self) -> int:
        return self.length()

    """
    Getters and Setters
    """
    def getUserID(self) -> str:
        return self.__userID
    
    def __getSongStack(self) -> list[HistorySong]:
        return self.__songStack


if (__name__ == "__main__"):
    #Test code here

    lHS = ListeningHistoryStripper(None , "USERID")
    # lHS.getRecentTracks(stop_at_timestamp="2025-01-20T00:56:37")
    lHS.getRecentTracks()
    print(lHS)
    print(lHS.length())

