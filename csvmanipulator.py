# Written by siembra1978
import numpy as np
import pandas as pd
import searchmusic
import searchtunes
import os
import time
from progress.bar import Bar
import datetime

importedCSV = "Apple Music Play Activity.csv"
keepColumns =['Artists', 'Song Name', 'Album Name','Play Duration Milliseconds', 'Album Artist']
scriptFile = os.path.dirname(os.path.abspath(__file__))
maxFMRows = 57317
rateLimit = 2

def filterCSV(inputCSV):
    df = pd.read_csv(inputCSV)
    df = df[df['Media Duration In Milliseconds'] > 0]
    df = df[df['Event Type'] == 'PLAY_END']
    df = df[df['End Reason Type'] != 'NOT_APPLICABLE']
    df = df[df['Play Duration Milliseconds'] > df['Media Duration In Milliseconds']/2]

    newAlbums = []
    artistsValues = []

    df = df.reset_index(drop=True)
    rowNum = len(df)

    bar = Bar('Finding Artists:', max=rowNum)
    os.system('clear')

    errors = 0

    for index, row in df.iterrows():
        artistValue = str(searchtunes.findArtist(row['Song Name'], row['Album Name']))
        if artistValue == 'No results found' or artistValue == 'Artist not found':
            errors += 1
        artistsValues.append(artistValue)

        albumCorrection = str(row['Album Name'])
        newAlbums.append(albumCorrection)

        bar.suffix = str(round(((index + 1) / rowNum * 100))) + '%% | ' + str(index+1) + '/' + str(rowNum) + ' | ETA: ' + str(datetime.timedelta(seconds = round((rowNum-(index+1))*rateLimit))) + ' | Errors: ' + str(errors)
        bar.next()
        time.sleep(rateLimit)

    bar.finish()

    df['Artists'] = artistsValues
    df['Album Name'] = newAlbums
    df['Album Artist'] = ''
    df = df[keepColumns]

    spliceAndFinalize(df)
def saveCSV(i, df):
    filename = f'outputs\data_chunk_{i + 1}.csv'
    saveToFile = os.path.join(scriptFile, filename)
    df.to_csv(saveToFile, header=False, index=False)

def spliceAndFinalize(df):
    df = df[df['Artists'] != 'Artist not found']
    df = df[df['Artists'] != 'No results found']
    print('Done!')
    chunks = [df[i:i + 3000] for i in range(0, df.shape[0], 3000)]

    for index, chunk in enumerate(chunks):
        saveCSV(index, chunk)

filterCSV(importedCSV)
