import math
import webdev
import os
import json
import matmult

osParentDirectory = "crawling"
osTFDirectory = "tf"
osTFIDFDirectory = "tfidf"

def crawl(seed):
    #first, make a list of all the links we've gone to
    lstPagesVisited=[]
    #make a queue for what pages we should visit
    lstQueue = []
    #dicOutgoingLinks will record what pages we've been to
    dicOutgoingLinks = {}
    #dicIncomingLinks will record incoming links of the pages
    dicIncomingLinks = {}
    #dicAllWords will basically record all the words we've been to
    dicAllWords={}
    
    # reset information
    resetInformation()

    #every time we come across a page, we add it to pages.txt
    osPagesFile = open("pages.txt", "a")
    lstQueue.append(seed)

    
    #while there's still something in the queue
    while(len(lstQueue)>0):
        #each time we go through one link
        strSubPage = lstQueue[0]
        #If the links found in page aren't in the queue or in the pages visited, add it to the list
        outGoingLinks = getOutgoingLinks(strSubPage)
        dicOutgoingLinks[strSubPage] = outGoingLinks
        # add the links to the dictionary of incoming list
        for url in outGoingLinks:
            dicValueAppendElement(dicIncomingLinks, url, strSubPage)
        #since we've gone on that page, let's add it to the pages we've visited
        lstPagesVisited.append(strSubPage)
        #We then add the page we've just visited to the text file
        osPagesFile.write(strSubPage+"\n")
        
        #this function records all the info we need in searchdata.py
        recordInformation(strSubPage, dicAllWords)
        #we then get rid of the website we've just visitied which is at lstQueue[0]
        lstQueue.pop(0)
        #for every link inside the page we're on, 
        for strLink in dicOutgoingLinks[strSubPage]:
            #if it's not in the queue already and not a key in dicOutgoingLinks visited, then
            if((strLink not in dicOutgoingLinks) and (strLink not in lstQueue)):
                #add that page to the queue
                lstQueue.append(strLink)
    #after we're done going through all the pages, close pages.txt
    osPagesFile.close()

    #record outgoing links and incoming links
    recordOutgoingLinksFile(dicOutgoingLinks)
    recordIncomingLinksFile(dicIncomingLinks)
    
    #Now that we have the pages we've been to, we can do the easy bit of recording IDF values
    recordIDF(dicAllWords, dicOutgoingLinks)

    # record tf-idf of every page
    osDirectory = osParentDirectory
    lstPages = os.listdir(osDirectory)
    for page in lstPages:
        osDirectory = os.path.join(osDirectory, page)
        recordTFIDF(osDirectory)
        osDirectory = osParentDirectory

    #create page rank file
    createPageRankFile()

    #the number of pages we visited will be the number of pages there are since we visited all of them
    return len(lstPagesVisited)

#O(n^m) due to finite number of processes
def resetInformation():
    # reset directory "crawling"
    if os.path.isdir(osParentDirectory):
        recursiveDeleteDirectory(osParentDirectory)
    #then create a new directory
    createNewDirectory(osParentDirectory)

    #reset directory "IDF Values"
    if os.path.isdir("IDF Values"):
        recursiveDeleteDirectory("IDF Values")
    #then create a new directory
    createNewDirectory("IDF Values")

    #we need to reset what's inside the pages.txt file
    if os.path.isfile("pages.txt"):
        os.remove("pages.txt")

#this function will write down the info into a file
#O(n) time due to functions called that are O(n)
def recordInformation(strSubPage, dicAllWords):
    #break down the lines
    lstLines=webdev.read_url(strSubPage).strip().split("\n")
    #dicWords will store the number of times a word appears
    #apple : 3
    #peach : 5
    dicWords={}
    
    #we'll read the whole thing
    countWord(lstLines, dicWords)
    
    # create new directory
    osDirectory = strSubPage[strSubPage.rfind("/")+1:len(strSubPage)-5]
    # joining parent directory
    osDirectory = os.path.join(osParentDirectory, osDirectory)

    # recursiveDeleteDirectory(osDirectory)
    createNewDirectory(osDirectory)
    
    #create a file and then write into it
    recordWordCount(osDirectory,dicWords,dicAllWords)
    
    #create a file that keeps track of how many words there are
    recordTotalWordCount(osDirectory,dicWords)

    #store the term frequency
    recordTF(osDirectory,dicWords)

#This generally updates a dictionary with the number of words inside
#O(n^2) time
def countWord(lstLines, dicWords):
    #for every line in the html page
    for strLine in lstLines:
        #If it starts with "<p>", then we know it has paragraphs
        if(strLine.strip().endswith("<p>")):
            blnParse = True
        if(strLine.strip()==("</p>")):
            blnParse = False
            
        #if it's time to parse the paragraph, then...
        if(blnParse==True and not strLine.strip().endswith("<p>")):
            #if it's not in the dictionary, make it 1
            if(strLine not in dicWords):
                dicWords[strLine]=1
            #otherwise, add 1
            else:
                dicWords[strLine]+=1

