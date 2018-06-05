#!/usr/local/bin/python3

import random
import sys
import copy
from itertools import chain
from math import factorial, ceil, floor
from scipy.misc import comb

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
    def get_played_cards(self,dealer_input):
        self.played_cards = dealer_input


    def get_field(self): # 場の状況を得る
        self.field = self.dealer.field

### 継承クラス (ここで基本クラスを継承して、様々な処理を行う) ###
#from nimmtTakahashi import TakahashiAI
class Field(object):
    def __init__(self,dealer):
        self.__dealer = dealer
        self.__num_field = self.__dealer.num_field # 4
        self.__num_max_column = self.__dealer.num_max_column # 5
        self.__max_card = self.__dealer.max_card # 104
        self.update()

    def update(self,field=None):
        if field is None:
            self.__field = self.__dealer.field
        else:
            self.__field = field
        self.__field_score = [Field.calc_score(self.__field[i]) for i in range(self.__num_field)]
        self.__most_right_field = [max(self.__field[i]) for i in range(self.__num_field)]
        self.__field_order = sorted(range(self.__num_field),key=lambda k:self.__most_right_field[k])
        self.__num_cards_column = [len(self.__field[i]) for i in range(self.__num_field)]
        self.__min_field = min(self.__most_right_field)
        self.__min_column = self.__most_right_field.index(self.__min_field)
        self.__min_num = self.__num_cards_column[self.__min_column]
        self.__max_field = max(self.__most_right_field)
        self.__max_column = self.__most_right_field.index(self.__max_field)
        self.__max_num = self.__num_cards_column[self.__max_column]

    @property
    def num_field(self):
        return self.__dealer.num_field
    @property
    def num_max_column(self):
        return self.__dealer.num_max_column
    @property
    def field(self):
        return self.__field
    @property
    def field_score(self):
        return self.__field_score
    @property
    def most_right_field(self):
        return self.__most_right_field
    @property
    def field_order(self):
        return self.__field_order
    @property
    def num_cards_column(self):
        return self.__num_cards_column # number of cards in each column
    @property
    def min_field(self):
        return self.__min_field
    @property
    def min_column(self):
        return self.__min_column
    @property
    def min_num(self): # minimum number of field
        return self.__min_num
    @property
    def max_field(self):
        return self.__max_field
    @property
    def max_column(self):
        return self.__max_column # column which has maximum card of field
    @property
    def max_num(self): # maximum card of field
        return self.__max_num
    @property
    def max_card(self): # maximum number of card
        return self.__max_card

    @staticmethod
    def calc_score(cards):
        def _bool_same_digit(num):
            if int(num/10) == 0:
                return False
            else:
                _1st_digit = int(num%10)
                while True:
                    num = int(num/10)
                    if num == 0:
                        break
                    if _1st_digit != int(num%10):
                        return False
                return True
        _sum = 0
        for i in cards:
            if _bool_same_digit(i):
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

