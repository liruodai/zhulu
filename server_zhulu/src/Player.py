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
	def __init__(self, nickname, country, myMap = None):
		self.nickname = nickname
		self.country = country
		# every player use the same map object.
		self.map = myMap
		# the initial action points for the player.
		self.ap = 10
		# the player's lands
		self.lands = []
		# the player's soldiers
		self.soldiers = {'K':[],'W':[]}


		# initial the capital and the only one soldier.
		if 900 == self.country:
			# Yan's capital id_land is 14
			# self.station = Land(14, 3, 900)
			land = myMap.id2land[14]
			land.is_capital = True
			land.owner = 900

			soldier = Soldier(201, 900, 'K', land)
			land.unmanning['K'].append(soldier)

			self.lands.append(land)

			self.soldiers['K'].append(soldier)

			# self.station = myMap.id2land[14]
			# # set the land's owner to the Yan.
			# self.station.owner = 900
			# # initial the only one soldier
			# self.soldier = Soldier(201, 900, 'K', self.station)
		elif 901 == self.country:
			# Qi's capital id_land is 68
			# self.station = Land(68, 3, 901)
			land = myMap.id2land[68]
			land.is_capital = True
			land.owner = 901

			soldier = Soldier(221, 901, 'K', land)
			land.unmanning['K'].append(soldier)

			self.lands.append(land)

			self.soldiers['K'].append(soldier)

			# self.station = myMap.id2land[68]
			# self.station.owner = 901
			# self.soldier = Soldier(221, 901, 'K', self.station)
		elif 902 == self.country:
			# Qin's capital id_land is 29
			# self.station = Land(29, 3, 902)
			land = myMap.id2land[29]
			land.is_capital = True
			land.owner = 902

			soldier = Soldier(241, 902, 'K', land)
			land.unmanning['K'].append(soldier)

			self.lands.append(land)

			self.soldiers['K'].append(soldier)

			# self.station = myMap.id2land[29]
			# self.station.owner = 902
			# self.soldier = Soldier(241, 902, 'K', self.station)
		elif 903 == self.country:
			# Chu's capital id_land is 53
			# self.station = Land(53, 3, 903)
			land = myMap.id2land[53]
			land.is_capital = True
			land.owner = 903

			soldier = Soldier(261, 903, 'K', land)
			land.unmanning['K'].append(soldier)

			self.lands.append(land)

			self.soldiers['K'].append(soldier)

			# self.station = myMap.id2land[53]
			# self.station.owner = 903
			# self.soldier = Soldier(261, 903, 'K', self.station)

	## The method that allows player to move the soldier.
	# @param self The object pointer.
	# @param pos The destination where the soldier should go.Pos is the logic id for the land.
	def move(self, pos):
		# get the land object from the game map
		dst = self.map.id2land[pos]
		# set the land's owner to the player.
		dst.owner = self.country
		# original land's owner will be none.
		self.station.owner = None
		# !! use this to record all the lands which the player has occupied. Will be modified later.
		self.station = dst
		# call the soldier's move method.
		self.soldier.move(dst)


	## The str method of the class. The form of the text information will like that: Player$ nickname:GAO force:900, knights:1, warriors:0
	# @param self The object pointer.
	# @return string to represent the object.
	def __str__(self):
		return 'Player$' + " nickname:" + self.nickname + " force:" + str(self.country) + ", knights:" + str(len(self.soldiers['K'])) +\
		", warriors:" + str(len(self.soldiers['W']))


if __name__ == '__main__':
	# simple test for the player class.
	p = Player('GAO', 900, Map())
	print p




