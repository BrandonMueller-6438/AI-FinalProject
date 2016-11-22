import numpy as np
from sklearn.naive_bayes import GaussianNB
import re
import codecs


words = {}
lines = []
Vectors = [[]]
Sentiments = []
file = "Democrat.csv"

# Populates The Dictionary From The Provided File
def save_words():
	print("Building Dictionary, This Might Take Awhile...")
	with codecs.open(file, "rb",encoding='utf-8', errors='ignore') as f:
		word = 0
		for line in f:
			wrds = re.split(",|\s",line.replace('\\n','').replace('\n',''))
			Sentiments.append(wrds.pop(0))
			lines.append(wrds)
			for wrd in wrds:
				try:
					if wrd not in words.keys():
						words[wrd] = word
						word += 1
				except:
					""
		print("Done! Length: "+str(words.__len__()))
	print("Writing File: Words.csv...")
	file = open('Words.csv','w',encoding='utf-8', errors='ignore')
	for ww in words.keys():
		file.write(ww+"\n")
	print("Writing File: Sentiments.csv...")
	file = open('Sentiments.csv','w',encoding='utf-8', errors='ignore')
	for s in Sentiments:
		file.write(s)
		file.write("\n")
		
		
# Returns The Index Of The Passed In Word, Otherwise Returns -1 If Not Found
def find_word_index(str):
	if str in words.keys():
		return words[str]
	else:
		return -1


# Builds The Vectors 		
def save_vectors():
	print("Building Vectors, This Might Take Awhile...")
	for line in lines:
		vec = [0]*words.__len__()
		for wd in line:
			vec[find_word_index(wd)] += 1
		Vectors.append(vec)
	Vectors.pop(0)
	print("Done! Length: "+str(Vectors.__len__()))
	print("Writing File: Vectors.csv...")
	file = open('Vectors.csv','w',encoding='utf-8', errors='ignore')
	for v in Vectors:
		for vv in v:
			file.write(str(vv)+",")
		file.write("\n")
		

# Converts A String Into A Vector - Please Use Spaces Between The Words In Your Sentence
def convert_to_vector(str):
	s = str.split(" ")
	ss = [0]*words.__len__()
	for w in s:
		ss[find_word_index(w)] += 1
	return ss

	
# Predict How Many Votes, Up Or Down, A Comment May Receive
def predict(str):
	print("Comment: '"+str+"'")
	print("I Think The Comment Will Get "+clf.predict([convert_to_vector(str)])[0]+" Votes")

	
def accept_input():
	var = ""
	while var != "Exit":
		var = input("\nEnter A Comment For The Classifier To Score ( Exit To Quit )\n")
		if var != "Exit":
			predict(var)


print("Getting Stuff Ready...")	
save_words()
save_vectors()
print("Fitting Data...")
clf = GaussianNB()
clf.fit(Vectors, Sentiments)
accept_input()