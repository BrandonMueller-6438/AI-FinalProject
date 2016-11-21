import numpy as np
import re

words = {}


# Populates The Dictionary From The Provided File
def save_words():
	f  = open('Trump.csv', 'r')
	ln = 0
	for line in f:
		try:
			print(line)
		except UnicodeDecodeError:
			pass
	print("Done! Length: "+str(words.__len__()))
	return words


save_words()

