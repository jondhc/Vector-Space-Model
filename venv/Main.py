#!/usr/bin/python3

import sys
import os
import pprint
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from xml.dom import minidom
import math
import collections
from operator import itemgetter
from matplotlib import pyplot
import numpy
#import untangle
dictionary = {}
idfDictionary = {}
relevantdictionary = {}
average = [0,0,0,0,0,0,0,0,0,0,0]
b = numpy.array(average)


def indexDocumentFrequency(totalNumberOfDocuments, documentsWithTermAppearance):
    return math.log10((totalNumberOfDocuments/documentsWithTermAppearance))

def similarityCoefficient(queryVector, documentVector):
    result = 0
    for i in range(0, len(queryVector)):
        result = result + (queryVector[i] * documentVector[i])
    return result


def tokenize(text):
    tokens = set(word_tokenize(text))
    return tokens


def createDictionary(terms, doc):
    for k in terms:
        dictionary.setdefault(k, []).append(doc)


def showDictionary(arg):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(list(arg.items()))


def getPosting(key):
    return dictionary[key]

#######################################################

def performAndQuery(post1, post2):
    results = []
    for i in post1:
        if i in post2:
            results.append(i)
    return results


def performOrQuery(post1, post2):
    return list(set(post1 + post2))


def performNotQuery(post):
    results = []
    for i in range(1, len(documents)):
        if documents[i] not in post:
            results.append(i)
    return results


def performAndQueryOrQuery(term1, term2, term3):  # and - or
    return list(performOrQuery((performAndQuery(getPosting(term1), getPosting(term2))), getPosting(term3)))


def performAndQueryAndQuery(term1, term2, term3):  # and - and
    return list(performAndQuery((performAndQuery((getPosting(term1)), (getPosting(term2)))), (getPosting(term3))))


def performAndQueryNotQuery(term1, term2):  # not - and
    return list(performAndQuery((term1), (performNotQuery(getPosting(term2)))))


def performOrQueryOrQuery(term1, term2, term3):  # or -or
    return list(performOrQuery((getPosting(term1)), (performOrQuery((getPosting(term2)), (getPosting(term3))))))


def performOrQueryNotQuery(term1, term2):  # not - or
    return list(performOrQuery((getPosting(term1)), (performNotQuery(getPosting(term2)))))


def performOrQueryAndQuery(term1, term2, term3):  # or - and
    return list(performAndQuery((performOrQuery((getPosting(term1)), (getPosting(term2)))), (getPosting(term3))))

#######################################################


def makeQuerys():
    print("What kind of query do you want?: ")
    print("a  ->  Simple AND Query")
    print("o  ->  Simple OR Query")
    print("n  ->  Simple NOT Query")
    print("aa ->  Query with AND - AND")
    print("ao ->  Query with AND - OR")
    print("an ->  Query with AND - NOT")
    print("oa ->  Query with OR - AND")
    print("oo ->  Query with OR - OR")
    print("on ->  Query with OR - NOT")
    print("b ->   Back to the previous menu")
    case = input()
    case.lower()
    showDictionary(dictionary)
    print()
    if case == "a":
        term1 = input("First term: ")
        term2 = input("Second term: ")
        print(performAndQuery((getPosting(term1)), (getPosting(term2))))
        mainOptions()
    elif case == "o":
        term1 = input("First term: ")
        term2 = input("Second term: ")
        print(performOrQuery((getPosting(term1)), (getPosting(term2))))
        mainOptions()
    elif case == "n":
        term1 = input("Termino: ")
        print(performNotQuery((getPosting(term1))))
        mainOptions()
    elif case == "aa":
        term1 = input("First term: ")
        term2 = input("Second term: ")
        term3 = input("Third term: ")
        print(performAndQueryAndQuery(term1, term2, term3))
        mainOptions()
    elif case == "ao":
        term1 = input("First term: ")
        term2 = input("Second term: ")
        term3 = input("Third term: ")
        print(performAndQueryOrQuery(term1, term2, term3))
        mainOptions()
    elif case == "an":
        term1 = input("First term: ")
        term2 = input("Second term: ")
        term3 = input("Third term: ")
        print(performAndQueryNotQuery(term1, term2))
        mainOptions()
    elif case == "oa":
        term1 = input("First term: ")
        term2 = input("Second term: ")
        term3 = input("Third term: ")
        print(performOrQueryAndQuery(term1, term2, term3))
        mainOptions()
    elif case == "oo":
        term1 = input("First term: ")
        term2 = input("Second term: ")
        term3 = input("Third term: ")
        print(performOrQueryOrQuery(term1, term2, term3))
        mainOptions()
    elif case == "on":
        term1 = input("First term: ")
        term2 = input("Second term: ")
        term3 = input("Third term: ")
        print(performOrQueryNotQuery(term1, term2))
        mainOptions()
    elif case == "b":
        os.system("clear")
        mainOptions()
    else:
        os.system("clear")
        print("Your option is invalid. Please try again")
        makeQuerys()

