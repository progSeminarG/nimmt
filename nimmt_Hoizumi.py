import random
import copy

##############
class Player(object):
	def get_know_dealer(self,dealer_input):
		self.dealer = dealer_input
	def get_hand(self,my_cards_input):
		self.my_cards = my_cards_input
	def put_card(self):
		return self.my_cards.pop(0)
	def taking_column(self):
		return 0
	
	def get_field(self):
		self.field = self.dealer.field


def print_for_debug(a):
	f = open('debug.txt','w')
	for value in a:
		f.write(str(value) + '\n')
	f.close()
def print_for_debugb(a):
	f = open("debug.txt","w")
	f.write(str(a) + "\n")
	f.close()

class HoizumiAI(Player):
	def get_know_dealer(self,dealer_input):		#ある種__init()__見たい最初だけ呼ばれる
		self.__dealer_info = dealer_input
		self.__num_of_players = self.__dealer_info.num_players
		self.__num_of_hand = self.__dealer_info.num_hand
		self.__num_of_rows = self.__dealer_info.num_field
	
	def get_field(self):
		self.field = self.__dealer_info.field
		self.mygame.my_fields.append(copy.deepcopy(self.field))			#自分のnimmtインスタンスにそれぞれの場を入れる
	
	def put_card(self):
		self.get_field()
		if len(self.my_cards) > 9:
			self.my_round += 1
			self.mygame.leaving_cards.append(list(range(1,105)))		#roundごとに全てのカードを入れる
			self.mygame.my_cards_virtual.append(list(self.my_cards)) #自分がもらったカードをnimmtインスタンスにも入れておく
		"""
		if self.my_round == 0:
			self.my_putting_card = self.my_first_round_algo()
		elif self.my_round == 1:
			self.my_putting_card = self.my_second_round_algo()
		elif self.my_round == 2:
			self.my_putting_card = self.my_third_round_algo()
		else:
			tmp = self.mygame.my_game_point.index(min(self.mygame.my_game_point))
			use_algo = {'0' : self.my_first_round_algo,'1' : self.my_second_round_algo,'2' : self.my_third_round_algo}
			if self.my_round > 2:
				if len(self.which_algo) != (self.my_round + 1):
					self.which_algo.append(self.which_algo[tmp])
				
				self.my_putting_card = use_algo[str(self.which_algo[self.which_algo[-1]])]()
			else:
				self.my_putting_card = use_algo[str(tmp)]()
		"""	
		self.my_putting_card = self.my_fourth_round_algo()
		#self.my_putting_card = self.my_cards.pop(0)
		self.mygame.my_putting_card_virtual.append(self.my_putting_card)	#自分のnimmtインスタンスに自分が出したカードを押し込む
			
		return self.my_putting_card
	
	class My_nimmt:					#自分のnimmtクラス(独自にゲームを行う)
		def __init__(self):
			self.my_fields = []		#全ての場が入る3次元配列となる
			self.my_game_point = []		#全てのラウンドにおける自分が得た値(大きいほど悪)
			self.my_putting_card_virtual = []	#自分が出した全てのカード (len()でターン数がわかる)
			self.my_other_players_cards = []	#全てのターンにおける他の人が出したカード(2次元配列)(ただし自分がカードを出した後に入る)
			self.leaving_cards = []	#最初に全てのカードをput_cardで入れ、出されたカードより残りのカードを減らしていく(全てを記録する場合2次元配列)
			self.my_cards_virtual = []	#ディーラにもらったカードを入れておくもの(2次元配列)
		def count_cows(self,field_cards,col_number):	#col_numberの列の牛を数える
			sum=0
			for value in field_cards[col_number]:
				if value == 55:
					sum += 7
				elif value%11 == 0:
					sum += 5
				elif value%10 == 0:
					sum += 3
				elif value%5 == 0:
					sum += 2
				else:
					sum += 1
			return sum
		def min_cows(self,field_cards):		#一番牛の数が少ない列を返す
			min = 200
			myindex = 0
			for i in range(len(field_cards)):
				if self.count_cows(field_cards,i) < min:
					min = self.count_cows(field_cards,i)
					myindex = i
			return myindex

		
		def play_the_game_virtual(self,field,my_putting_card,other_players_cards):	#自分の中で仮想にゲームを行う返り値は自分の得た値
			myfield = copy.deepcopy(field)							#my_putting_cardにより、得る値がどのように変わるかを見れる
			other_p_cards = list(other_players_cards)
			other_p_cards.append(my_putting_card)
			other_p_cards.sort()
			for value in other_p_cards:
				flag = -1
				mymin = 104
				penal = 0
				for field_value_index in range(len(myfield)):
					if myfield[field_value_index][-1] < value:
						if mymin > (value - myfield[field_value_index][-1]):
							mymin = value - myfield[field_value_index][-1]
							flag = field_value_index
				if flag == -1:
					takingrow = self.min_cows(myfield)	#他の人は一番牛が小さくなる列を選ぶと推測
					penal = self.count_cows(myfield,takingrow)
					myfield[takingrow].clear()
					myfield[takingrow].append(value) 
				elif flag in list(range(4)):
					if len(myfield[flag]) > 4:
						penal = self.count_cows(myfield,flag)
						myfield[flag].clear()
						myfield[flag].append(value)
					else:
						myfield[flag].append(value)
				
				if value == my_putting_card:
					myfield.clear()
					return penal

		def play_the_game_real(self):
			return self.play_the_game_virtual(self.my_fields[-1],self.my_putting_card_virtual[-1],self.my_other_players_cards[-1])
			#return self.play_the_game_virtual([[23],[100],[101],[102]],50,[24,25,26,27])			

		def calc_leaving_cards(self):			#残っているカードを計算する
			if len(self.leaving_cards) == 0:
				return
			for value in self.my_other_players_cards[-1]:
				if value in self.leaving_cards[-1]:
					self.leaving_cards[-1].remove(value)
			if len(self.my_putting_card_virtual) != 0:
				if self.my_putting_card_virtual[-1] in self.leaving_cards[-1]:
					self.leaving_cards[-1].remove(self.my_putting_card_virtual[-1])
			for myrow in self.my_fields[-1]:
				for value in myrow:
					if value in self.leaving_cards[-1]:
						self.leaving_cards[-1].remove(value)
		
		

					 
	def __init__(self):
		self.mygame = HoizumiAI.My_nimmt()
		self.my_penal = []			#自分が得たであろうターン毎のペナルティー
		self.my_round = -1			#現在のラウンドを記録
		self.which_algo = [0,1,2]			#使ったアルゴリズムを入れておく
	def get_played_cards(self,played_cards):
		self.__played_cards = list(played_cards)
		self.__played_cards.remove(self.my_putting_card)	#自分のカードを消す
		self.mygame.my_other_players_cards.append(copy.deepcopy(self.__played_cards))	#自分のnimmtインスタンスに他人のカードを流し込む
		self.mygame.calc_leaving_cards()		#場に出たカードを全てのカードから消していく	
		
		self.my_penal.append(self.mygame.play_the_game_real())		#自分のnimmtによりペナルティーを計算する
		
		#print_for_debug(self.mygame.my_other_players_cards)	
		if (len(self.my_penal) % 10) == 0:			#ラウンドごとにpenalをまとめている
			sum = 0
			for i in range(self.my_round*10,self.my_round*10 + 10):
				sum += self.my_penal[i]
			self.mygame.my_game_point.append(sum)
		for arr in self.mygame.my_cards_virtual:
			arr.sort() 
		#print_for_debug(self.mygame.my_game_point)
					
								
	def my_first_round_algo(self):	#一番最初に行う人(これを基準に評価し、それ以降のroundに影響が出る)
		self.my_cards.sort()
		if len(self.my_cards) > 9:
			return self.my_cards.pop(-2) #最後より一つ前の値を使う
		else:
			field_element_num = 0
			for my_row in self.field:
				field_element_num += len(my_row)
			if field_element_num > 18:	#緊急事態のため一番でかいやつを出す
				if len(self.my_cards) != 0:
					return self.my_cards.pop(-1)
		
			elif field_element_num > 15:	#場のカードが12枚を超えたらやばいから小さめのカ-ドを選ぶ
				lastnum = []
				for my_row in self.field:
					lastnum.append(my_row[-1])
				lastnum.sort()
				myselection = [value for value in self.my_cards if lastnum[1] < value] #rowの最後の小さい方から2つめより大きいものを作る
				if len(myselection) != 0:
					if (len(self.my_cards)-1) !=  self.my_cards.index(myselection[0]): #この中でも一番大きいやつは残しておく
						return self.my_cards.pop(self.my_cards.index(myselection[0]))
				else:
					myselection = [value for value in self.my_cards if lastnum[0] < value] #rowの最後の一番小さいやつより大きいやつ
					if len(myselection) != 0:	
						if(len(self.my_cards)-1) != self.my_cards.index(myselection[0]):
							return self.my_cards.pop(self.my_cards.index(myselection[0])) 
				if len(self.my_cards) > 1:
					return self.my_cards.pop(1)
				else:
					return self.my_cards.pop(0)	
				
					
			else:	#安心して自分の値を出す
				lastnum = []
				for my_row in self.field:
					lastnum.append(my_row[-1])
				lastnum.sort()
				for value in lastnum:	#この中から一番小さい数字から置いていくが、なかった場合次を探し最終的に何もなかったら一番小さいやつ
					myselection = [val for val in self.my_cards if val > value]
					if len(myselection) != 0:
						return self.my_cards.pop(self.my_cards.index(myselection[0]))
				if len(self.my_cards) != 0:
					return self.my_cards.pop(0)	
							
		
	def my_second_round_algo(self):		#2番目に行う人(一回目がある値よりもpenaltyが低ければ1回目を優先)
		self.my_cards.sort()
		for my_array in self.mygame.my_fields[-1]:		#確定カードを持っている場合優先
			if len(my_array) == 4:
				myselection = [val for val in self.my_cards if (val-my_array[-1]) == 1]
				if len(myselection) != 0:
					return self.my_cards.pop(self.my_cards.index(myselection[0]))
		
		if len(self.my_cards) > 1:	#自分のカードの最大から最小を決めて、場に出ていないカードのどの位置にあるか調べる
			mymax = self.my_cards[-1]
			mymin = self.my_cards[0]
			if (mymax - mymin) > 51:	#攻撃する
				tmp = list(self.mygame.leaving_cards[self.my_round]) #これが今現在場に出てきていないカードたち
				part_of_one = [val for val in tmp if mymin > val]	#下の方のカードを持っている集団
				part_of_three = [val for val in tmp if mymax < val]	#上の方のカードを持っている集団
				if len(part_of_one) > len(part_of_three):		#攻撃チャンス
					baias = 7
					if len(self.mygame.my_other_players_cards) != 0:
						baias = len(self.mygame.my_other_players_cards[0])
					
					if baias > 5:
						attack_num = 18
					else:
						attack_num = 20
					num_of_element = 0
					last_cards = []
					for my_array in self.mygame.my_fields[-1]:
						num_of_element += len(my_array)
						last_cards.append(my_array[-1])
					if num_of_element >= attack_num:		#attack_numより大きい場合、フィールドの一番右より小さく一番大きい値を取ってくる
						myselection = [val for val in self.my_cards if min(last_cards) > val]
						myselection.sort()
						if len(myselection) != 0:
							return self.my_cards.pop(self.my_cards.index(myselection[-1]))
						else:
							return self.my_cards.pop(0)		#列のコストが一番小さいやつを取りたいため
						
					else:
						last_cards.sort()
						last_cards.reverse()
						for value in last_cards:
							myselection = [val for val in self.my_cards if val > value]	#列の右端の一番でかいやつよりも大きいやつなかったら次
							if len(myselection) != 0:
								return self.my_cards.pop(self.my_cards.index(myselection[0]))
						return self.my_cards.pop(0)	#列のコストが一番小さいやつを好むため
				else:	#あんまり攻撃はしないかも(危機的状況下を判断した方が良い)
					last_cards = []
					num_of_element = 0	
					for each_row in self.mygame.my_fields[-1]:
						last_cards.append(each_row[-1])
						num_of_element += len(each_row)
					last_cards.sort()
					if num_of_element > 19:	#やばいからそれぞれの列を計算して見て値が10以下だったら一番小さい値を出す
						for col in range(4):
							if 11 > self.mygame.count_cows(self.mygame.my_fields[-1],col):
								return self.my_cards.pop(0)
						myselection = [val for val in self.my_cards if val < last_cards[0]] #右端の一番小さいやつよりも小さく一番大きい値
						if len(myselection) != 0:
							return self.my_cards.pop(self.mycards.index(myselection[-1]))
						else:
							return self.my_cards.pop(-1)	#とりあえずしたから２番目	
					else:
									#一番小さいやつから見ていってそれ以上の場合はその一番小さな値を出す
						myselection = [val for val in self.my_cards if val > last_cards[0]]
						if len(myselection) != 0:
							return self.my_cards.pop(self.my_cards.index(myselection[0]))
						else:
							return self.my_cards.pop(-2)	#とりあえず上から2番目
					
			else:		#割と守り(本当はそれぞれの列の長さを数えてそれも考慮した方が良い)
				last_cards = []
				count_element = 0
				for my_row in self.mygame.my_fields[-1]:
					last_cards.append(my_row[-1])
					count_element += len(my_row) 
				last_cards.sort()		#列の右端のmin,maxの間の値で一番小さくないものをとる
				if count_element > 18:
					myselection = [val for val in self.my_cards if val < last_cards[0]]	#一番小さいやつよりも小さくて一番大きいやつ
					if len(myselection) != 0:
						return self.my_cards.pop(self.my_cards.index(myselection[-1]))
				else:
					myselection = [val for val in self.my_cards if val > last_cards[0]]	#一番小さいやつより大きくて一番小さいやつ
					if len(myselection) != 0:
						return self.my_cards.pop(self.my_cards.index(myselection[0]))
				if len(self.my_cards) > 1:
					return self.my_cards.pop(1)
				else:
					return self.my_cards.pop(0)
		else:
			return self.my_cards.pop(0)

	def my_third_round_algo(self):
		self.my_cards.sort()
		last_vals = []
		arr_len = []
		for arr in self.mygame.my_fields[-1]:
			last_vals.append(arr[-1])
			arr_len.append(len(arr))
		for i in range(len(arr_len)):
			if arr_len[i] == 4:
				myselection = [value for value in self.my_cards if value > last_vals[i]]
				if len(myselection) != 0:
					return self.my_cards.pop(self.my_cards.index(myselection[0]))
														#確定カードの判定を行った
		last_vals.sort()
		part_of_small = [val for val in self.my_cards if val < 52]
		part_of_big   = [val for val in self.my_cards if val >= 52]
		if len(part_of_small) > len(part_of_big):
			for value in arr_len:
				if value < 2:		#場rowが1になっている時小さい方からバンバン出す(ただし一番小さいやつは取っておく)
					if len(self.my_cards) > 1:
						return self.my_cards.pop(1)
				else:
					if len(part_of_small) != 0:
						return self.my_cards.pop(self.my_cards.index(part_of_small[-1]))
					else:
						return self.my_cards.pop()
		else:
			sum = 0
			for val in arr_len:
				sum += val
			if sum > 19:		#場のカードが20枚を超えたら一番小さいコストの列の最後の値より小さくて一番大きいやつを出す
				myindex = self.mygame.min_cows(self.mygame.my_fields[-1])
				myselection = [val for val in self.my_cards if val < self.mygame.my_fields[-1][myindex][-1]]
				if len(myselection) != 0:
					return self.my_cards.pop(self.my_cards.index(myselection[-1]))
				return self.my_cards.pop()	
			else:
				other_cards_min = [val for val in self.mygame.leaving_cards[-1] if self.my_cards[0] > val]	#自分のカードより残りの小さいカード
				other_cards_max = [val for val in self.mygame.leaving_cards[-1] if self.my_cards[-1] < val]	#自分のカードより大きいカード
				if len(other_cards_min) < 4 and len(self.my_cards) < 6:	#5ターン目以降
					return self.my_cards.pop(0)
				elif len(other_cards_max) < 4:
					if sum < 17:	#この場合、場における一番小さな値をおく
						myselection = [val for val in self.my_cards if val > last_vals[0]]
						if len(myselection) != 0:
							return self.my_cards.pop(self.my_cards.index(myselection[0]))
					else:	#勝負どき(他の人がとってくれると信じて出ている一番コストが少ない列の値より小さいやつで一番大きやつを出す)
						myindex = self.mygame.min_cows(self.mygame.my_fields[-1]) 
						myselection = [val for val in self.my_cards if val < self.mygame.my_fields[-1][myindex][-1]]
						if len(myselection) != 0:
							return self.my_cards.pop(self.my_cards.index(myselection[-1]))
						else:	#諦めて小さめの大きめのやつを出す
							if len(self.my_cards) > 1:
								return self.my_cards.pop(1)
							else:
								return self.my_cards.pop(0)
				else:
					return self.my_first_round_algo()	#外注w	
					
					
			return self.my_second_round_algo()		


	def my_fourth_round_algo(self):
		num_of_all_cards = self.__num_of_players * (self.__num_of_hand - 1) + self.__num_of_rows
		num_of_all_cards = num_of_all_cards - ((self.__num_of_hand - len(self.my_cards)) * (self.__num_of_players - 1)) - self.__num_of_rows #今のターンでの残りのカード数
															#さらに自分のカードは分かっているので引いておく
		min_of_penal = []		#この値が一番小さいindexを使う
		for value in self.my_cards:
			penal_sum = 0
			for i in range(50):
				speculative_cards = random.sample(list(self.mygame.leaving_cards[-1]),num_of_all_cards) 
				other_people_putting = random.sample(speculative_cards,self.__num_of_players - 1)
				penal_sum += self.mygame.play_the_game_virtual(self.mygame.my_fields[-1],value,other_people_putting)	
			min_of_penal.append(penal_sum)
			
		select_index = 	min_of_penal.index(min(min_of_penal))
		return self.my_cards.pop(select_index)

	def my_fifth_round_algo(self):
		num_of_all_cards = self.__num_of_players * (self.__num_of_hand - 1) + self.__num_of_rows
		num_of_all_cards = num_of_all_cards - ((self.__num_of_hand - len(self.my_cards)) * (self.__num_of_players - 1)) - self.__num_of_rows #今のターンでの残りのカード数
						#さらに自分のカードは分かっているので引いておく
		min_of_penal = []               #この値が一番小さいindexを使う
		for value in self.my_cards:
			penal_sum = 0
		for i in range(100):
			speculative_cards = random.sample(list(self.mygame.leaving_cards[-1]),num_of_all_cards)	#ここでカードを分ける
			other_people_putting = []
			for i in range(self.__num_of_players - 1):
				other_people_putting.append(random.sample(speculative_cards,len(self.my_cards)))
				for remove_val in other_people_putting[-1]:
					if remove_val in speculative_cards:
						speculative_cards.remove(remove_val)
			#ここで他の人たちの動きをシュミレートするのだが、virtualで作っていなかったため、自分のインスタンスを一回退避させておく
			tmp = self.my_cards
			tmp2 = self.field
			self.field = self.mygame.my_fields[-1]
			other_people = []
			for k in range(self.__num_of_players - 1):
				self.my_cards = other_people_putting[k]
				other_people.append(self.my_first_round_algo())
			self.my_cards = tmp
			self.field = tmp2
			penal_sum += self.mygame.play_the_game_virtual(self.mygame.my_fields[-1],value,other_people)
		min_of_penal.append(penal_sum)

		select_index =  min_of_penal.index(min(min_of_penal))
		return self.my_cards.pop(select_index)

