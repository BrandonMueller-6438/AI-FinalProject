import numpy as np
from sklearn.naive_bayes import GaussianNB
import re
import codecs


words = {}
wordUse = {}
lines = []
Vectors = [[]]
Sentiments = []
write = "No"
wordUseFlag = 0


# Populates The Dictionary From The Provided File
def save_words(file):
	print("Building Dictionary, This Might Take Awhile...")
	
	# Uses the codes library to open the file
	with codecs.open(file, "rb",encoding='utf-8', errors='ignore') as f:
		word = 0
		
		# Runs through each line in the file
		# And processes the information
		for line in f:
			
			# Removes unwanted characters and spaces
			wrds = re.split(",|\s",line.replace('\\n','').replace('\n',''))
			
			# The wrds array contains all the resulting
			# tokens from the re.split function above.
			# The first token in the wrds array is always
			# a number - this is one of our sentiments.
			# It is popped off the wrds array and added to
			# the Sentiments array and will be part of the
			# data fitting after preprocessing is finished.
			Sentiments.append(int(wrds.pop(0)))
			lines.append(wrds)
			for wrd in wrds:
				try:
					
					# We store non-duplicate words into the words
					# and wordCount dictionaries here.
					if wrd not in words.keys() and wrd is not "":
						words[wrd] = word
						wordUse[wrd] = 0
						word += 1
				except:
					""
		print("Done! Initial Length: "+str(words.__len__()))
	if write == "Yes":
		
		# We write the Dictionary words out to
		# a file when the "write" field above is
		# set to "yes".
		print("Writing File: Words.csv...")
		file = open('results/Words.csv','w',encoding='utf-8', errors='ignore')
		for ww in words.keys():
			file.write(ww+"\n")
			
		# We write the Sentiments out to
		# a file when the "write" field above is
		# set to "yes".
		print("Writing File: Sentiments.csv...")
		file = open('results/Sentiments.csv','w',encoding='utf-8', errors='ignore')
		for s in Sentiments:
			file.write(str(s))
			file.write("\n")
		
		
# Returns The Index Of The Passed In Word, Otherwise Returns -1 If Not Found
def find_word_index(str):
	
	# We return the index of the word contained
	# within "str". If the word is not in the Dictionary
	# we just return -1 and handle that so it doesn't
	# crash the program.
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
	
	# Remove the words from our Dictionary
	# that appear in our dataset less than X times.
	# We can conclude that those words are the horrible
	# mis-spellings and other typographical errors that
	# are found on a Reddit forum.
	for wu in wordUse:
		if wordUse[wu] < 10:
			del words[wu]
	cnt = 0
	
	# Once we delete the unwanted words
	# from our Dictionary, the words that are
	# left must be re-indexed. Resolves index-errors
	# bug that was previously a problem.
	for wrd in words.keys():
		words[wrd] = cnt
		cnt += 1
	print("Done! New Words Length: "+str(words.__len__()))
	
	# Sets The wordUseFlag so the next time
	# the find_word_index function is referenced, it
	# will not double count the words again in the
	# wordUse Dictionary, see the "find_word_index" function
	# above.
	wordUseFlag = 1
	
	# Generates the information within the Vectors
	# 2D Array.
	for line in lines:
		vec = [0]*words.__len__()
		for wd in line:
			if wd in words.keys():
				vec[find_word_index(wd)] += 1
		Vectors.append(vec)
	
	# We pop this first index of the Vectors 2D Array
	# Because the First index is empty.
	Vectors.pop(0)
	print("Done! Length: "+str(Vectors.__len__()))
	
	# We write the Vectors information out
	# to Vectors.csv, if the "write" field below
	# is set to "yes".
	if write == "Yes":
		print("Writing File: Vectors.csv...")
		file = open('results/Vectors.csv','w',encoding='utf-8', errors='ignore')
		for v in Vectors:
			for vv in v:
				file.write(str(vv)+",")
			file.write("\n")


# Writes The Words And How Many Times Each Word Was Used To A CSV File
def save_Word_Use():
	
	# We write the WordUse information
	# to WordUse.csv if the "write" field below
	# is set to "yes".
	if write == "Yes":
		file = open('results/WordUse.csv','w',encoding='utf-8', errors='ignore')
		for wu in wordUse:
			file.write(wu+","+str(wordUse[wu])+"\n")
			

# Converts A String Into A Vector.
# Please Use Spaces Between The Words In Your Sentence / Comment.
def convert_to_vector(str):
	s = str.split(" ")
	ss = [0]*words.__len__()
	for w in s:
		ss[find_word_index(w)] += 1
	return ss

	
# Predict whether a comment will receive
# a low number of votes: 0, a moderate number of votes: 1,
# or a large number of vote: 2.
def predict(str):
	print("\nComment: '"+str+"'")
	res = clf.predict([convert_to_vector(str)])
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
save_words("memes/Naive/Clinton.csv")
save_vectors()
save_Word_Use()
print("Fitting Data...")
clf = GaussianNB()
clf.fit(Vectors, Sentiments)
accept_input()