#######################################################


def mainOptions():
    print()
    print("These are the tasks you can do:")
    print("p -> Print the Inverted Index ")
    print("q -> Make a Query")
    print("e -> Exit of program")
    op = input("Please choose an option to do: ")
    op.lower()

    if op == "p":
        os.system("clear")
        showDictionary(dictionary)
        next = input("Would you like to do anything else? (yes/no): ")
        next.lower()
        if next == "yes":
            print()
            mainOptions()
        else:
            print("Thanks for comming!")
            sys.exit()
    elif op == "q":
        os.system("clear")
        makeQuerys()
    elif op == "e":
        print("Thanks for comming!")
        sys.exit()

#######################################################

def openDocs():
    for doc in os.listdir("./cranfield.all"):
        createTermDictionary(getDocNo(doc), parseDoc(doc))
    #print(dictionary)

def parseDoc(document):
    doc = minidom.parse("./cranfield.all/" + document)
    textElement = doc.getElementsByTagName('TEXT')[0]
    textContent = textElement.firstChild.data
    titleElement = doc.getElementsByTagName('TITLE')[0]
    titleContent = textElement.firstChild.data
    #print(getDocNo(document))
    return textContent + titleContent

def getDocNo(document):
    doc = minidom.parse("./cranfield.all/" + document)
    numberElement = doc.getElementsByTagName('DOCNO')[0]
    number = numberElement.firstChild.data
    return number

def createTermDictionary(docNo, text):

    stopWordsList = stopwords.words('english')
    stopWordsList.append(",")
    stopWordsList.append(".")
    stopWordsSet = set(stopWordsList)

    tokensList = word_tokenize(text)
    tokensListWOStopwords = []
    for token in tokensList:
        if token not in stopWordsSet:
            tokensListWOStopwords.append(token)
    tokensCounter = collections.Counter(tokensListWOStopwords)
    #print(docNo)
    #print(tokensCounter)

    for element in tokensCounter:
        dictionary.setdefault(element, {})[docNo.strip()] = tokensCounter[element]


def calculateIDF():
    for x in dictionary:
        idfDictionary[x] = indexDocumentFrequency(1400,len(dictionary[x]))
    #print(idfDictionary)

def vsm(query):
    documentResults = {}
    tokensCounter = collections.Counter(word_tokenize(query))
    tokenizedQuery = tokenize(query)
    for x in tokenizedQuery: #Term
        if x in dictionary: #Term
            if idfDictionary[x]!= 0.0:
                for y in dictionary[x]: #Document
                    docWeight = idfDictionary[x] * dictionary[x][y] #IDF of terms in document
                    queryWeight = idfDictionary[x] * tokensCounter[x]
                    result = docWeight * queryWeight
                    if(y not in documentResults):
                        documentResults.setdefault(y, 0)
                        documentResults[y] = documentResults[y] + result
                    else:
                        documentResults[y] = documentResults[y] + result
    docRanking=sorted(documentResults.items(), key=itemgetter(1), reverse=True)
    #print(docRanking)
    return docRanking

