import math
import searchdata

def search(phrase, boost):

    # lstResults is a list of dictionaries
    # dicPage is each entry in lstResults that tracks url, title and (search) score for the page
    lstResults =[]
    dicPage = {}

    # store url and title to lstResults
    ioFile = open("pages.txt","r")
    strURL = ioFile.readline().strip()
    while(strURL != ""):
        dicPage["url"] = strURL
        dicPage["title"] = strURL[strURL.rfind("/")+1: len(strURL) - 5]
        lstResults.append(dicPage)
        strURL = ioFile.readline().strip()
        dicPage = {}
    ioFile.close()
    
    lstSearchWords = phrase.strip().split()
    
    # calculate tf-idf value for the query and store it to a dictionary
    # key: value = word: [count, tf-idf of this word in the query]
    # e.g., apple: [5, 0.6]
    dicQry = calculateQryTFIDF(lstSearchWords)
    
    # calculate the cosine similarity score for all websites
    lstResults = calculateSimilarityScore(dicQry, lstResults, boost)

    # find and return top 10 similar pages
    lstTopResults = findTopResults(lstResults, 10)
    return lstTopResults

# calculate tf-idf for the query and return a dictionary that contains tf-idf value for all the words in the query
def calculateQryTFIDF(words):
    # dicQry is used to store query words info
    #       word : [count, tf-idf of this word in the query]
    # e.g., apple : [5,0.6]
    dicQry = {}

    numOfWords = len(words)

    for word in words:
        if word in dicQry:
            dicQry[word][0] += 1
        else:
            dicQry[word] = [1,1]
    
    # calculate tf-idf for each word and store it to the first entry of its value
    for word in dicQry:
        tf = dicQry[word][0] / numOfWords
        # tfidf = log2(1+tf) * tf
        dicQry[word][1] = math.log2(1+tf) * searchdata.get_idf(word)

    return dicQry

def calculateSimilarityScore(dict, list, boost):
    # for each search word in dict, calculate similarity score and store it to the list (dictionary list that tracks url, title and score)
    for index in range(len(list)):

        numerator = 0
        denominator = 0
        sumSqrDocTFIDF = 0
        sumSqrQryTFIDF = 0
            
        for word in dict:
            docTFIDF = searchdata.get_tf_idf(list[index]["url"], word)
            qryTFIDF = dict[word][1]

            # calculate the numerator
            numerator += docTFIDF * qryTFIDF

            # calculate the denominator factors
            sumSqrDocTFIDF += docTFIDF**2
            sumSqrQryTFIDF += qryTFIDF**2
        
        # calculate the denominator
        denominator = math.sqrt(sumSqrDocTFIDF * sumSqrQryTFIDF)

        # calculate the final result
        if(denominator == 0):
            list[index]["score"] = 0
        else:
            score = numerator/denominator
            if boost:
                # score multiplied by page rank
                score *= searchdata.get_page_rank(list[index]["url"])
            list[index]["score"] = score
    return list

def findTopResults(list, num):
    topResults = []
    # make sure the required top num is no more than the length of the unsorted list
    if len(list) >= num:
        for i in range(num):
            score = -1
            index = 0
            page = {}
            for j in range(len(list)):
                if (list[j]["score"]) > score:
                    page = list[j]
                    score = list[j]["score"]
                    index = j
            topResults.append(page)
            list.pop(index)
        return topResults
    else:
        return None
