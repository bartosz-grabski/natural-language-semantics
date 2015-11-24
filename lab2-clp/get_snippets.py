# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from lib.clp import clp
import sys
import re
import codecs
import pickle
import subprocess

class Parser(object):

	def __init__(self, word, snippets_count):
		self.word = word
		self.snippets_count = snippets_count

		
	def save_to_file(self,filename):
		pickle.dump(snippets,open(filename,"wb"))

	def load_from_file(self,filename):
		self.snippets = pickle.load(open(filename,"rb"))

	def parse_snippets(self):

		#output_file = codecs.open("output","w","utf-8")
		tuples = []
		
		for snippet in self.snippets:
			snippet = re.sub(r"[^\w ]+","",snippet)
			snippet = snippet.split()

			element_index = snippet.index(self.word)
			left_hand_side = snippet[:element_index]
			right_hand_side = snippet[element_index+1:]
			
			left_hand_side = reversed(left_hand_side)
			right_hand_side = reversed(right_hand_side)

			text_to_search = u' '.join(left_hand_side)

			left_verb = self._find_verb(text_to_search)

			text_to_search = u' '.join(right_hand_side)

			right_verb = self._find_verb(text_to_search)

			tuples.append((left_verb,self.word,right_verb))

		return tuples;

	def _find_verb(self,text_list):


		for element in text_list:
			i = clp.rec(element)
			if clp.label(i[0]) == clp.PLP.CZESCI_MOWY.CZASOWNIK:
				forms = clp.forms(i[0])
				if len(forms) > 0 and forms[0] == element:
					return element

		return "unavailable"


def syntax(argv):
	print "usage :", "python " + argv[0], "<WORD> <SNIPPETS>"


if __name__ == "__main__":
	if (len(sys.argv) < 3):
		syntax(sys.argv)
		exit()

	parser = Parser(sys.argv[1],int(sys.argv[2]))
	parser.load_from_file("snippets.txt")
	tuples = parser.parse_snippets()

	output_file = codecs.open("verbs.txt","w","utf-8")

	for t in tuples:
		output_file.write(" ".join(t) + "\n")


	
