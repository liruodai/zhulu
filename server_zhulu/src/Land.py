#!/usr/bin/env python
#coding=utf-8
#
'''
@package Land
The package only contains one class, the Land class.
The Land class is abstract for the land on the map.
'''
from Owner import Owner


class Land(Owner):
	'''
	Each land class will has these attributes:id, type, owner and unmanning.
	id, every object has an unique id.
	type, type of the land. 0 for mountain. 1 for plain with grain 1. 2 for plain with grain 2. 3 for town.
	owner, the force who has the land.
	unmanning, contains the soldier objects who have stand on the land.
	'''
	# id2type map the integer to string. 
	# 0->mountain, 1->plain1, 2->plain2, 3->town
	id2type = {0:'mountain', 1:'plain1', 2:'plain2', 3:'town'}
	
	## The constructor of the Land class.
	# @param self The object pointer.
	# @param id The id of the land.
	# @param owner The owner of the land.
	# @param type The type of the land. 0 for mountain. 1 for plain with grain 1. 2 for plain with grain 2. 3 for town.
	# @param unmaning The soldiers who stand on the land.
	def __init__(self, id, type, owner = None, unmanning=[]):
		super(Land, self).__init__(id, owner)
		self.type = type
		self.unmanning = unmanning
		


	## The str method of the class. The form of the text information will like that: Land$ ID:1, owner:gao, type:plain1, soldiers:0
	# @param self The object pointer.
	# @return string to represent the object.
	def __str__(self):

		info = 'Land$' + ' ID:' + str(self.id) + ", owner:" + str(self.owner) + ', type:' + self.id2type[self.type] + ', soldiers:' + str(len(self.unmanning))
		
		return info
	

if __name__ == '__main__':
	# simple test for the Land class.
	l = Land(1 , 1, 'gao')
	print l
