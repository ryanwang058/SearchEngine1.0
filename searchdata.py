import os
import json

#this function searches outgoing links from the outgoinglinks.json file
def get_outgoing_links(URL):
    osFile = open("outgoinglinks.json", "r")
    dicOutgoingLinks = json.load(osFile)
    osFile.close()
    
    if URL in dicOutgoingLinks:
        return dicOutgoingLinks[URL]
    else:
        return None
    
def get_incoming_links(URL):
    osFile = open("incominglinks.json", "r")
    dicIncomingLinks = json.load(osFile)
    osFile.close()
    
    if URL in dicIncomingLinks:
        return dicIncomingLinks[URL]
    else:
        return None

def get_page_rank(URL):
    osFile = open("pagerank.json", "r")
    dicPageRank = json.load(osFile)
    osFile.close()

    if URL in dicPageRank:
        return dicPageRank[URL]
    else:
        return -1

def get_idf(word):
    fltIDF = 0
    #so we're going to go into the IDF Value folder
    strFile = word+"_idf.txt"
    osPath = os.path.join("IDF Values", strFile)
    if os.path.exists(osPath):
        osFile = open(osPath,"r")
        fltIDF = float(osFile.readline())
        osFile.close()
    #i forgot to use the log function on this. 
    return fltIDF
    
def get_tf(URL, word):
    fltTF=0
    #we go into the directory with the URL name
    prtDirectory = "crawling"
    tfDirectory = "tf"

    osDirectory = os.path.join(prtDirectory,URL[URL.rfind("/")+1:len(URL)-5])
    osDirectory = os.path.join(osDirectory, tfDirectory)
    if os.path.isdir(osDirectory):
        #if it's a directory, go ahead
        osFile = (word+"_tf.txt")
        osPath = os.path.join(osDirectory, osFile)
        if os.path.isfile(osPath):
            #we go into the word file
            osFile = open(osPath, "r")
            #we read that word file
            fltTF = float(osFile.read())
            osFile.close()
    return fltTF

def get_tf_idf(URL, word):
    fltTFIDF=0
    #we go into the directory with the URL name
    osParentDirectory = "crawling"
    osTFIDFDirectory = "tfidf"

    osDirectory = os.path.join(osParentDirectory,URL[URL.rfind("/")+1:len(URL)-5])
    osDirectory = os.path.join(osDirectory, osTFIDFDirectory)
    if os.path.isdir(osDirectory):
        #if it's a directory, go ahead
        osFile = (word+"_tfidf.txt")
        osPath = os.path.join(osDirectory, osFile)
        if os.path.isfile(osPath):
            #we go into the word file
            osFile = open(osPath, "r")
            #we read that word file
            fltTFIDF = float(osFile.readline().strip())
            osFile.close()
    return fltTFIDF