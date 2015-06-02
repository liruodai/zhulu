#!/usr/bin/env python
#coding=utf-8

'''
@package Base
The package only contains one class, the Base class.
All the other classes in the project are inherited from the Base class. 
'''

class Base(object):
	'''
	The Base class is the father class for all other classes.
	The Base class just has an attribute: id. All the different
	classes have different ids.
	'''

	## The constructor of the Base class.
	# @param self The object pointer.
	# @param id The id of the object.
	def __init__(self, id):
		self.id = id
	
	## The str method of the class. The form of the text information will like that: Base$ ID:123
	# @param self The object pointer.
	# @return string to represent the object.
	def __str__(self):
		return 'Base$' + ' ID:'+str(self.id)



if __name__ == '__main__':
	# simple test for the Base class.
	base = Base(123)
	print base
