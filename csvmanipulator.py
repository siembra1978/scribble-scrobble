# Written by siembra1978
import numpy as np
import pandas as pd
import searchmusic
import searchtunes
import os
import subprocess
import platform
import time
from progress.bar import Bar
import datetime

importedCSV = "Apple Music Play Activity.csv"
keepColumns =['Artists', 'Song Name', 'Album Name','Play Duration Milliseconds', 'Album Artist']
scriptFile = os.path.dirname(os.path.abspath(__file__))
rateLimit = 2

def setTitle(title):
    title = str(title)
    if platform.system() == "Windows":
        os.system(f"title {title}")
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")
        sys.stdout.flush()
def filterCSV(inputCSV):
    df = pd.read_csv(inputCSV)
    df = df[df['Media Duration In Milliseconds'] > 0]
    df = df[df['Event Type'] == 'PLAY_END']
    df = df[df['End Reason Type'] != 'NOT_APPLICABLE']
    df = df[df['Play Duration Milliseconds'] > df['Media Duration In Milliseconds']/2]

    newAlbums = []
    artistsValues = []

    lastIteration = [None]
    timeTable = []
    timeElapsed = 0
    avgTimeDiff = 0

    df = df.reset_index(drop=True)
    rowNum = len(df)

    bar = Bar('| Finding Artists', max=rowNum)
    setTitle('Finding Artists...')

    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

    errors = 0
    notFound = 0

    timeInit = time.time()

    for index, row in df.iterrows():

        now = time.time()

        if lastIteration[0] is not None:
            timeElapsed = now - lastIteration[0]
            timeTable.append(timeElapsed)
            avgTimeDiff = sum(timeTable) / len(timeTable)

        lastIteration[0] = now

        artistValue = str(searchtunes.findArtist(row['Song Name'], row['Album Name']))

        if artistValue == 'Error':
            errors += 1
        elif artistValue == 'No results found' or artistValue == 'Artist not found':
            notFound +=1

        artistsValues.append(artistValue)

        albumCorrection = str(row['Album Name'])
        newAlbums.append(albumCorrection)

        # progress stuff
        percentComplete = str(round(((index + 1) / rowNum * 100))) + '%'
        indexedProgress = str(index+1) + '/' + str(rowNum)
        estimatedTime = str(datetime.timedelta(seconds = round((rowNum-(index+1))*avgTimeDiff)))
        overallTimeElapsed = str(datetime.timedelta(seconds = round((now - timeInit))))

        bar.suffix = percentComplete + '% | ' + indexedProgress + ' | ETA: ' + estimatedTime + ' | Time Elapsed: ' + overallTimeElapsed + ' | Artists Not Found: ' + str(notFound) + ' | Errors: ' + str(errors) + ' | '
        setTitle(percentComplete + ' [] ETA: ' + estimatedTime)

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
    df = df[df['Artists'] != 'Error']
    chunks = [df[i:i + 3000] for i in range(0, df.shape[0], 3000)]

    for index, chunk in enumerate(chunks):
        saveCSV(index, chunk)

filterCSV(importedCSV)
print('Done!')
setTitle("Done!")
input('Press enter to exit: ')