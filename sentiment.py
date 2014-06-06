#  This script applies the AFINN-111.txt word sentiment scores to
#  longer texts, and then shows and saves a graph of the moving average
#  of the sentiment score.  Other functions provide additional features
#  and are noted below.
#
#  Note:  This was written for Python 2.7.  Required libraries are below.
#  I think only numpy and matplotlib need to be installed. The rest are
#  already included with a standard python installation.
#
#  If you execute from the terminal, you'll need to pass two parameters:
#
#   - movAvPeriod (number of words to include in the moving average period, e.g., 550)
#   - fileName (name of txt file with or without the full path to evaluate, e.g, mytext.txt)
#
#  Also, this saves a pdf copy of the graph to your drive in the current dir.
#  It will overwrite previous copies of the graph made that same day.
#  There's also a function in here to create a new txt file of the text, but
#  that file will have the score along side each line.  That function works,
#  but it could use some cleanup (e.g., punctuation is stripped in the document
#  it creates).
#
#  To execute from the command line, just save this script in the folder
#  with the txt file you want to evaluate, and then from the terminal:
#
#     > python sentiment.py 550 nameOfFile.txt
#
#  This may not work depending on what directories you have in your PATH
#  variables.  If that sounds like a headache, you may be better off
#  downloading pycharm.  It's free.  It's awesome. And you can edit
#  and execute code all at once, all in the same place.
#
#  Questions?  Email me:  ctgrant@gmail.com
#  As for licenses:  Be nice, give credit, and let me know if you do something interesting.

import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import re
import urllib
from sys import argv
import datetime



########################################################################
########################################################################
###
###  Script Functions
###


### Currently used in commands below.

# Grabs AFINN-111.txt from github and puts it into a dict object.
def readSentimentFileFromGit():
    '''
    This function grabs AFINN-111.txt from an online
    resource, and then it creates a dictionary object
    from that list.  The dictionary is used as we score
    texts. (Thank you Univ. of Washington and Finn Arup
    Nielsen.) 
    '''
    page = urllib.urlopen('https://raw.githubusercontent.com/uwescience/datasci_course_materials/master/assignment1/AFINN-111.txt')
    wordScores = {}
    for line in page:
        term, score = line.split('\t')
        score = score.rstrip('\n')
        wordScores[term] = int(score)
    return wordScores


# Grabs a local copy of AFINN-111.txt and puts it into a dict object.
def readSentimentFileLocal(sntFilePath):
    '''
    Provide the path name to a local copy of AFINN-111.txt,
    and this function will return a dictionary object with
    words and their scores.
    '''
    checkFileAvailability(sntFilePath)
    afinnfile = open(sntFilePath, 'r')
    wordScores = {}  # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split('\t')  # Splits on the tab character that's in this file.
        score = score.rstrip('\n')
        wordScores[term] = int(score)  # Convert the score to an integer.
    return wordScores


# Checks if the text file is there, called by other functions.
def checkFileAvailability(fileName):
    '''
    Checks to see if the fileName points to a file that exists.
    fileName should have the full file path (note, however, this
    can be the filepath starting at the current working directory.
    If the file isn't present, it'll print an error message.
    But this needs better error handling.
    '''

    locations = [m.start() for m in re.finditer('/', fileName)]
    if len(locations) == 0:
        fileDir = os.getcwd()
    elif (len(fileName)-1 == locations[-1]):
        endString = locations[-2]
        fileDir = fileName[0:endString]
        fileName = fileName[locations[-2]+1:locations[-1]]
        print("The file is there, but don't put the extra '/' on the end of your path")
    else:
        endString = locations[-1]
        fileDir = fileName[0:endString]
        fileName = fileName[locations[-1]+1:]
    print(fileDir)
    contents = os.listdir(fileDir)
    if fileName in contents:
        print("Yes, it's there")
    else:
        print("The file was not found.")
        # This is a crappy error handling approach as it
        # doesn't handle anything, but we'll get there later.
        return("Error: File not available.")


