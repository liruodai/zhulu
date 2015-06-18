#!/usr/bin/env python
#coding=utf-8
#finished on 2015.6.2
import socket
import threading
from Queue import Queue

from Player import Player
from Map import Map

from random import shuffle,randint
import sys
import copy
import pickle


Yan, Qi, Qin, Chu = 900, 901, 902, 903
class Server:
	'''
	This is the server class. Provide service on the server 
	'''
	# @param host, the IP of the server
	# @param port, the port that has been listened
	
	def __init__(self, host = '127.0.0.1', port = 30000):
		'''
		do some initial. Load some data such as map,
		'''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Socket has been created!'
		self.sock.bind((host, port))
		self.sock.listen(10)
		print 'Socket now listening'
		
		# 载入地图数据
		self.map = Map()

		# 载入id2soldier
		with open('../data/id2soldier.pkl', 'rb') as f:
			self.id2soldier = pickle.load(f)

		# 用于随机化分配各家势力
		self.rand_force = [Yan, Qi, Qin, Chu]
		shuffle(self.rand_force)
		
		# socket列表。key = socket connection, value = country
		self.conn_list = {}

		# 玩家nickname列表。key = country, value = nickname. 用来初始化。	
		self.nickname_list = {}

		# 玩家列表。key = country ID, value = player()
		self.players_list = {}

		# 标记状态
		self.status = 'LOGIN'
		
		# 玩家排位，列表中元素为各方势力值 eg.900 901 903 902
		self.player_order = []
		# 玩家turn顺序表，存势力号900,901...
		self.turn_list = []

		# 当前turn，存势力号900等
		self.current_turn = 0
		self.next_turn = 0
		# 标记当前round
		self.round = 1
		
		# put receive into the queue. message begins with 900# to indicate the force  
		self.recv_queue = Queue(32)
		
		# send message to everyone use an queue.
		self.send_queue = {}
		for country in self.rand_force:
			self.send_queue[country] = Queue(32)
			# print country
		
		
	## 从客户端接收消息，并且放入公用的接收消息队列中
	# @param conn, socket变量
	def recv_data(self, conn):
		while True:
			try:
				raw_data = conn.recv(1024)
				# 把接收到的数据放入queue中，以$隔开。 势力$接收到的消息
				msg = str(self.conn_list[conn]) + '$' + raw_data
				# put message into the queue
				self.recv_queue.put(msg, 1)
				# print 'recv_data: ' + msg
			except:
				pass
	
	
	## 从发送队列中依次取消息发送
	# @param conn, the socket connection
	def send_data(self, conn):
		while True:
			# try to obtain the message from the queue
			try:
				# obtain message from queue and send them
				data = self.send_queue[self.conn_list[conn]].get(1)
				# print data
				try:
					conn.send(data)
					# print 'send_data:  ' + data
				except:
					pass
			except:
				pass
	
	## Server向玩家广播消息。（主线程向消息队列中压入消息）
	# @param msg, 需要压入的消息。
	def broadcast(self, msg):
		for v in self.send_queue.values():
			v.put(msg, 1)
		print 'broadcast: ' + msg

	## Server向一个玩家或多个玩家发送消息。（向消息队列中压入消息）
	# @param msg, 需要压入的消息；
	# @param force_list, 需要发送的对象势力或势力列表，(存放势力值，900,901等等)。
	def send_msg(self, msg, force_list):
		if isinstance(force_list, list):	#若force_list是国家列表
			for v in force_list:
				self.send_queue[v].put(msg, 1)
				print 'send msg %s to %d: ' % (msg, v)
		if isinstance(force_list, int):		#若force_list是单个国家
			self.send_queue[force_list].put(msg, 1)
			print 'send msg %s to %d: ' % (msg, force_list)
	
	## 编码信息。数据格式：eg：LOGIN#xiaoming,huangjiaozhu,choudoufu,laoganma;
	# @param cmd, 类型：字符串, 内容：命令, eg:'LOGIN'
	# @param data_list, 类型：任意int、float、str或它们的数组, 内容：数据, eg:'nickname'或['nickname','xiaoming']
	def encode_msg(self, cmd, data_list):
		temp_data = copy.deepcopy(data_list)
		if isinstance(temp_data, list):		#若data_list是数据列表
			for idx, item in enumerate(temp_data):
				temp_data[idx] = str(item)	# 将数据转化为str型
			temp_data = ','.join(temp_data)
			return cmd + '#' + temp_data + ';'
		if isinstance(temp_data, str):		#若data_list是单个字符串数据
			temp_data = str(temp_data)
			return cmd + '#' + temp_data + ';'
	
	## 接收信息并解码。返回解码值，如果多条消息粘连，将第一条之后的消息按原格式放回消息队列recv_queue中。
	# @return: force(int), cmd(str), data(str)
	def recv_msg(self):
		try:
			raw_data = self.recv_queue.get(1)	# 从消息队列中取消息
			print 'raw_data: ' + raw_data
			data_list = raw_data.split(';')		# 先以‘;’为标志解开
			if '' != raw_data[1]:				# 判断是否有多条消息粘连，若粘连
				for n in data_list[1:-1]:		# 则将第一条之后的消息加‘;’放回消息队列
					self.recv_queue.put(n+';', 1)
				print self.recv_queue
			force, msg = data_list[0].split('$')	# 解码第一条消息
			force = int(force)
			cmd, data = msg.split('#')				# force, cmd, data分别为势力，指令，数据。
			# data = data.split(',') 				# type(data) == list
			# # 若data中只有一个str，则将data转化为str类型，否则保留为list类型
			# if 1 == len(data):
			# 	data = data[0]
			# print 'decoded data: ' + str(force), cmd, data
			return force, cmd, data
		except:
			print 'Wrong msg format!'
		
	## 游戏初始化，实例化四个player，存入players_list
	def game_init(self):
		#self.nickname_list= {900:'1',901:'2',902:'3',903:'4'}
		player_Yan = Player(self.nickname_list[Yan], Yan, self.map, self.id2soldier)
		# print player_Yan.lands[0], player_Yan.map.id2land[player_Yan.lands[0]].unmanning	
		player_Qi = Player(self.nickname_list[Qi], Qi, self.map, self.id2soldier)
		# print player_Qi.lands[0], player_Qi.map.id2land[player_Qi.lands[0]].unmanning	
		player_Qin = Player(self.nickname_list[Qin], Qin, self.map, self.id2soldier)
		# print player_Yan.lands[0], player_Yan.map.id2land[player_Yan.lands[0]].unmanning	
		player_Chu = Player(self.nickname_list[Chu], Chu, self.map, self.id2soldier)
		self.players_list = { Yan: player_Yan, Qi: player_Qi, Qin: player_Qin, Chu: player_Chu }
							
		# for player in self.players_list.values():
		# 	print player.map.id2land[player.lands[0]].unmanning	

	## 判断行军操作是否合法
	# @param: march_dic 记录每个soldier消耗的ap点数，key:s_id，value:消耗的ap
	# @param: force 势力号
	# @param: dst 行军目的地
	# @param: s_id 士兵id
	# @return: True or False
	def if_march_legal(self, march_dic, force, dst, s_id): 	# 当前版本每次只行军1格，判断地形是平原or山地，加1 or 加2. 
		# 根据dst（即id）判断地形类型是山地or平原，进而加1or加2判断合法性。
		if self.map.id2land[dst].type == 0: 			
			land_ap = 2 				# 山地行军步兵消耗2点ap
		else: 
			land_ap = 1 				# 平原行军步兵消耗1点ap

		for item in s_id:
			if self.id2soldier[item].type == 'K':
				minus_ap = land_ap / 2.0 		# 骑兵行军消耗减半
			else:
				minus_ap = land_ap 				# 步兵行军消耗正常
			if item in march_dic: 		# 若该soldier在march_dic中，说明以前行军过，加上之前的行军消耗判断是否合法
				if self.players_list[force].ap - march_dic[item] - minus_ap < 0:
					return False
			else: 						# 该soldier不在march_dic中
				if self.players_list[force].ap - minus_ap < 0:
					return False
		else: 			# list中soldier全部合法，才能返回True
			return True

	## 记录每次行军，每个soldier花费的行动点ap，存在march_dic中，返回最大消耗ap
	# @param: march_dic 存储每个soldier花费的行动点ap，直到收到DONE#march时清空
	# @param: dst 行军目的地id号
	# @param: s_id 行军的soldier的id号，type为list，list内数据为int
	# @return: max_ap 目前为止消耗的最大行动点数ap
	def get_march_ap(self, march_dic, dst, s_id): 	# 操作与函数if_march_legal相似
		if self.map.id2land[dst].type == 0: 	# 判断地形	
			land_ap = 2
		else:
			land_ap = 1
		
		for item in s_id: 		
			if self.id2soldier[item].type == 'K':
				minus_ap = land_ap / 2.0 		# 骑兵行军消耗减半
			else:
				minus_ap = land_ap 				# 步兵行军消耗正常
			if item in march_dic: 				# 计算每个soldier本次行军总的ap消耗
				march_dic[item] += minus_ap
			else:
				march_dic[item] = minus_ap
		max_ap = max(march_dic.values())
		return max_ap


	## 游戏开始前，AUCTION后的排序
	# @param: 每位玩家的竞价ap点数	
	# @return: order_list(list)，存每位玩家的势力号
	def init_order(self, dic_ap):	# 按照Yan,Qi,Qin,Chu的顺序，逐个确定位置
		dic = copy.deepcopy(dic_ap)
		dic[Yan] += 0.3
		dic[Qi] += 0.2
		dic[Qin] += 0.1
		sorted_dic=sorted(dic.items(),key=lambda d:d[1],reverse=True) 	# 降序排序
		order_list = [sorted_dic[0][0], sorted_dic[1][0], sorted_dic[2][0], sorted_dic[3][0]]
		return order_list

	## 新的回合开始前，玩家行动顺序排序
	# @return: order_list(list)，存每位玩家的势力号
	def get_new_order(self):
		dic = {}
		for idx,force in enumerate(self.player_order):
			dic[force] = self.players_list[force].ap + (3-idx)/10.0
		sorted_dic=sorted(dic.items(),key=lambda d:d[1],reverse=True)
		order_list = [sorted_dic[0][0], sorted_dic[1][0], sorted_dic[2][0], sorted_dic[3][0]]
		return order_list

	## 回合没有结束，得到本回合下一个turn的玩家势力号
	# @return: 下一个turn的force号
	def get_next_turn(self):
		idx = self.turn_list.index(self.current_turn)
		if len(self.turn_list) == idx+1:
			return self.turn_list[0]
		else:
			return self.turn_list[idx+1]

	## 判断游戏是否结束
	# @return: True or False
	def if_gameover(self):
		rand_num = randint(1,6)
		if self.round == 3 and rand_num < 2:
			# 骰子数为1，则结束
			print 'round: %d; dice: %d, game over!' % (self.round, rand_num)
			return True
							   
		elif self.round == 4 and rand_num < 3:
			# 骰子数为1、2，则结束
			print 'round: %d; dice: %d, game over!' % (self.round, rand_num)
			return True
								   
		elif self.round == 5 and rand_num < 4:
			# 骰子数为1、2、3，则结束
			print 'round: %d; dice: %d, game over!' % (self.round, rand_num)
			return True
								   
		elif self.round == 6:
			# 一定结束
			print 'round: %d, game over!' % (round)
			return True

		else:
			print 'round: %d; dice: %d, game continue.' % (self.round, rand_num)
			return False

	## 游戏的主循环
	def run(self):
		while True:
			if self.status == 'LOGIN':
				if len(self.conn_list) < 4:		# 玩家人数少于4
					conn, addr = self.sock.accept()		# 持续监听连接
					print 'Connected with ' + addr[0] + ':' + str(addr[1])
					self.conn_list[conn] = self.rand_force.pop()	# 有新连接，给分配国家号
					threading.Thread(target = self.recv_data, args = (conn, )).start()	# 开收消息线程
					threading.Thread(target = self.send_data, args = (conn, )).start()	# 开发消息线程
					force, cmd, data = self.recv_msg()		# 接收登录消息
					if cmd == 'LOGIN':
						# Saving login information in nickname_list
						self.nickname_list[force] = data
						print "Online players: ", self.nickname_list.values()
						# Then send online players_list to online players
						msg_to_send = self.encode_msg('NICK',self.nickname_list.values())
						self.send_msg(msg_to_send, self.nickname_list.keys())
						print 'New player coming & send msg'
				else:
					self.status = 'INIT'

			elif self.status == 'INIT':
				self.game_init()	# game初始化
				for force in [Yan, Qi, Qin, Chu]:
					msg_to_send = self.encode_msg('ALLOC',[force,self.nickname_list[Yan],self.nickname_list[Qi],self.nickname_list[Qin],self.nickname_list[Chu]])
					self.send_msg(msg_to_send,force)		# 广播每个玩家的势力分配情况
				done_list = []		# 存储收到的DONE#init消息
				while len(done_list) < 4:	# 不够4个，持续接收
					force, cmd, data = self.recv_msg()
					if 'DONE' == cmd and 'init' == data:	
						if force not in done_list:	# 确定是新玩家发送的DONE#init才有效
							done_list.append(force)
				else:
					print '4 players here! Start auction!'
					self.status = 'AUCTION'		# 跳转到AUCTION状态
			
			elif self.status == 'AUCTION':
				msg_to_send = self.encode_msg('START','auction')
				self.broadcast(msg_to_send)	# 广播START#auction消息
				auction_dic = {}		# auction_dic用来存储每个玩家的竞位点数，key:force; value:ap
				while len(auction_dic) < 4:	# 不够4个，则收消息，存储
					force, cmd, data = self.recv_msg()
					if 'AUCTION' == cmd:
						auction_dic[force] = int(data)
				else: 			# 收齐4个AUCTION消息
					# 排序
					self.player_order = self.init_order(auction_dic)
					print 'auction_dic: ', auction_dic
					# 从player.ap中减去消耗的ap点数
					for force in auction_dic:
						self.players_list[force].ap -= auction_dic[force]
						print 'Player[%d].ap: %d' % (force, self.players_list[force].ap) 
					msg_to_send = self.encode_msg('ORDER',self.player_order)
					self.broadcast(msg_to_send)
					self.status = 'GAME'
					print 'Auction complete! Game start!'

			elif self.status == 'GAME':
				# 确定回合
				# 确定哪个玩家的turn
				# recv_msg
				# action
				# update
				# DONE#turn

				# 初始化轮次表turn_list和当前轮次current_turn
				self.turn_list = copy.deepcopy(self.player_order)
				self.current_turn = copy.deepcopy(self.turn_list[0])
				self.next_turn = copy.deepcopy(self.turn_list[1])
				print "player_order: ", type(self.player_order[0]), self.player_order
				print "current_turn: ", type(self.current_turn), self.current_turn
				print "next_turn: ", type(self.next_turn), self.next_turn
				print "turn_list: ", self.turn_list, type(self.turn_list[0])
				player_action_flag = 0 		# 标志变量，用来标记player在它的turn中是否有行动；1行动，0无行动
				# 初始化行军部分参数
				march_dic = {} 	# 存储一次完整行军操作移动的士兵和每个士兵消耗的行动点数
				max_ap = 0 			# 存储一次完整行军操作消耗的最大行动点数ap

				msg_to_send = self.encode_msg('ROUND', [self.round, self.current_turn])
				self.broadcast(msg_to_send)

				while self.status == 'GAME':
					force, cmd, data = self.recv_msg() 	# 第一版的ACTION行动的data只有dst一个参数
					if  self.current_turn == force: 	# 必须是当前turn的玩家发出的指令
						print "right force number!"

						if cmd == 'MARCH': 		# 行军指令
							print 'march action!'
							player = self.players_list[force]
							data = data.split(',') 	
							dst = int(data[0]) 			# dst为行军目的地id号
							s_id = map(int, data[1:]) 	# s_id为行军soldier的id号
							if self.if_march_legal(march_dic, force, dst, s_id): 	# 如果行军操作合法
								print 'march legal.'

								player_action_flag = 1 	# 标记此player已经action

								self.players_list[force].move(force, dst, s_id) 		# 修改players_list中除ap外的所有信息
								max_ap = self.get_march_ap(march_dic, dst, s_id) 		# 得到当前所有soldier行军消耗的最大ap数
								print 'max_ap: ', max_ap
								msg_to_send = self.encode_msg('UPDATE', [force, int(player.ap-max_ap), 'MARCH', dst, ','.join(map(str, s_id))])
								self.broadcast(msg_to_send)
							else: 					# 如果行军操作不合法
								print 'march illegal!'
								msg_to_send = self.encode_msg('ILLEGAL', ['MARCH', dst, ','.join(map(str, s_id))])
								self.send_msg(msg_to_send, force)

						elif 'DONE' == cmd and 'march' == data: 	# 完成行军指令
							print 'DONE march!'
							self.players_list[force].ap -= max_ap 		# 完成行军，修改ap值
							self.players_list[force].ap = int(self.players_list[force].ap)
							max_ap = 0 						# 临时变量max_ap和march_dic清空
							march_dic = {}

						elif 'DONE' == cmd and 'turn' == data:
							print "DONE turn"
							#判断本round此player能否行动,若被禁掉，从可行动列表中删除
							if player_action_flag == 0 or self.players_list[force].ap <= 0:
								self.turn_list.remove(force) 	# player在本round不再行动，从turn_list中删除
								print "%d did no action or no action point left, its actions end in this round!" % (self.current_turn)
								print "turn_list: ", self.turn_list
								# 广播更新后的turn_list
								# 发送的是不在turn_list中的force
								msg_temp = []
								for item in self.player_order:
									if item not in self.turn_list:
										msg_temp.append(item)
								msg_to_send = self.encode_msg('TURN',msg_temp) 	# 发送turn_list中剔除的force
								self.broadcast(msg_to_send)
								#判断本round是否结束
								if self.turn_list == []:
									#本round已经结束
									print "This round ends! Next round!"
									#判断是否GAME OVER
									if self.if_gameover():
										self.status = 'OVER'
										print "GAME OVER!"
								
									#没有GAME OVER，开始新round				   
									else:
										self.round += 1 	# 新的round
										print "New round %d!" % (self.round)
										self.player_order = self.get_new_order() 	# 玩家完整顺序列表重排列
										# broadcast 新turn顺序
										msg_to_send = self.encode_msg('ORDER',self.player_order)
										self.broadcast(msg_to_send)

										self.turn_list = copy.deepcopy(self.player_order) 	# 更新实际顺序列表
										self.current_turn = copy.deepcopy(self.turn_list[0]) # 更新当前turn
										self.next_turn = copy.deepcopy(self.turn_list[1]) 		# 更新下一个turn
										for player in self.players_list.values(): 	# 更新所有玩家ap
											player.ap = 10 #每个新round开始时，每个player的ap行动点赋10
										# broadcast 新round和turn
										msg_to_send = self.encode_msg('ROUND', [self.round, self.current_turn])
										self.broadcast(msg_to_send)
								else:
									self.current_turn = copy.deepcopy(self.next_turn)
									self.next_turn = self.get_next_turn()
									# 广播whose turn
									msg_to_send = self.encode_msg('ROUND', [self.round, self.current_turn])
									self.broadcast(msg_to_send)
													   
							else:
								print "Round continue! Next turn!"
								# 本round没有结束，继续此round，下一个玩家的turn
								player_action_flag = 0
								# 确定下一个turn
								self.current_turn = self.next_turn
								self.next_turn = self.get_next_turn()
								# 广播whose turn
								msg_to_send = self.encode_msg('ROUND', [self.round, self.current_turn])
								self.broadcast(msg_to_send)
																		  
			elif self.status == 'OVER':                   
				# self.order_dic={}
				# for player in self.players_list.values():
				# 	self.order_dic[player.country] = player.ap + (3-self.player_order.index(player.country))# keys: country, values: ap+上一轮排序权值
				# order_dic_res=sorted(self.order_dic.items(),key=lambda d:d[1],reverse=True)#按照value排序
				# self.player_order = [order_dic_res[k][0] for k in range(4)]
				#_ = filter(lambda x:x == self.player_order[0], self.players_list.values())[0].nickname
				msg_to_send = self.encode_msg('OVER','print the Winner!')
				self.broadcast(msg_to_send)
				sys.exit(0)		
				
if __name__ == '__main__':
	Server().run()
