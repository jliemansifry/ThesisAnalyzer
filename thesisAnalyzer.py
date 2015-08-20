import matplotlib.pyplot as plt
import pylab
import numpy as np
from collections import Counter
import pandas as pd
import string
fileName = "thesis.txt"
f = open(fileName,'r')
def readFile(f): # return an array of all the words as separated by spaces
	return [word for line in open(f,'r') for word in line.split()]

def remove_punc(word): # remove any of'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
	return word.translate(string.maketrans("",""), string.punctuation)

def sentenceAnalyzer(f): # return an array of all the words, 
	with open(f,'r') as file:
		alltext = file.read() 
		wordArr = readFile(fileName)
		for word in wordArr:
			wordArr[wordArr.index(word)] = remove_punc(word).lower()
		return wordArr

allWordsLowerCase = sentenceAnalyzer(fileName)

def splitDocument(pieces,whichPiece): # generate the 50 most common words in the given slice of thesis
	len_slice = int((1./pieces)*len(allWordsLowerCase))
	yield Counter(allWordsLowerCase[len_slice*whichPiece:len_slice*(whichPiece+1)]).most_common(50)

allParts = []
for i in range(10):
	for arr in splitDocument(10,i):
		frame = pd.DataFrame(arr)
		frame['Which Piece'] = i
		allParts.append(frame)
df = pd.concat(allParts,ignore_index=False) # write the data frame
df.columns = ['word','freq','whichpiece'] # label columns

pivoted = df.pivot_table('freq',index='whichpiece',columns='word',aggfunc='sum')
subset = pivoted[['debris','gas','disk','model']] # words of interest
ax = subset.fillna(0).plot(kind='bar')
ax.set_xticklabels(['0-10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-100'])
ax.set_xlabel("Part of Thesis Analyzed (% of way through)")
ax.set_ylabel("Number of Occurances")
pylab.gcf().subplots_adjust(bottom=0.15)
#plt.show()
plt.savefig("Thesis_Word_Frequency_200dpi",dpi=200)
