MovingAverageSentimentAnalysis
==============================

This script applies the AFINN-111.txt word sentiment scores to
longer texts, and then shows and saves a graph of the moving average
of the sentiment score.  Other functions provide additional features
and are noted below.  This is a bit of a departure from the normal 
tweet scoring that I've seen. 

Note:  This was written for Python 2.7.  Required libraries are below.
I think only numpy and matplotlib need to be installed. The rest are
already included with a standard python installation.

If you execute from the terminal, you'll need to pass two parameters:

 - movAvPeriod (number of words to include in the moving average period, e.g., 550)
 - fileName (name of txt file with or without the full path to evaluate, e.g, mytext.txt)

Also, this saves a pdf copy of the graph to your drive in the current dir.
It will overwrite previous copies of the graph made that same day.
There's also a function in here to create a new txt file of the text, but
that file will have the score along side each line.  That function works,
but it could use some cleanup (e.g., punctuation is stripped in the document
it creates).

To execute from the command line, just save this script in the folder
with the txt file you want to evaluate, and then from the terminal:

   > python sentiment.py 550 nameOfFile.txt

This may not work depending on what directories you have in your PATH
variables.  If that sounds like a headache, you may be better off
downloading pycharm.  It's free.  It's awesome. And you can edit
and execute code all at once, all in the same place.

Questions?  Email me:  ctgrant at gmail.com

As for licenses:  Be nice, give credit, and let me know if you do something interesting. 
