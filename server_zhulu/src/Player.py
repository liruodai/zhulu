#!/usr/bin/env python
#coding=utf-8

'''
@package Player
The package only contains one class, the Player class.
The Player class is abstract for the players.
'''

from Base import Base
from Soldier import Soldier
from Land import Land
from Map import Map


class Player(Base):
	'''
	The Player class has these attributes:nickname, country, ap, station, soldier, and the map.
	nickname is the name when player register in the game.
	country is the force of the player. 900 for yan. 901 for qi. 902 for qin. 903 for chu.
	ap is the points that the player can use to take actions.
	station record the player's domain lands.
	soldier record all the soldiers that the player has.
	map the game map for all players.

	'''

	# the max number of knights
	TOTAL_KNIGHT = 4
	# the max number of warriors
	TOTAL_WARRIOR = 8

	## The constructor of the Player class.
	# @param self The object pointer.
	# @param nickname The name of the player.
	# @param country The force of the player. 900 for yan. 901 for qi. 902 for qin. 903 for chu
	# @param myMap The game map for all the players.
	def __init__(self, nickname, country, myMap = None, id2soldier = None):
		self.nickname = nickname
		self.country = country
		# every player use the same map object.
		self.map = myMap
		# every player use the same id2soldier get the soldier object from the id.
		self.id2soldier = id2soldier
		# the initial action points for the player.
		self.ap = 10
		# the player's lands
		self.lands = []
		# the player's soldiers
		self.soldiers = {'K':[],'W':[]}


		# initial the capital and the only one soldier.
		self.init_capital_soldier(country)

	## The method that initial the capital and the soldiers. One knight and three warriors
	# @param self The object pointer.
	# @param force The force of the player.
	def init_capital_soldier(self, force):
		
		info = {900:{'CAPITAL':14, 'SOLDIER':[201,205,206,207]}, 901:{'CAPITAL':68, 'SOLDIER':[221,225,226,227]},\
				902:{'CAPITAL':29, 'SOLDIER':[241,245,246,247]}, 903:{'CAPITAL':53, 'SOLDIER':[261,265,266,267]}}

		# initial the capital information
		capital = info[force]['CAPITAL']

		land = self.map.id2land[capital]
		land.is_capital = True
		land.owner = force

		self.lands.append(capital)

		# initial the soldiers
		for i in info[force]['SOLDIER']:
			soldier = self.id2soldier[i]
			soldier.station = capital
		
			land.unmanning[soldier.type].append(i)
			self.soldiers[soldier.type].append(i)

	## The method that allows player to move the soldier.
	# @param self The object pointer.
	# @param pos The destination where the soldier should go.Pos is the logic id for the land.
	def move(self, pos):
		# get the land object from the game map
		dst = self.map.id2land[pos]
		# set the land's owner to the player.
		dst.owner = self.country
		# original land's owner will be none.
		#self.station.owner = None
		# !! use this to record all the lands which the player has occupied. Will be modified later.
		#self.station = dst
		# call the soldier's move method.
		self.soldier.move(pos)


	## The str method of the class. The form of the text information will like that: Player$ nickname:GAO force:900, knights:1, warriors:0
	# @param self The object pointer.
	# @return string to represent the object.
	def __str__(self):
		return 'Player$' + " nickname:" + self.nickname + " force:" + str(self.country) + ", knights:" + str(len(self.soldiers['K'])) +\
		", warriors:" + str(len(self.soldiers['W']))


if __name__ == '__main__':
	# simple test for the player class.
	import pickle

	with open('../data/id2soldier.pkl', 'rb') as f:
		id2soldier = pickle.load(f)
	p = Player('GAO', 900, Map(), id2soldier)
	print p
	for k in p.lands:
		print k

	for k in p.soldiers['K']:
		print k


	for k in p.soldiers['W']:
		print k




