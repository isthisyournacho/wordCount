import glob
import re
import string
import json
import sys
import getopt
import time
import os

start_time = time.time()

data = {}
words = []
numWords = 0
numSentence = 0

#Configurations
directory = os.getcwd() + "/"
top = 100
ofile = ""
searchpattern = "*.tsv"
wordchosen = ""

myopts, args = getopt.getopt(sys.argv[1:],"d:o:n:w:")

for o, a in myopts:
    if o == '-d':
        directory = a
    elif o == '-o':
        ofile = a
    elif o == '-n':
        top = int(a)
    elif o == '-w':
        wordchosen = a

#If script is run with no arguments, display help
if myopts == []:
    print("")
    print("Usage: python hastags.py -d DIRECTORY -o OUTPUTFILE -n NUMBEROFWORDS -w SPECIFICWORD")
    print("")
    print("DIRECTORY = Directory to scan for .txt files (Default: Current Working Directory)")
    print("OUTPUTFILE = Location to output json data (Default: To Terminal")
    print("NUMBEROFWORDS = Top # of words to display (Default: " + str(top))
    print("SPECIFICWORD = Word you wish specifically (When enabled, only this word is output)")
    print("")
    exit()

print("Scanning directory " + directory + " with search pattern: " + searchpattern)

#This loops through files, then sentences, then words to do the count
for filename in glob.glob(directory + searchpattern):
    with open(filename) as f:
        text = f.read()
        #print(filename + ": " + text)

    # Splits text into individual sentences
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

    # print sentences
    for sentence in sentences:
        if sentence == "": #handles blank lines
            continue
        numSentence += 1
        sentence = sentence.replace("\r\n","").replace("\n","")
        pattern = re.compile("\w+\t.*")
        if pattern.match(sentence):
            intentKey = re.sub(r'(\w+)\t.*', r'\1', sentence)
            print(intentKey)
        #print("Sentence " + str(d) + " is: " + sentence)
        for word in sentence.lower().split():
            table = str.maketrans(dict.fromkeys(string.punctuation))
            word = word.translate(table)
            if word == "":
                continue
            numWords += 1
            #print("Word " + str(i) + " is: " + word)
            if word in data:
                #print(word + " already exists")
                data[word]["occurrences"] = data[word]["occurrences"] + 1
                #if sentence not in data[word]["examplelist"]:
                    #data[word]["examplelist"].append(sentence)
                #if filename not in data[word]["doclist"]:
                    #data[word]["doclist"].append(filename)
            else:
                # Add word = word, occurrences = int (1), doc = doclist (filename), example = exampleList (sentence)
                if data:
                    # If data exists but word is new, add a new entry
                    data[word] = {"occurrences": 1, "doclist": [filename], "examplelist": [sentence]}
                else:
                    # If data does not exist, create it
                    data = {word: {"occurrences": 1, "doclist": [filename], "examplelist": [sentence]}}
                if words:
                    words = words + "," + word
                else:
                    words = word

#print data
print(str(numWords) + " words scanned revealed " + str(data.__len__()) + " unique in " + str(numSentence) + " sentences in %s seconds." % (time.time() - start_time))

if numWords == 0:
    exit()

jsonString = json.dumps(data)
jsonObject = json.loads(jsonString)

#sort the keys (words) buy the # of occurrences descending
isort = sorted(jsonObject, key=lambda x: (jsonObject[x]['occurrences']), reverse=True)

j = 0

if wordchosen == "": #If word was not chosen, just provide top words
    if top == 1:
        thisObj = '{"' + isort[j] + '": ' + json.dumps(jsonObject[isort[j]]) + '}'
    else:
        while j < top:
            if j == 0:
                thisObj = "["
            thisObj =  thisObj + '{"' + isort[j] + '": ' + json.dumps(jsonObject[isort[j]]) + '},'
            #print(thisObj)
            j += 1
        print("")
        thisObj = thisObj[:-1] + "]" #remove last comma and add ]
else: #If word was chosen, display that word only
    if wordchosen in jsonObject:
        thisObj = '{"' + wordchosen + '": ' + json.dumps(jsonObject[wordchosen]) + '}'
    else:
        print("ERROR: " + wordchosen + " does not exist!!")
        exit()

#If output file configured, write there, otherwise write to terminal.
if ofile == "":
    print(thisObj)
else:
    f = open(ofile,"w")
    f.write(thisObj)
    print("Wrote output to " + ofile)