# Read in the text to score, and spit it out as a python list of words.
def textToList(fileName):
    '''
    This opens the text to be read. File should be a txt file.
    Returns a list with each individual word separated.
    Some issues remain with contractions, we'll sort that out later.
    '''
    checkFileAvailability(fileName)
    # Open and read the file.
    f = open(fileName, 'U')
    text = f.readlines()
    f.close()
    # Tokenize the text
    text = [i.strip().split() for i in text]
    # This is where we'll need to keep a copy with punct.
    # Come back later, keep that, and it'll make for a
    # prettier version for printing later.
    textList = []
    for aLine in text:
        for aWord in aLine:
            textList.append(aWord)
    # Then strip the punctuation
    for i in range(0,len(textList)):
        textList[i] = re.sub(r'[^\w\s]','',textList[i])
    return textList


# This actually scores the words
def scoreTextWordList(wordList):
    '''
    This takes our existing text list and word score dictionary,
    and scores stuff.
    '''
    # Now score each word
    wordSentimentScores = []
    for word in wordList:
        if word in sentDict:
            wordSentimentScores.append(sentDict[word])
        else:
            wordSentimentScores.append(0)
    return wordSentimentScores


# Now create our moving average using this number
def findMovAvgScore(wordSentimentScores, movingAveragePeriod=550):
    '''
    This generates our simple moving average based on sentiment score
    list passed to it.  Moving average period defaults to 550, but
    can be adjusted.
    '''
    movAvgScore = []
    for i in range(0,movingAveragePeriod):
        movAvgScore.append(0)
    for i in range(movingAveragePeriod,len(wordSentimentScores),1):
        rollScore = wordSentimentScores[(i-movingAveragePeriod):i]
        movAvg = np.mean(rollScore)
        movAvgScore.append(movAvg)
    return movAvgScore


# Okay, now lets do some plotting
# This also saves a copy of the graph as a pdf.
# NOTE: THIS WILL MERCILESSLY OVERWRITE PREVIOUS COPIES OF ANY GRAPH YOU
# MADE ON THE SAME DATE, OR ANY OTHER FILE YOU HAPPENED TO HAVE WITH THAT
# SAME NAME THAT IS IN THE SAME DIRECTORY.
def plotScoreMA(movAvgScore, textName, movingAveragePeriod=550):
    font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 6}
    matplotlib.rc('font', **font)
    plt.plot(movAvgScore)
    plt.suptitle("File: " + textName + " - Moving Average Period: " + str(movingAveragePeriod))
    plt.ylabel("Sentiment Score")
    xticks = np.arange(0,len(movAvgScore),500)
    plt.xticks(xticks)
    for i in range(0,len(movAvgScore),1000):
        matplotlib.pyplot.axvline(i,ymin = -1, ymax = 1)
    fileSaveName = textName + " " + str(datetime.datetime.now().date()) + ".pdf"
    plt.savefig(fileSaveName, papertype = 'letter')
    plt.show()


##############################################
### Not currently used, but potentially useful.

# Prints text to the console (with some limitations), but helpful to read
# certain key points.
def printText(wordList, movAvgScore, start=550, end=1000):
    '''
    This will print lines of text with the score next to each line.
    The printed score is the score at the end of that line.
    That score is also multiplied by 100, because it's easier to read.
    JUST NOTICED:  This misses the last partial fragment of text (modulo remainder).
    Fix later.
    '''
    for i in range(start,end,10):
        score = "%.3f" % (movAvgScore[i] * 100)
        if len(score) == 6:
            filler = " "
        else:
            filler = "  "
        print(str(i) + "\t" + filler + str("%.3f" % (movAvgScore[i] * 100)) + ": \t"+ " ".join(wordList[(i-20):(i)]))


