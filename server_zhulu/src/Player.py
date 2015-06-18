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
	The Player class has these attributes:nickname, force, ap, station, soldier, and the map.
	nickname is the name when player register in the game.
	force is the force of the player. 900 for yan. 901 for qi. 902 for qin. 903 for chu.
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
	# @param force The force of the player. 900 for yan. 901 for qi. 902 for qin. 903 for chu
	# @param myMap The game map for all the players.
	def __init__(self, nickname, force, myMap = None, id2soldier = None):
		self.nickname = nickname
		self.force = force
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
		self.init_capital_soldier(force)

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
		print land

		self.lands.append(capital)

		# initial the soldiers
		for i in info[force]['SOLDIER']:
			soldier = self.id2soldier[i]
			soldier.station = capital
		
			land.unmanning[soldier.type].append(i)
			self.soldiers[soldier.type].append(i)

	## The method that allows player to move the soldier.
	# @param self: The object pointer.
	# @param force: The force number.
	# @param dst_id: The destination's id.
	# @param s_id: The marching soldiers' ids; type can be str or list, for the case that one or more soldiers march
	def move(self, force, dst_id, s_id):
		# get the land object from the game map
		dst = self.map.id2land[dst_id]

		# Step 1: 得到出发地点ori
		ori_id = self.id2soldier[s_id[0]].station
		ori = self.map.id2land[ori_id] 
		# Step 2: 修改soldier.station
		for item in s_id:
			soldier = self.id2soldier[item] 
			soldier.station = dst_id
		# Step 3: 修改land.unmanning
			ori.unmanning[soldier.type].remove(item) 	# 修改出发地点信息
			dst.unmanning[soldier.type].append(item) 	# 修改目标地点信息
		# Step 4: 修改lands和land.owner
		if dst_id not in self.lands:
			self.lands.append(dst_id) 		# 修改目标地点信息
		dst.owner = force
		if ori.is_barn == False and ori.type != 3 and ori.unmanning['K'] == [] and ori.unmanning['W'] == []:
			self.lands.remove(ori_id) 	# 修改出发地点信息
			ori.owner = None

		print 'move action--', force
		print 'ori: ', ori_id
		print 'dst: ', dst_id 
		print 'soldiers: ',  s_id
		print 'lands: ', self.lands
		print 'ori.owner and unmanning: ', ori.owner, ori.unmanning 
		print 'dst.owner and unmanning: ', dst.owner, dst.unmanning


	## The str method of the class. The form of the text information will like that: Player$ nickname:GAO force:900, knights:1, warriors:0
	# @param self The object pointer.
	# @return string to represent the object.
	def __str__(self):
		return 'Player$' + " nickname:" + self.nickname + " force:" + str(self.force) + ", knights:" + str(len(self.soldiers['K'])) +\
		", warriors:" + str(len(self.soldiers['W']))


if __name__ == '__main__':
	# simple test for the player class.
	import pickle
	m = Map()

	with open('../data/id2soldier.pkl', 'rb') as f:
		id2soldier = pickle.load(f)
	p1 = Player('GAO1', 900, m, id2soldier)
	p2 = Player('GAO2', 901, m, id2soldier)
	p3 = Player('GAO3', 902, m, id2soldier)
	p4 = Player('GAO4', 903, m, id2soldier)
	print p1
	for k in p1.lands:
		print k

	for k in p1.soldiers['K']:
		print k


	for k in p1.soldiers['W']:
		print k

	print p1.map.id2land[14].unmanning




