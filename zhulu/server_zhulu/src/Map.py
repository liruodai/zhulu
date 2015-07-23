#!/usr/bin/env python
#coding=utf-8

'''
@package Map
The package only contains one class, the Map class.
The Map class is abstract for the game map.
This class loads data from the files.
'''
import pickle
from Land import Land

class Map:
	'''
	The map class is abstract for the game map.
	It has two data structures. One(adj_matrix) is used represent the logic connections between lands.
	Another(id2land) is used to get the land object from the land's id.
	'''
	## The constructor of the Land class. Load date from the file. 
	# @param self The object pointer.
	def __init__(self):
		# load the adjacency matrix.
		with open('../data/map.pkl', 'rb') as f:
			self.adj_matrix = pickle.load(f)
		# load the dictionary data. key:id -> value:land object.
		with open('../data/id2land.pkl', 'rb') as f:
			self.id2land = pickle.load(f)

	## The function is used to get the neighbour of land
	def get_neighbour_id(self, land_id):
		neighbour_id = []

		for v, link in enumerate(self.adj_matrix[land_id]):
			if link:
				neighbour_id.append(v)
		return neighbour_id


if __name__ == '__main__':
	# simple test for the Map class.
	myMap = Map()
	print myMap.adj_matrix[20]
	print myMap.get_neighbour_id(20)
	for k,v in myMap.id2land.items():
		print v