class Card(object):
    def __init__(self,number,field_inst,unknown_cards):
        self.__number = number # number of card
        self.__field_inst = field_inst # field instance
        self.__unknown_cards = unknown_cards # list of unknown cards
        self.__num_field = field_inst.num_field # number of column = 4
        self.__num_max_column = field_inst.num_max_column # number of maximum columm = 5
        self.__max_card = field_inst.max_card # maxinum number of card = 104
        self.update(field_inst)

    def update(self,field_inst=None,unknown_cards=None):
        if field_inst is not None:
            self.__field_inst = field_inst
        if unknown_cards is not None:
            self.__unknown_cars = unknown_cards

        self.__num_cards_column = field_inst.num_cards_column
        self.__most_right_field = self.__field_inst.most_right_field
        _local_sequence = sorted(self.__most_right_field + [self.__number]) # most_right_field + self_number
        _index = _local_sequence.index(self.__number) # order of self number in most_right_field
        if _index == 0:
            self.__category = 'l' # low category
            self.__left_neighbor = None
            self.__column = None # putting column
            self.__right_neighbor = _local_sequence[_index+1]
            self.__position = None
            self.__num_space = None
            self.__prior_cards = []
        else:
            self.__category = 'h' # high category
            self.__left_neighbor = _local_sequence[_index-1] # field value of the putting column
            self.__column = self.__most_right_field.index(self.__left_neighbor) # putting column
            self.__right_neighbor = self.__max_card+1 if _index == self.__num_field else _local_sequence[_index+1]
            _local_sequence = sorted(self.__unknown_cards + [self.__left_neighbor] + [self.__number])
            _left_position_lseq = _local_sequence.index(self.__left_neighbor)
            _my_position_lseq = _local_sequence.index(self.__number)
            self.__position = _my_position_lseq \
                - _left_position_lseq \
                + self.__num_cards_column[self.__column] -1
            print("num_max_column:",self.__num_max_column)
            print("self.__num_cards_column:",self.__num_cards_column[self.__column])
            self.__num_space = self.__num_max_column - self.__num_cards_column[self.__column]
            self.__prior_cards = copy.deepcopy(_local_sequence[_left_position_lseq+1:_my_position_lseq])
            print("me:",self.__number)
            print("unknown:",self.__unknown_cards)
            print("field:",self.__field_inst.field)
            print("prior:",self.__prior_cards)
            print("category:", self.__category)
            print("column:", self.__column)
            print("position:", self.__position)
            #sys.exit(1)

    @staticmethod
    def get_score(_num):
        def _bool_same_digit(num):
            if int(num/10) == 0:
                return False
            else:
                _1st_digit = int(num%10)
                while True:
                    num = int(num/10)
                    if num == 0:
                        break
                    if _1st_digit != int(num%10):
                        return False
                return True
        if _bool_same_digit(_num):
            if _num % 5 == 0:
                return 7
            else:
                return 5
        elif _num % 10 == 0:
            return 3
        elif _num % 5 == 0:
            return 2
        else:
            return 1


    @property
    def number(self):
        return self.__number #1,..,104
    @property
    def category(self):
        return self.__category #'l'ow,'h'igh
    @property
    def column(self):
        return self.__column #None, 0,..,3
    @property
    def left_neighbor(self):
        return self.__left_neighbor #None, 1,..,103
    @property
    def right_neighbor(self):
        return self.__right_neighbor #None, 2,..,104
    @property
    def position(self):
        return self.__position #None, 1,.. (most left card's index is 0)
    @property
    def num_space(self):
        return self.__num_space #None, 4, 3, 2, 1, 0
    @property
    def prior_cards(self):
        return self.__prior_cards #list of possible inserting cards


class TakahashiAI(Player):

    def get_know_dealer(self,dealer_input):
        self.__dealer = dealer_input
        self.__num_field = self.__dealer.num_field # 4
        self.__max_card = self.__dealer.max_card # 104
        self.__num_hand = self.__dealer.num_hand # 10
        self.__num_max_column = self.__dealer.num_max_column # 5
        self.__num_players = self.__dealer.num_players
        self.__unknown_cards = [
                i+1
                for i in range(self.__max_card)
                ]
        self.__field_inst = Field(self.__dealer)
        self.__field = self.__field_inst.field
        self.__update_unknown_cards(list(chain.from_iterable(self.__field)))

    def get_hand(self,my_cards_input):
        self.__my_cards = my_cards_input
        self.__my_cards.sort(reverse=True)
        self.__my_original_cards = copy.deepcopy(self.__my_cards)
        self.__update_unknown_cards(self.__my_cards)
        self.__my_cards_inst = [
                Card(self.__my_cards[i],self.__field_inst,self.__unknown_cards)
                for i in range(len(self.__my_cards))
                ]

    def put_card(self):
        self.get_field()
        self.__field_inst.update(field=self.__field)
        self.__update_unknown_cards(list(chain.from_iterable(self.__field)))
#        print(self.__get_probability(2,2,2,4,2))
        _num_try = 100
        print(self.__get_score_ordered_list(self.__unknown_cards))
        print("insert prob:",self.__get_insert_prob())
        sys.exit(1)
        return self.__put_card_by_demo(_num_try)

    def __put_card_by_demo(self,num_try):
        _score_for_my_cards = []
        for _card in self.__my_cards:
            _score_summed = self.__play_random_pack(_card,num_try)
            _score_for_my_cards.append(_score_summed)
        _min_index = _score_for_my_cards.index(min(_score_for_my_cards))
        return self.__my_cards.pop(_min_index)

    def __get_probability(self,_num_each_cards,_num_players,_num_key_cards,_num_all_cards,_num_pick_cards):
        _nfact = factorial(_num_each_cards)
        _num_more = _num_pick_cards%_num_players
        print("#####")
        print(_num_each_cards,_num_players,_num_key_cards,_num_all_cards,_num_pick_cards)
        print(float(_nfact/factorial(_num_each_cards-ceil(_num_pick_cards/_num_players)))**(_num_more))
