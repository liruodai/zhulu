#coding=utf-8
'''
@package generate_map
The package is used to generate the game map data.
Pickle two data structures at last.(adj_matrix and id2land)
'''

import pickle
from Land import Land

def generate_map(f):
	# mark the style of land.for example 0:0, first is represent the city and second
	# is represent the landform
	landform = {}
	# first scan the all lands 
	with open(f) as data:
		for line in data:
			k, v = map(int, line.split(':')[0].split('#'))
			landform[k] = v

	adj_matrix = [[0 for j in xrange(len(landform))]for i in xrange(len(landform))]
	
	id2land = {k:Land(k, v) for k,v in landform.items()}
	# print id2land
	# second scan the adjacency list
	with open(f) as data:
		for line in data:
			temp = line.split(':')
			start = int(temp[0].split('#')[0])
			adj_list = map(int, temp[1].split(','))
			
			for end in adj_list:
				adj_matrix[start][end] = 1

	return adj_matrix, id2land


if __name__ == '__main__':
	adj_matrix, id2land = generate_map('./map.txt')
	
	# check for the adj_matrix as a symmetric matrix     
#     print adj_matrix
#     
#     for i in xrange(len(adj_matrix)):
#         for j in xrange(len(adj_matrix)):
#             if adj_matrix[i][j] != adj_matrix[j][i]:
#                 print i, j, 'False'
#                 break
 
	# use pickle to save python objects
	with open('./map.pkl', 'wb') as f:
		pickle.dump(adj_matrix, f)
	
	with open('./id2land.pkl', 'wb') as f:
		pickle.dump(id2land, f)
	  
	# to obtain data from pickle
	with open('./id2land.pkl', 'rb') as f:
		id2land = pickle.load(f)
	
	# for idx in id2land:
	# 	print idx, id2land[idx]
#          
	
	
	
