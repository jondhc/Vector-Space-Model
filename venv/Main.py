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
#import untangle
dictionary = {}

def indexDocumentFrequency(totalNumberOfDocuments, documentsWithTermAppearance):
    return math.log((totalNumberOfDocuments/documentsWithTermAppearance))

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
    print(dictionary)

def parseDoc(document):
    doc = minidom.parse("./cranfield.all/" + document)
    textElement = doc.getElementsByTagName('TEXT')[0]
    textContent = textElement.firstChild.data
    #print(getDocNo(document))
    return textContent

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
    #print(tokensCounter)

    for element in tokensCounter:
        dictionary.setdefault(element, {})[docNo] = tokensCounter[element]

    #print(dictionary)


    '''for i in tokens:
        dictionary.setdefault(i, {})
    '''


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
#print(similarityCoefficient([0, 0, 0, 0, 0, .176, 0, 0, .477, 0, .176], [0, 0, .477, 0, .477, .176, 0, 0, 0, .176, 0])) #expectedresult = 0.031

