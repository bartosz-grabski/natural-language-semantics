# -*- coding: utf-8 -*-
from pygraphviz import *
import os
import codecs
import re



def get_graphs():

	graphs = {}
	
	for directory in [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]:

		

		primary_node = directory

		graph = _get_new_graph()

		graph.add_node(directory, color="green")

		for csv_filename in os.listdir(directory):
			filename = csv_filename[:-4]
			if filename != directory: 
				graph.add_node(filename, color="red")
			graph.add_edge(directory, filename)
			filepath = os.path.join(os.getcwd(),directory,csv_filename)
			f = codecs.open(filepath, "r", "utf-8")
			for line in f.read().split("\n"):
				line = line.split(",")
				if (len(line) > 1):
					node_name = re.sub(r"[.\\]","",line[1])
					graph.add_node(node_name)
					color = "black"
					if int(line[0]) > 10:
						color = "blue"
					graph.add_edge(filename,node_name, label=line[0], color=color)


		graphs[directory] = graph

	return graphs


def _get_new_graph():
	
	g=AGraph(directed=True)

	# set some default node attributes
	g.node_attr['style']='filled'
	g.node_attr['shape']='circle'
	g.node_attr['fixedsize']='false'
	g.node_attr['nodesep']=2.0
	g.node_attr['overlap']='scale'

	return g
