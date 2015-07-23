#coding=utf-8
'''
@package generate_map
The package is used to generate the id2soldiers data.
'''

import pickle
from Soldier import Soldier


def generate_id2soldier(f):

	id2soldier = {}

	with open(f) as data:
		for line in data:
			soldier_ID, typ, force = line.split('#')
			id2soldier[int(soldier_ID)] = Soldier(int(soldier_ID), int(force), typ)

	
	return id2soldier


if __name__ == '__main__':
	id2soldier = generate_id2soldier('./soldiers_ID.txt')
	# for k, v in id2soldier.items():
	# 	print k, v

	with open('./id2soldier.pkl', 'wb') as f:
		pickle.dump(id2soldier, f)

	# test for the pickle data
	with open('./id2soldier.pkl', 'rb') as f:
		temp = pickle.load(f)
	for k, v in temp.items():
		print k, v