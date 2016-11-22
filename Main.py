import numpy as np
import re
import string
import codecs

words = {}

# Populates The Dictionary From The Provided File
def save_words():
	print("Building Dictionary, This Might Take Awhile...");
	with codecs.open('Trump.csv', "rb",encoding='utf-8', errors='ignore') as f:
		word = 0
		for line in f:
			wrds = line.replace('\\n','').replace('\n','').split(" ")
			for wrd in wrds:
				try:
					if wrd not in words.keys():
						words[wrd] = word
						word += 1
				except:
					""
		print("Done! Length: "+str(words.__len__()))
	file = open('Words.csv','w',encoding='utf-8', errors='ignore')
	for ww in words.keys():
		file.write(ww+"\n")


# Returns The Index That The Passed In Word Is Located, Otherwise Returns -1 If Not Found
def find_word_index(str):
	if str in words.keys():
		return words[str]
	else:
		return -1
	

save_words()