def getRelevants():
    with open("cranqrel", 'r', encoding='utf-8') as infile:
        for line in infile:
            items = line.split(" ")
            query = items[0]
            relevantDoc =  items[1]
            relevantdictionary.setdefault(query,[]).append(relevantDoc)
        #print(relevantdictionary)
    return relevantdictionary


def performQueries():
    queries = {}
    queries["1"] = "what similarity laws must be obeyed when constructing aeroelastic modelsof heated high speed aircraft ."
    queries["2"] = "what are the structural and aeroelastic problems associated with flight of high speed aircraft ."
    queries["4"] = "what problems of heat conduction in composite slabs have been solved so far ."
    queries["8"] = "can a criterion be developed to show empirically the validity of flow solutions for chemically reacting gas mixtures based on the simplifying assumption of instantaneous local chemical equilibrium ."
    queries["9"] = "what chemical kinetic system is applicable to hypersonic aerodynamic problems ."
    queries["10"] = "what theoretical and experimental guides do we have as to turbulent couette flow behaviour ."
    queries["12"] = "is it possible to relate the available pressure distributions for an ogive forebody at zero angle of attack to the lower surface pressures of an equivalent ogive forebody at angle of attack ."
    queries["13"] = "what methods -dash exact or approximate -dash are presently available for predicting body pressures at angle of attack."
    queries["15"] = "papers on internal /slip flow/ heat transfer studies ."
    queries["18"] = "are real-gas transport properties for air available over a wide range of enthalpies and densities ."
    for i in queries:
        print(i)
        print(vsm(i))
        calculatePrecision(i, vsm(i))


def calculatePrecision(queryNo, vsm):
    precisionAndRecallRanking = {}
    relevantDocuments = getRelevants()
    hundredPercent = len(set(relevantDocuments[queryNo]))
    documentPercentage = 100/hundredPercent
    retrievedAndRelevant = 0
    retrieved = 0
    for i in vsm:
        retrieved = retrieved + 1
        if i[0] in set(relevantDocuments[queryNo]):
            retrievedAndRelevant = retrievedAndRelevant + 1
            #print(retrievedAndRelevant / retrieved)

            if(documentPercentage*retrievedAndRelevant < 10):
                precisionAndRecallRanking[0] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant < 20):
                precisionAndRecallRanking[10] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant < 30):
                precisionAndRecallRanking[20] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant < 40):
                precisionAndRecallRanking[30] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant < 50):
                precisionAndRecallRanking[40] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant < 60):
                precisionAndRecallRanking[50] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant < 70):
                precisionAndRecallRanking[60] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant < 80):
                precisionAndRecallRanking[70] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant < 90):
                precisionAndRecallRanking[80] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant < 100):
                precisionAndRecallRanking[90] = retrievedAndRelevant / retrieved
            elif (documentPercentage * retrievedAndRelevant == 100):
                precisionAndRecallRanking[100] = retrievedAndRelevant / retrieved
            else:
                print("Not in range")
    graph(precisionAndRecallRanking, queryNo)

def graph(precision, queryNo):
    recall = [0,10,20,30,40,50,60,70,80,90,100]
    for i in recall:
        if i not in precision:
            precision[i] = 0
    y = []

    for j in precision:
        y.append(precision[j])
    a= numpy.array(y)
    global b
    b  = b + a
    #print(b)
    pyplot.plot(recall,y,'ro''-')
    pyplot.title(queryNo)
    pyplot.show()


def plotAverage():
    recall = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for i in b:
        i = i/len(b)
    pyplot.plot(recall, b, 'ro''-')
    pyplot.title('Average')
    pyplot.show()

#######################################################
###################### MAIN
#######################################################

'''
dictionary = {}
documents = sys.argv[1:]
for i in documents:
    file = open(i, "r")
    message = file.read()
    createDictionary(tokenize(message), i)
print("YOUR INVERTED INDEX IS READY!")
print()
mainOptions()
'''

#######################################################

openDocs()
calculateIDF()
performQueries()
plotAverage()


