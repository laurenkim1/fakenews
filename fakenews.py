import numpy as np 
import pandas as pd 
import re
from random import randint

maxSeqLength = 250
batchSize = 24
lstmUnits = 64
numClasses = 2
iterations = 100000
numStories = 63000


fake_df = pd.read_csv('fake.csv')
print fake_df.columns
fake_text = fake_df['text']

real_df = pd.read_json('signalmedia-1m.jsonl',lines=True)
print real_df.columns
real_text = real_df['content']

# choose 50,000 random stories from the real dataset
real_i = np.random.choice(len(real_text), size=50000, replace=False)
real_text = real_text[real_i]

def loadGloveModel():
    print "Loading Glove Model"
    f = open('glove.42B.300d.txt','r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print "Done.",len(model)," words loaded!"
    return model

strip_special_chars = re.compile("[^A-Za-z0-9 ]+")

def cleanSentences(string):
    string = string.lower().replace("<br />", " ")
    return re.sub(strip_special_chars, "", string.lower())

# glove word-vec dictionary
glove = loadGloveModel()

# stories x the first 200 words
train_matrix = np.zeros((numStories, maxSeqLength))

story_index = 0

for story in real_text:
	words = np.zeros((maxSeqLength+1))
	indexCounter = 0
	cleanedLine = cleanSentences(story)
	split = cleanedLine.split()
	if len(split)< maxSeqLength:
		indexCounter = maxSeqLength-len(split)
	else:
		split = split[:maxSeqLength]
	for word in split:
		words[indexCounter] = word
		indexCounter = indexCounter + 1
	words[maxSeqLength]="REAL"
	train_matrix[story_index] = words
	story_index+=1

for story in fake_text:
	words = np.zeros((maxSeqLength+1))
	indexCounter = 0
	cleanedLine = cleanSentences(story)
	split = cleanedLine.split()
	if len(split)< maxSeqLength:
		indexCounter = maxSeqLength-len(split)
	else:
		split = split[:maxSeqLength]
	for word in split:
		words[indexCounter] = word
		indexCounter = indexCounter + 1
	words[maxSeqLength]="Fake"
	train_matrix[story_index] = words
	story_index+=1

np.save('train_matrix', train_matrix)



def getTrainBatch():
    labels = []
    arr = np.zeros([batchSize, maxSeqLength])
    for i in range(batchSize):
        if (i % 2 == 0): 
            num = randint(1,11499)
            labels.append([1,0])
        else:
            num = randint(13499,24999)
            labels.append([0,1])
        arr[i] = ids[num-1:num]
    return arr, labels

def getTestBatch():
    labels = []
    arr = np.zeros([batchSize, maxSeqLength])
    for i in range(batchSize):
        num = randint(11499,13499)
        if (num <= 12499):
            labels.append([1,0])
        else:
            labels.append([0,1])
        arr[i] = ids[num-1:num]
    return arr, labels



