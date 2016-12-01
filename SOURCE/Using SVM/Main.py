import numpy as np
from sklearn import svm
import re
import codecs
import copy


words = {}
wordUse = {}
lines = []
Vectors = [[]]
Sentiments = []
write = "No"
wordUseFlag = 0
min = 0
max = 0


# Populates The Dictionary From The Provided File
def save_words(file):
	print("Building Dictionary, This Might Take Awhile...")
	with codecs.open(file, "rb",encoding='utf-8', errors='ignore') as f:
		word = 0
		for line in f:
			wrds = re.split(",|\s",line.replace('\\n','').replace('\n',''))
			Sentiments.append(int(wrds.pop(0)))
			lines.append(wrds)
			for wrd in wrds:
				try:
					if wrd not in words.keys() and wrd is not "":
						words[wrd] = word
						wordUse[wrd] = 0
						word += 1
				except:
					""
		print("Done! Initial Length: "+str(words.__len__()))
	if write == "Yes":
		print("Writing File: Words.csv...")
		file = open('results/Words.csv','w',encoding='utf-8', errors='ignore')
		for ww in words.keys():
			file.write(ww+"\n")
		print("Writing File: Sentiments.csv...")
		file = open('results/Sentiments.csv','w',encoding='utf-8', errors='ignore')
		for s in Sentiments:
			file.write(str(s))
			file.write("\n")
		
		
# Returns The Index Of The Passed In Word, Otherwise Returns -1 If Not Found
def find_word_index(str):
	if str in words.keys():
		if wordUseFlag == 0:
			wordUse[str] += 1
		return words[str]
	else:
		return -1


# Builds The Vectors 		
def save_vectors():
	print("Building Vectors, This Might Take Awhile...")
	print("Trimming Words Dictionary...")
	# Populate Word Use Array
	for line in lines:
		for wd in line:
			find_word_index(wd)
	for wu in wordUse:
		if wordUse[wu] < 10:
			del words[wu]
	cnt = 0
	for wrd in words.keys():
		words[wrd] = cnt
		cnt += 1
	print("Done! New Words Length: "+str(words.__len__()))
	wordUseFlag = 1
	for line in lines:
		vec = [0]*words.__len__()
		for wd in line:
			if wd in words.keys():
				vec[find_word_index(wd)] += 1
		Vectors.append(vec)
	Vectors.pop(0)
	print("Done! Length: "+str(Vectors.__len__()))
	if write == "Yes":
		print("Writing File: Vectors.csv...")
		file = open('results/Vectors.csv','w',encoding='utf-8', errors='ignore')
		for v in Vectors:
			for vv in v:
				file.write(str(vv)+",")
			file.write("\n")


# Writes The Words And How Many Times Each Word Was Used To A CSV File
def save_Word_Use():
	if write == "Yes":
		file = open('results/WordUse.csv','w',encoding='utf-8', errors='ignore')
		for wu in wordUse:
			file.write(wu+","+str(wordUse[wu])+"\n")
			

# Converts A String Into A Vector - Please Use Spaces Between The Words In Your Sentence
def convert_to_vector(str):
	s = str.split(" ")
	ss = [0]*words.__len__()
	for w in s:
		ss[find_word_index(w)] += 1
	return ss

	
# Predict How Many Votes, Up Or Down, A Comment May Receive
def predict(str):
	print("\nComment: '"+str+"'")
	res = model.predict([convert_to_vector(str)])
	print(res)
	#print("I Think The Comment Will Get "+model.predict([convert_to_vector(str)])[0]+" Votes")


# Grab Input From The Console
def accept_input():
	var = ""
	while var != "Exit":
		var = input("\nEnter A Comment For The Classifier To Score ( Exit To Quit )\n")
		if var != "Exit":
			res = predict(var)
			


# Delete Objects From Dictionary			
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r
			

# Program Entry Point			
print("Getting Stuff Ready...")	
save_words("memes/Democrat.csv")
save_vectors()
save_Word_Use()
min = Sentiments[0]
max = Sentiments[Sentiments.__len__()-1]
print("Fitting Data...")
model = svm.SVR(kernel='linear')
model.fit(Vectors, Sentiments)
accept_input()