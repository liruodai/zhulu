#!/usr/bin/env python
#coding=utf-8

'''
@package Soldier
The package only contains one class, the Soldier class.
The Soldier class is abstract for the knight and warrior.
'''

from Owner import Owner


class Soldier(Owner):
	'''
	Each Soldier class has these attributes:id, onwer, type, and station.
	'''
	## The constructor of the Soldier class.
	# @param self The object pointer.
	# @param id The id of the soldier.
	# @param owner The force which soldier belongs to.
	# @param type The type of the Soldier. Knight or warrior. The 'K' for knight and 'W' for warrior.
	# @param station The place where the soldier stands on.
	def __init__(self, id, owner, type, station = None):
		# initail the attributes what are inherited from the father class:Owner
		super(Soldier, self).__init__(id, owner)
		self.type = type
		self.station = station
		# The state of the Soldier.
		# 1 stand for fighting. 0 stand for not fighting. -1 stand for dead.
		self.state = 1 

	## The method for the soldier moves.
	# @param self The object pointer.
	# @param dst The ID of the destination land. 
	def move(self, dst):
		self.station = dst


	## The str method of the class. The form of the text information will like that: Soldier$ ID:100, owner:gaozhefeng, type:K
	# @param self The object pointer.
	# @return string to represent the object.
	def __str__(self):
		return 'Soldier$' + ' ID:' + str(self.id) + ", owner:" + str(self.owner) + ', type:' + str(self.type)
	

if __name__ == '__main__':
	# simple test for the Soldier class.
	s = Soldier(100, 'gaozhefeng', 'K')
	print s
