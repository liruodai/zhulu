#!/usr/bin/env python
#coding=utf-8

'''
@package Owner
The package only contains one class, the Owner class.
The owner class is used as the father class for other class which has the attribute owner.
'''

from Base import Base

class Owner(Base):
	'''
	This Owner class has an extra attribute: owner. 
	The owner indicates who has the object.
	'''
	
	## The constructor of the Owner class.
	# @param self The object pointer.
	# @param id The id of the object.
	# @param owner The owner of the object.
	def __init__(self, id, owner):
		# initial the id attribute what is inherited from the father class:Base
		super(Owner, self).__init__(id)
		self.owner = owner
	

	## The str method of the class. The form of the text information will like that: Owner$ ID:123, owner:gaozhefeng
	# @param self The object pointer.
	# @return string to represent the object.
	def __str__(self):
		return 'Owner$' + ' ID:' + str(self.id) + ", owner:" + str(self.owner)


if __name__ == '__main__':
	# simple test for the Owner class.
	tmp = Owner(123, 'gaozhefeng')
	print tmp
