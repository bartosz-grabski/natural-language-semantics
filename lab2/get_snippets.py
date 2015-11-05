# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import atexit
import re
import codecs
import pickle
import subprocess

class Snippet(object):

	def __init__(self):
		pass


class PLNCScrapper(object):

	PLNC_SEARCH_URL = "http://www.nkjp.pl/poliqarp/" 
	MORFOLOGIK_ARGS = ["java", "-jar", "morfologik-tools-1.9.0-standalone.jar", "plstem", "-ie" ,"UTF-8" ,"-oe" ,"UTF-8"]

	def __init__(self, word, snippets_count):
		self.word = word
		self.snippets_count = snippets_count


	def query_polish_language_national_corpus(self):

		browser = webdriver.Firefox()
		browser.implicitly_wait(10)

		atexit.register(lambda : browser.quit())

		browser.get(self.PLNC_SEARCH_URL)

		select = browser.find_element_by_name("corpus")
		select.click()
		select.find_element_by_xpath("//option[@value='nkjp1800']").click()

		elem = browser.find_element_by_id('id_query') # Find the search box
		elem.send_keys(self.word)
		elem.send_keys(Keys.RETURN)

		snippets = []

		count = 0
		
		while count < self.snippets_count:
			
			snippets_hrefs = map(lambda x: x.get_attribute("href"), browser.find_elements_by_xpath("//a[starts-with(@rel,'m')]"))
			next_page_href = browser.find_element_by_class_name("next_page").find_element_by_tag_name("a").get_attribute("href")
			
			for href in snippets_hrefs:
				
				browser.get(href)

				snippet = browser.find_element_by_id("result-context").text
				snippets.append(snippet)

				count += 1

			
			browser.get(next_page_href)


		self.snippets = snippets;
		return snippets
		
	def save_to_file(self,filename):
		pickle.dump(snippets,open(filename,"wb"))

	def load_from_file(self,filename):
		self.snippets = pickle.load(open(filename,"rb"))

	def parse_snippets(self):

		#output_file = codecs.open("output","w","utf-8")
		tuples = []
		
		for snippet in self.snippets:
			snippet = re.sub(r"[^\w ]+","",snippet, flags=re.UNICODE)
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

	def _find_verb(self,text):
		
		p = subprocess.Popen(self.MORFOLOGIK_ARGS, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		output_data, error_data = p.communicate(text.encode("utf-8"))
		decoded_output = output_data.decode('utf-8').split('\n')
			
		for line in decoded_output:
			try:
				i = line.index("verb")
				j = line.index("\t")
				verb = line[:j]
				return verb
			except:
				pass

		return "unavailable"


def syntax(argv):
	print "usage :", "python " + argv[0], "<WORD> <SNIPPETS>"


if __name__ == "__main__":
	if (len(sys.argv) < 3):
		syntax(sys.argv)
		exit()
	scrapper = PLNCScrapper(sys.argv[1],int(sys.argv[2]))
	#snippets = scrapper.query_polish_language_national_corpus()
	#scrapper.load_from_file("snippets.txt")
	scrapper.load_from_file("snippets.txt")
	tuples = scrapper.parse_snippets()

	output_file = codecs.open("verbs.txt","w","utf-8")

	for t in tuples:
		output_file.write(" ".join(t) + "\n")


	