#This function checks if a directory exists and deletes it
#O(n^n) time
def recursiveDeleteDirectory(osDirectory):
    for entry in os.listdir(osDirectory):
        if os.path.isdir(os.path.join(osDirectory,entry)):
            recursiveDeleteDirectory(os.path.join(osDirectory,entry))
        elif os.path.isfile(os.path.join(osDirectory,entry)):
            os.remove(os.path.join(osDirectory,entry))
    os.rmdir(osDirectory)

#O(1)
def createNewDirectory(osDirectory):
    #If the directory doesn't exist
    if not os.path.exists(osDirectory):
        #make a directory
        os.makedirs(osDirectory)

#This function creates files for every word and prints the number of times that word appears
#O(n) time
def recordWordCount(osDirectory, dicWords, dicAllWords):
    #for every key value(word) inside the dicWords dictionary,
    for strWord in dicWords:
        #create the file name
        strFileName = strWord+".txt"
        #make the path
        osPath = os.path.join(osDirectory,(strFileName))
        #open the file
        osFile = open(osPath, "w")
        #write the amount of times that word pops up into the file
        osFile.write(str(dicWords[strWord]))
        #then close the file
        osFile.close()
        #if the word isn't a part of dictionary of all words, then
        if(strWord not in dicAllWords):
            #make the word a key and make the value(number of times it comes up) 1
            dicAllWords[strWord]=1
        #if it's already a key but it pops up anyway, then we know the word occurs again
        else:
            #so we add 1
            dicAllWords[strWord]+=1

#This function creates a file for every word term frequency
#O(n) time
def recordTF(osDirectory,dicWords):
    #first, we read the number of total numbre of word
    osPath = os.path.join(osDirectory,("total.txt"))
    osFile = open(osPath, "r")
    fltTotal = float(osFile.readline())
    osFile.close()

    # create tf
    osDirectory = os.path.join(osDirectory,osTFDirectory)
    createNewDirectory(osDirectory)
    
    #for every word in dicWords
    for strWord in dicWords:     
        #now, we record the term frequencies
        osPath = os.path.join(osDirectory,(strWord+"_tf.txt"))
        #open the file
        osPath = open(osPath, "w")
        #write into it
        osPath.write(str(float(dicWords[strWord])/fltTotal))
        #then close the file
        osPath.close()

#This function creates a file that prints out the total words in a page
#O(n) time
def recordTotalWordCount(osDirectory, dicWords):
    #initialize the total
    intTotal=0
    #find the path
    strPath = os.path.join(osDirectory,("total.txt"))
    osFile = open(strPath, "w")
    #for every word in dicWords
    for strWord in dicWords:
        #add the number of times a word apears into inttotal
        intTotal+=dicWords[strWord]
    
    #then print out 
    osFile.write(str(intTotal))
    osFile.close()

#O(n) time
def recordIDF(dicAllWords,dicOutgoingLinks):
    intTotalDocuments = len(dicOutgoingLinks)
    #for every word in the dictionary of all words
    for strWord in dicAllWords:
        #enter the idf directory
        osPath = os.path.join("IDF Values", strWord+"_idf.txt")
        #create the IDF value for the word
        osPath = open(osPath,"w")
        osPath.write(str(math.log2(intTotalDocuments/(1+dicAllWords[strWord]))))
        osPath.close()

def recordTFIDF(osDirectory):
    
    # read tf
    osInDirectory = os.path.join(osDirectory, osTFDirectory)
    lstTF = os.listdir(osInDirectory)
    dicTFIDF = {}
    for tf in lstTF:
        osPath = os.path.join(osInDirectory,tf)
        filein = open(osPath, "r")
        dicTFIDF[tf[0: tf.find("_")] + "_tfidf.txt"] = [float(filein.readline().strip()),0]
        filein.close()
    
    # read idf
    osInDirectory = "IDF Values"
    lstIDF = os.listdir(osInDirectory)
    for idf in lstIDF:
        if idf[0: idf.find("_")] + "_tfidf.txt" in dicTFIDF:
            osPath = os.path.join(osInDirectory,idf)
            filein = open(osPath, "r")
            dicTFIDF[idf[0: idf.find("_")] + "_tfidf.txt"][1] = float(filein.readline().strip())
            filein.close()

    # write word_tfidf.txt
    # 1. create tf-idf directory
    osOutDirectory = os.path.join(osDirectory, osTFIDFDirectory)
    createNewDirectory(osOutDirectory)

    # 2. write tfidf txts from dicTFIDF
    for tfidf in dicTFIDF:
         osPath = os.path.join(osOutDirectory,tfidf)
         fileout = open(osPath, "w")
         fileout.write(str(math.log2(1+dicTFIDF[tfidf][0])*dicTFIDF[tfidf][1]))
         fileout.close()