#        print("in 1:",_nfact,_num_each_cards,ceil(_num_pick_cards/_num_players),_num_more)
        print(float(_nfact/factorial(_num_each_cards-floor(_num_pick_cards/_num_players)))**(_num_players-_num_more))
        print(comb(_num_key_cards,_num_pick_cards))
        print(float(factorial(_num_pick_cards)))
        print(float(factorial(_num_all_cards-_num_pick_cards)/factorial(_num_all_cards-_num_each_cards*_num_players)))
        print(comb(_num_players,_num_more))
        print(float(factorial(_num_all_cards)))
        print("prob:",_nfact/factorial(_num_each_cards-ceil(_num_pick_cards/_num_players))**(_num_more)*(_nfact/factorial(_num_each_cards-floor(_num_pick_cards/_num_players)))**(_num_players-_num_more)*comb(_num_key_cards,_num_pick_cards)*factorial(_num_pick_cards)*factorial(_num_all_cards-_num_pick_cards)/factorial(_num_all_cards-_num_each_cards*_num_players)*comb(_num_players,_num_more)/factorial(_num_all_cards))


        print("####/")
        return (_nfact/factorial(_num_each_cards-ceil(_num_pick_cards/_num_players))) \
                **(_num_more) \
                *(_nfact/factorial(_num_each_cards-floor(_num_pick_cards/_num_players))) \
                **(_num_players-_num_more) \
                *comb(_num_key_cards,_num_pick_cards) \
                *factorial(_num_pick_cards) \
                *factorial(_num_all_cards-_num_pick_cards) \
                /factorial(_num_all_cards-_num_each_cards*_num_players) \
                *comb(_num_players,_num_more) \
                /factorial(_num_all_cards)


    def __get_score_ordered_list(self,_list_of_cards):
        _score = [Card.get_score(i) for i in _list_of_cards]
        return sorted(_list_of_cards,key=lambda card:_score[_list_of_cards.index(card)],reverse=True)

    def __get_insert_prob(self):
        _insert_prob_list = []
        _num_each_cards = len(self.__my_cards_inst)
        _num_players = self.__num_players -1
        _num_all_cards = len(self.__unknown_cards)
        for card in self.__my_cards_inst:
            if card.category is 'h':
                print("prior_cards:",card.prior_cards)
                _num_key_cards = len(card.prior_cards)
                _num_pick_cards = card.num_space
#                _num_pick_cards = _num_key_cards
                print("n:",_num_each_cards)
                print("l:",_num_pick_cards)
                print("s:",_num_players)
                print("N:",_num_all_cards)
                print("m:",_num_key_cards)
                _insert_prob_list.append(self.__get_probability(_num_each_cards,_num_players,_num_key_cards,_num_all_cards,_num_pick_cards))
            else:
                _insert_prob_list.append(None)
        print("cards:",self.__my_cards)
        print("prob:",_insert_prob_list)
        print("field:",self.__field)
        print("unknown:",self.__unknown_cards)

#        mylist = [6,0,0,0,0,0]
#        for i in range(8):
#            print("mylist:",i,mylist)
#            mylist = self.__shift(mylist)

#        _list_of_list_of_tuple = [self.__make_tuple(7,7)]
#        self.__break_tuple(_list_of_list_of_tuple,7)
#        for i in _list_of_list_of_tuple:
#            print(i)

