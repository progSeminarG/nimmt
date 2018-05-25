#!/usr/local/bin/python3

import random

### 基本 Player クラス (みんなこれを使えば良い) ###
class Player(object):
	### 必須メソッド (4 つ) ###
	def get_know_dealer(self,dealer_input): # ディーラーのインスタンスを得る
		self.dealer = dealer_input
	def get_hand(self,my_cards_input): # ディーラー側で呼んで、手札を得る
		self.my_cards = my_cards_input
	def put_card(self): # ディーラー側で呼んで、どのカードを出すか知らせる
		return self.my_cards.pop(0)
	def taking_column(self): # 一番小さい数を出したときにディーラー側で呼んで、どの列を引き取るか知らせる
		return 0


	def get_field(self): # 場の状況を得る
		self.field = self.dealer.field

### 継承クラス (ここで基本クラスを継承して、様々な処理を行う) ###
#from nimmtHuman import Human
class KikuchiAI(Player):

	def put_card(self):
		#一番小さなカードを出す
		_putting_card = min(self.my_cards)
		self.my_cards.remove(_putting_card)
		return _putting_card
	
	def taking_column(self):

		#列ごとに牛の計算をする
		#そのあとcowリストに入れる。
		cow = []
		for i in range(4):
			cow.append(self.__calc_score(self.dealer.field[i]))

		#min()でもっともちいさいものを出す、index()っていうのがあるんですね！便利！
		return cow.index(min(cow))
		 

	def __calc_score(self,cards): # スコアの計算のためのサブメソッド（ぱくりました。）
		_sum = 0
		for i in cards:
			if i%11 == 0:
				if i % 5 == 0:
					_sum += 7
				else:
					_sum += 5
			elif i % 10 == 0:
				_sum += 3
			elif i % 5 == 0:
				_sum += 2
			else:
				_sum += 1
		return _sum

	def print_field(self):
		_num_field = self.dealer.num_field
		_field = self.dealer.field
		print("current field is:")
		for i in range(_num_field):
			print(_field[i])


