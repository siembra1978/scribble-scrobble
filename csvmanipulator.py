# Written by siembra1978
import numpy as np
import pandas as pd
import searchmusic

importedCSV = "Apple Music Play Activity.csv"
keepColumns =['Play Duration Milliseconds', 'Album Name', 'Song Name', 'Event Type', 'End Reason Type', 'Event Received Timestamp']

def filterCSV(inputCSV):
    df = pd.read_csv(inputCSV)
    df = df[df['Media Duration In Milliseconds'] > 0]
    df = df[df['Event Type'] == 'PLAY_END']
    df = df[df['End Reason Type'] != 'NOT_APPLICABLE']
    df = df[df['Play Duration Milliseconds'] > df['Media Duration In Milliseconds']/2]
    df = df[keepColumns]

    artistsValues = []

    for index, row in df.iterrows():
        artistValue = searchmusic.findArtist(row['Song Name'],row['Album Name'])
        artistsValues.append(artistValue)
        print(artistValue)

    df['Artists'] = artistsValues

    return(df)

finalDF = filterCSV(importedCSV)
#print(finalDF.to_string())
finalDF.to_csv('Testing Result.csv', index=False)