def getOutgoingLinks(url):

    lstLines = webdev.read_url(url).strip().split("\n")

    # 2 variables to keep track of the beginning and end of a link
    intStart = 0
    intEnd = 0
    
    strBeginning = url[0:url.rfind("/")+1]
    strLink = ""
    lstLinks=[]
    
    #we'll read the whole thing
    for strLine in lstLines:
        #If it starts with "<a href", then we know it has a link to another pages
        if(strLine.startswith("<a href")):
            #find the index of the first "
            intStart = strLine.find('"')
            #find the index of the last "
            intEnd = strLine.rfind('"')
            #everything in between the " " will be the link
            strLink = strLine[intStart+1:intEnd]
            
            #If it's a relative link(it starts with "./", we'll add the absolute start onto the name of it
            #Instead of "./N-0.html
            if(strLink.startswith("./")):
                #It will be https://scs.carleton.N-0.html now I think
                strLink = strBeginning+strLink[2:len(strLink)]
            #now we add the link to our list of links
            lstLinks.append(strLink)
    return lstLinks

#O(1)
def recordOutgoingLinksFile(dict):
    #make the file in the general directory
    file = open( "outgoinglinks.json", "w")
    json.dump(dict,file)
    file.close()

def recordIncomingLinksFile(dict):
    #make the file in the general directory
    file = open( "incominglinks.json", "w")
    json.dump(dict,file)
    file.close()

# create a dictionary with all the urls and their page rank and store it in a json file 
def createPageRankFile():
    # page rank for all the URLs
    alpha = 0.1
    euclideanDistThreshold = 0.0001
    
    row = [] # row of the adjacency matrix
    adjacencyMatrix = [] # N * N matrix
    dict = {} # id -> link, e.g., 1:'http://.../N-3.html'
    reversedDict = {} # link -> id, e.g., 'http://.../N-3.html':1
    
    # create dict and reverse dict
    count = 0
    filein = open("pages.txt", "r")
    link = filein.readline().strip()
    while link != "":
        dict[count] = link
        reversedDict[link] = count
        count += 1
        link = filein.readline().strip()
    filein.close()
    
    # load outgoing links
    file = open("outgoinglinks.json", "r")
    outgoinglinks = json.load(file)
    file.close()

    # create adjacency matrix
    adjacencyMatrix = [-1] * len(dict)
    row = [-1] * len(dict)
    for id in dict:
        for link in reversedDict:
            if link in outgoinglinks[dict[id]]:
                row[reversedDict[link]] = 1
            else:
                row[reversedDict[link]] = 0
        adjacencyMatrix[id] = row
        row = [-1] * len(dict)
    
    # scaled adjacency matrix after adding alpha/N to each entry
    count = 0
    for i in range(len(adjacencyMatrix)):
        for j in range(len(adjacencyMatrix[0])):
            if adjacencyMatrix[i][j] == 1:
                count += 1
        if count == 0:
            for j in range(len(adjacencyMatrix[0])):
                adjacencyMatrix[i][j] = (1 / len(adjacencyMatrix)) * (1-alpha) + (alpha / len(adjacencyMatrix))
        else:
            for j in range(len(adjacencyMatrix[0])):
                adjacencyMatrix[i][j] = (adjacencyMatrix[i][j] / count) * (1-alpha) + (alpha / len(adjacencyMatrix))
        count = 0
    
    # power iteration with adjacency matrix
    # initialize iterating vector
    iteratingVector = [[1 / len(adjacencyMatrix)] * len(adjacencyMatrix)]
    
    # use modules of matmult in tutorial4 to calculate
    finalPageRankVector = matmult.mult_matrix(iteratingVector, adjacencyMatrix) 
    dist = matmult.euclidean_dist(finalPageRankVector, iteratingVector)

    # iterate until dist < euclideanDistThreshold when we find the stable final page rank vector
    while dist >= euclideanDistThreshold:
        iteratingVector = finalPageRankVector
        finalPageRankVector = matmult.mult_matrix(iteratingVector, adjacencyMatrix)
        dist = matmult.euclidean_dist(finalPageRankVector, iteratingVector)
    
    # write a json file contains all the page urls and their page rank.
    # key = url, value = page rank
    dicPageRank = {}
    for url in reversedDict:
        # reversedDict: key=url, value=id. So finalPageRankVector[0][id] is the page rank result for the url with this id
        dicPageRank[url] = finalPageRankVector[0][reversedDict[url]]
    fileout = open("pagerank.json", "w")
    json.dump(dicPageRank,fileout)
    fileout.close()

def dicValueAppendElement(dict, key, value):
    if not(key in dict):
        dict[key] = [value]
    else:
        dict[key].append(value)
