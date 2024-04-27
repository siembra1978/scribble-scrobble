# Written by siembra1978
import numpy as np
import pandas as pd
import searchmusic
import searchtunes
import os
import time
import datetime

importedCSV = "Apple Music Play Activity.csv"
keepColumns =['Artists', 'Song Name', 'Album Name','Play Duration Milliseconds', 'Album Artist']
scriptFile = os.path.dirname(os.path.abspath(__file__))
maxFMRows = 3000
rateLimit = 4

def filterCSV(inputCSV):
    df = pd.read_csv(inputCSV, nrows=maxFMRows)
    df = df[df['Media Duration In Milliseconds'] > 0]
    df = df[df['Event Type'] == 'PLAY_END']
    df = df[df['End Reason Type'] != 'NOT_APPLICABLE']
    df = df[df['Play Duration Milliseconds'] > df['Media Duration In Milliseconds']/2]

    newAlbums = []
    artistsValues = []

    for index, row in df.iterrows():
        artistValue = str(searchtunes.findArtist(row['Song Name'],row['Album Name']))
        artistsValues.append(artistValue)
        #print(artistValue)

        albumCorrection = str(row['Album Name'])
        newAlbums.append(albumCorrection)

        print(str(((index + 1) / maxFMRows) * 100) + '%')
        #print("About " + str(((maxFMRows-index)*rateLimit)/60) + " minutes left!")
        time.sleep(rateLimit)

    df['Artists'] = artistsValues
    df['Album Name'] = newAlbums
    df['Album Artist'] = ''
    #df['Play Duration Milliseconds'] = newTimes
    df = df[keepColumns]

    spliceAndFinalize(df)
def saveCSV(i, df):
    filename = f'outputs\data_chunk_{i + 1}.csv'
    saveToFile = os.path.join(scriptFile, filename)
    df.to_csv(saveToFile, header=False, index=False)

def spliceAndFinalize(df):
    df = df[df['Artists'] != 'Artist not found']
    df = df[df['Artists'] != 'No results found']

    chunks = [df[i:i + 3000] for i in range(0, df.shape[0], 3000)]

    for index, chunk in enumerate(chunks):
        saveCSV(index, chunk)

filterCSV(importedCSV)