# Instead of printing to the console, this saves a new file with the
# text and scores.  No punctuation.  Fix later.  THIS WILL OVERWRITE ANY
# FILE WITH THE SAME NAME.  THIS SAVES THE FILE AS THE SAME NAME AS THE
# TEXT FILE BEGIN SCORED, BUT IT ADDS THE DATE.  SO ESSENTIALLY IF YOU
# RUN THIS TWICE IN THE SAME DAY, IT'LL OVERWRITE THE PRIOR TEXT FILE
# YOU MADE USING THIS FUNCTION HERE.  (OR ANY OTHER RANDOM FILE THAT
# YOU HAPPEN TO HAVE THAT HAS THIS SAME NAME THAT IS IN THE SAME DIRECTORY.)
def saveText(wordList, movAvgScore, fileName):
    '''
    This will save a text file with the text and the score next to each line.
    The printed score is the score at the END of that line.
    That score is also multiplied by 100, because it's easier to read.
    ALSO, THIS WILL MERCILESSLY OVERWRITE ANY FILE WITH THE SAME NAME
    NOTE: I HAVE THIS FUNCTION ADDING THE DATE TO THE FILE NAME SO THAT
    IT'S LESS LIKELY TO OVERWRITE ANYTHING YOU ALREADY HAVE, BUT BE WARNED.
    '''
    time = datetime.datetime.now()
    saveName = fileName + " " + str(time.date()) + '.txt'
    file = open(saveName, 'w')
    fileContents = []
    for i in range(0,len(wordList),10):
        score = "%.3f" % (movAvgScore[i] * 100)
        if len(score) == 6:
            filler = " "
        else:
            filler = "  "
        file.write("%s\n" % (str(i) + "\t" + filler + str("%.3f" % (movAvgScore[i] * 100)) + ": \t"+ " ".join(wordList[(i-20):(i)])))
    file.close


# Shows scored words only from a text, along with related info.
def showSentWords(wordList, wordSentimentScores, movAvgScore):
    '''
    This function shows only the words that were scored in
    a text, along with their position and the current moving
    average score, and the score of that word.
    '''
    for i in range(0,len(wordSentimentScores)):
        if wordSentimentScores[i] != 0:
            print(str(i) + " (" + str(movAvgScore[i])[0:6] + ")" + ": \t" + str(wordList[i]) + " " + str(wordSentimentScores[i]))


# Function to print out as 2 columns score and word.  Not great.
def printWordScoreOverRange(wordSentimentScores, wordList, start=0, end=500):
    for i,j in zip(wordSentimentScores[start:end], wordList[start:end]):
        print(str(i) + "\t\t" + j)


# Function to locate all of the places a word occurs.  Not explicitly used
# in this script, but helpful to see where it is.
def locateWord(theWord, wordList):
    locations = []
    for i,j in enumerate(wordList):
        if j == theWord:
            locations.append(i)
    return locations


# For scoring only the positive words.  Not currently used in this script.
def positiveWordsScore(wordList):
    posScore = []
    for word in wordList:
        if word in sentDict:
            if sentDict[word] > 0:
                posScore.append(sentDict[word])
            else:
                posScore.append(0)
        else:
            posScore.append(0)
    return posScore


# For scoring only the negative words.  Not currently used in this script.
def negativeWordsScore(wordList):
    negScore = []
    for word in wordList:
        if word in sentDict:
            if sentDict[word]<0:
                negScore.append(sentDict[word])
            else:
                negScore.append(0)
        else:
            negScore.append(0)
    return negScore


###
###
###
########################################################################
########################################################################


# If you execute from an ide, or some other means, you can assign
# movAvPeriod and fileName yourself.

# If you're executing from the command line, it'll call these
# and properly assign your variables.

# movAvPeriod should be the number of words to include in the
# moving average period.

# fileName is the name of the file with or without the full path
# that points to the txt file you want to evaluate.

print(argv)
movAvPeriod, fileName = argv[1:]

movAvPeriod = int(movAvPeriod)

# fileName = 'simi.txt'
# Choose our moving average period.
# movAvPeriod = 550

# Let's get our script into our environment.
# sentDict = readSentimentFile("AFINN-111.txt")
sentDict = readSentimentFileFromGit()
wordList = textToList(fileName)
wordSentimentScores = scoreTextWordList(wordList)
movAvgScore = findMovAvgScore(wordSentimentScores, movAvPeriod)
plotScoreMA(movAvgScore, fileName, movAvPeriod)

printText(wordList, movAvgScore, len(wordList)-250, len(wordList))
print("Printed the last 250 words")
