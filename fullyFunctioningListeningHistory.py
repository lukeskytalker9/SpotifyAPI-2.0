from datetime import datetime

from ListeningHistoryStripper import ListeningHistoryStripper
from SQLObject import SQLObject
from User import User
"""
This file is just temporary to add songs to listeninginHistory

!ISSUES!
- The time is not staying at todays date and not changing and also probably not including everything
- undable to parse last listened so programm crashes
"""
if (__name__ == "__main__"):


    user = User(None)

    ## L2L#1 , L2L#2 , L2L#3 , L2L#4 , L2L#5 , L2L#6 , L2L#7 , L2L#8 , L2L#9 , L2L#10 , L2L#11, L2L#12
    generalUnwantedPLaylists = ["4TjzxhnkEVeuHluwRxcTjK", 
                                "2lr5WAKVUih78U3uAwVANK", 
                                "6m5NFn4obowHqouRcwuvWz",
                                "4n32bH9cjghdYqupNPFgi4", 
                                "71VWfO07IkVh5RenBgPxTB", 
                                "4Fih0nG0y1bDpHxhdi2YhE", 
                                "6gKIdDIswcHqeQeq5oqf59",
                                "70ygsIiRD0ArRuyMi5Di7q", 
                                "32sgrn4S4vU6kQtHLXYsNx", 
                                "7Drs4yW3iJNMLbk0TZu8n4", 
                                "7HI1SXk32pncvIoiC14M5t",
                                "3WYaAD1KZ7N5vZY1hsR06N"]
    
    #Syd and Jack songs that are sad but sometimes happy
    generalUnwantedPLaylists.append("2moFFFfrTnzHoznOjWeMag")
    #Songs that strangely remind me of you… huh
    generalUnwantedPLaylists.append("4wGOSeNyEyTvJY3C5v97h9")
    #Little Insignificant Speck
    generalUnwantedPLaylists.append("7duqrK1ZecXNWbderKzd0n")
    
    
    user.updateData(generalUnwantedPLaylists)
    

    sql = SQLObject()
    lastHistoryTime: datetime|None =  sql.getLastHistoryTime(user.getUserID())
    print("lastHistoryTime" , lastHistoryTime , type(lastHistoryTime))


    lH = ListeningHistoryStripper(None , user.getUserID())
    lH.getRecentTracks(limit = 500 , stopAtTimestamp=lastHistoryTime)
    print(len(lH))

    sql.addListeningHistoryToSQL(lH)
