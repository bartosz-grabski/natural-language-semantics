# -*- coding: utf-8 -*-
import sys
import re
import codecs
import itertools
import graphs as g

# Parses snippets and tokenizes them 
class SnippetParser(object):

	def __init__(self, snippets_file = "verbs.txt"):
		self.snippets_file = snippets_file
		self.parsed_snippets = []
		self.combinations = []
		self.unmatched_edges = []
		self.matched_edges = []


	def parse_snippets(self):
		input_file = codecs.open(self.snippets_file, "r", "utf-8")
		snippets = input_file.read().split("\n")
		parsed_snippets = []
		for snippet in snippets:
			snippet = re.sub(r"[^\w ]+","",snippet, flags=re.UNICODE)
			snippet = snippet.lower()
			snippet = snippet.split()
			parsed_snippets.append(snippet)

		self.parsed_snippets = parsed_snippets
		return parsed_snippets

	def compare_to_graph(self, graph_node_name):
		g = self.get_graph(graph_node_name)

		if g is None:
			return

		matched_edges = []
		unmatched_edges = []

		snippet_perms= self._generate_all_snippet_permutations()

		for snippet_perm in snippet_perms:
			for pair in snippet_perm:
				if g.has_edge(pair[0],pair[1]):
					e = g.get_edge(pair[0],pair[1])
					edge_to_add = (e,int(e.attr['label']))
					if not edge_to_add in matched_edges:
						matched_edges.append(edge_to_add)
				else:
					unmatched_edges.append((pair[0],pair[1]))

		matched_edges = self._sort_by(matched_edges)


		self.matched_edges = matched_edges
		self.unmatched_edges = unmatched_edges

		return matched_edges, unmatched_edges


	def _sort_by(self, collection):
		return sorted(collection,key = lambda x : x[1], reverse=True)


	def get_graph(self, name):
		graphs = g.get_graphs()
		return graphs[name] if name in graphs else None

	def _generate_all_snippet_permutations(self):

		pairs = []

		for snippet in self.parsed_snippets:
			pairs.append(itertools.permutations(snippet,2))

		return pairs

	def print_to_output_files(self):

		output_file_matched = codecs.open("matched.out", "w", "utf-8")
		output_file_unmatched = codecs.open("unmatched.out", "w", "utf-8")

		for matched in self.matched_edges:
			output_line = matched[0][0] + u' ' + matched[0][1] + u' ' + str(matched[1]) + '\n'
			output_file_matched.write(output_line)

		output_file_matched.close()

		for unmatched in self.unmatched_edges:
			output_line = unmatched[0] + u' ' + unmatched[1] + '\n'
			output_file_unmatched.write(output_line)

		output_file_unmatched.close()



if __name__ == "__main__":
	parser = SnippetParser()
	parser.parse_snippets()
	parser.compare_to_graph("morze")
	parser.print_to_output_files()

	#print u
	#parser.compare_to_graph("morze")



	
 