#        print("##### check __mek_rest_tuple")
#        print(self.__make_tuple(7,2))

        
        print("probability2:",self.__get_probability2())

        sys.exit(1)
        return _insert_prob_list

    # calc probability
    # _N: total number of cards
    # _n: number of cards each player has
    # _s: number of playter
    # _m: total number of key cards
    # _l: number of key cards to be distributed
    def __get_probability2(self,_N,_n,_s,_m,_l):
        def perm(_n,_r):
            return comb(_n,_r)*factorial(_r)
        def prod(_n,_s,_list_of_combination):
            _prod = 1
            _ss = _s
            for _tuple in _list_of_combination:
                _prod *= perm(_n,_tuple[0])**_tuple[1]
                _prod *= comb(_ss,_tuple[0])
                _ss -= _tuple[0]
            return _prod
        _prob = 0.0
        for _mp in range(_l,_m+1):
            for _lp in range(_l,_mp+1):
                _pattern = [self.__make_tuple(_mp,_mp)]
                self.__break_tuple(_pattern,_mp)
                _prob += prod(_n,_s,_pattern) * perm(_m,_mp) * perm(_N-_m,_n*_s-_mp)
        _prob /= perm(_N,_n*_s)
        return _prob

    def __break_tuple(self,_list_of_list_of_tuple,_num):
        if _list_of_list_of_tuple[-1] != [(1,_num)]:
            _current_list = copy.deepcopy(_list_of_list_of_tuple[-1]) # only the last one will be revised
            for _tuple in _current_list[::-1]:
                _current_list.remove(_tuple)
                if _tuple[0] > 1: # (x>1,*)
                    _new_num_value = _tuple[0]
                    if _tuple[1] > 1: # (x,y>1) y -> y-1
                        _new_num_people = _tuple[1] -1
                        _current_list.append((_new_num_value,_new_num_people))
                    _rest_num = _num - self.__sum_tuple(_current_list)
                    _current_list += self.__make_tuple(_rest_num,_new_num_value-1)
                    _list_of_list_of_tuple.append(_current_list)
                    self.__break_tuple(_list_of_list_of_tuple,_num)
                    break

    def __make_tuple(self,_total,_num_init):
        _tuple_list = []
        for _num in range(_num_init,0,-1):
            _num_people = int(_total / _num)
            if _num_people > 0:
                _total -= _num * _num_people
                _tuple_list.append((_num,_num_people))
                if _total == 0:
                    return _tuple_list

    def __sum_tuple(self,_list_of_tuple):
        _sum = 0
        for _tuple in _list_of_tuple:
            _sum += _tuple[0]*_tuple[1]
        return _sum

    # given _list_input re-distributed
    def __shift(self,_list_input): #bug: ex) for 6, [2,2,2,0,0,0] can't be detected
        _list = copy.deepcopy(_list_input)
        _num_list = len(_list)
        for k in range(_num_list)[::-1]:
            if _list[k] > 1:
                _list[k] = _list[k]-1
                for l in range(k+1,_num_list):
                    if _list[l] < _list[k]:
                        _list[l] = _list[l]+1
                        return _list

    def __play_random_pack(self,_my_card,_num_play):
        _ged_earned_score_sum = [0]*self.__num_players
        for i in range(_num_play):
            _ged_earned_score = self.__play_random(_my_card)
            _ged_earned_score_sum = [x+y for (x,y) in zip(_ged_earned_score_sum,_ged_earned_score)]
        return _ged_earned_score_sum[-1]

    def __play_random(self,_my_card):
        _ged_played_cards = random.sample(copy.deepcopy(self.__unknown_cards),self.__num_players-1)
        _ged_played_cards.append(_my_card)
        _ged_field = copy.deepcopy(self.__field)
        _ged_earned_cards = [[] for i in range(self.__num_players)]
        _field_score = self.__get_field_score(_ged_field)
        _column = _field_score.index(min(_field_score))
        self._line_up_cards(_ged_field,_ged_played_cards,_ged_earned_cards,self._min_field_score_column)
        _ged_earned_score = [Field.calc_score(_ged_earned_cards[j]) for j in range(self.__num_players)]
        return _ged_earned_score

    def taking_column(self):
        _players_score = self.__dealer.score
        self.__field = self.__dealer.field
        self.__field_score = self.__get_field_score(self.__field)
        _played_cards = self.__dealer.played_cards
        for i in range(self.__num_hand):
            if self.__my_original_cards[i] in _played_cards:
                self.__bib = _played_cards.index(self.__my_original_cards[i])
                _my_card = _played_cards[self.__bib]
                break
        _score_diff = []
        for i in range(self.__num_field):
            _earned_cards = [[] for i in range(self.__num_players)]
            self._line_up_cards(
                    copy.deepcopy(self.__field),
                    copy.deepcopy(_played_cards),
                    _earned_cards,
                    lambda : i
                    )
            _score = [Field.calc_score(_earned_cards[j]) for j in range(self.__num_players)]
            _score = [x+y for (x,y) in zip(_score,_players_score)]
            _my_score = _score[self.__bib]
            _comparing_score = min(_score)
            if _my_score == _comparing_score:
                _comparing_score = sorted(_score)[1]
            _score_diff.append(_my_score - _comparing_score)
        return _score_diff.index(min(_score_diff))
#        return self.__field_score.index(min(self.__field_score))

    def get_played_cards(self,dealer_input):
        self.__played_cards = dealer_input
        self.__update_unknown_cards(self.__played_cards)

    def _line_up_cards(self,_field,_played_cards,_earned_cards,_func_taking_column):
        self.__line_up_cards_recursive(
                _field, #return final field
                _played_cards, #return []
                copy.deepcopy(_played_cards), #no return
                _earned_cards, #return earned cards
                _func_taking_column #no return
                )

    # line_up_cards のコアの部分
    def __line_up_cards_recursive(self,_field,rest_cards,played_cards,_earned_cards,_func_taking_column): 
        _most_right_field = [
                max(_field[i]) for i in range(self.__num_field)
                ]
        _min_field = min(_most_right_field)
        _min_rest_cards = min(rest_cards)
        _min_player = played_cards.index(_min_rest_cards)
        if _min_field > _min_rest_cards: # Field のカードよりも小さいカードが出されたとき
            _field_score = self.__get_field_score(_field)
            _replace_column = _func_taking_column()
            for i in _field[_replace_column]:
                _earned_cards[_min_player].append(i)
            _field[_replace_column] = [rest_cards.pop(rest_cards.index(_min_rest_cards))]
        else: # 小さいカードから順に場にカードを並べる
            for i in sorted(_most_right_field,reverse=True):
                if _min_rest_cards > i:
                    _column = _most_right_field.index(i)
                    _field[_column].append(rest_cards.pop(rest_cards.index(_min_rest_cards)))
                    # 1 列に self.__NUM_MAX_COLUMN (=5) 枚より多く置いたとき
                    if len(_field[_column]) > self.__num_max_column:
                        for j in range(self.__num_max_column):
                            _earned_cards[_min_player].append(
                                    _field[_column].pop(0)
                                    )
                    break
        if len(rest_cards) > 0: # 出されたカード (rest_cards) が全部処理されるまで再帰的に実行
            self.__line_up_cards_recursive(_field,rest_cards,played_cards,_earned_cards,_func_taking_column)


    def get_field(self): # 場の状況を得る
        self.__field = self.__dealer.field
        self.__update_unknown_cards(list(chain.from_iterable(self.__field)))

    def _min_field_score_column(self):
        _field_score = self.__get_field_score(self.__field)
        return _field_score.index(min(_field_score))

    def __divide_hands(self):
        # need: __most_right_field
        self.__min_field = min(self.__most_right_field)
        self.__lower_hand = []
        self.__upper_hand = []
        for i in self.__my_cards: # __my_cards already sorted
            if i < self.__min_field:
                self.__lower_hand.append(i)
            else:
                self.__upper_hand.append(i)

    def __calc_trap_risk(self): # risk given by positive int (higher: risky)
        __trap_thresh = 4
        __trap_rate = 2
        self.__field_score = self.__get_field_score(self.__field)
        self.__trap_risk = []
        for i in range(self.__num_field):
            if self.__field_score[i] < __trap_thresh:
                self.__trap_risk.append(__trap_rate*(self.__field_score[i]-__trap_thresh))
            else:
                self.__trap_risk.append(0)
        __minIndex = self.__most_right_field.index(min(self.__most_right_field))
        self.__trap_risk[__minIndex] = 0

    def __update_unknown_cards(self,list_of_known_cards):
        for i in list_of_known_cards:
            try:
                self.__unknown_cards.remove(i)
            except ValueError:
                pass

    def __get_field_score(self,_field): # calculate scores of each column
        return [Field.calc_score(_field[i]) for i in range(self.__num_field)]

