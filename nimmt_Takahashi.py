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
        print("insert prob:",self.__get_insert_risk())
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

    def __get_insert_risk(self):
        _insert_risk_list = []
        _insert_prob = []
        _score_of_lines = []
        _num_each_cards = len(self.__my_cards_inst) # number of cards for each hand
        _num_players = self.__num_players -1 # number of players except myself
        _num_all_cards = len(self.__unknown_cards) # number of cards unknown
        _insert_prob_list = []
        for card in self.__my_cards_inst:
            if card.category is 'h':
                print("prior_cards:",card.prior_cards) # possible inserting cards
                _num_keycards = len(card.prior_cards) # number of keycards
                _num_pick_cards = card.num_space
                print("#:",card.number)
                print("N:",_num_all_cards)
                print("n:",_num_each_cards)
                print("s:",_num_players)
                print("m:",_num_keycards)
                print("l:",_num_pick_cards)
# include following for implementation
#                _insert_prob_list.append(self.__calc_probability(_num_all_cards,_num_each_cards,_num_players,_num_keycards,_num_pick_cards))
#        print("insert_prob_list=",_insert_prob_list)
#        return _insert_prob_list

## test 1
#        _current_list = self.__make_tuple(4,4)
#        _list_of_current_list = [copy.deepcopy(_current_list)]
#        print("_list_of_current_list0:",_list_of_current_list)
#        self.__break_tuple(_list_of_current_list,_current_list,4,3,4)
#        print("_list_of_current_list1:",_list_of_current_list)
#        sys.exit(1)

# test 2
        _N = 90 #90 # 30 # 90 # total number of cards
        _n = 10 #10 #  3 # 10 # number of cards one hold
        _s =  8 # 8 #  4 # 8  # number of players
        _m = 76 # 3 # 15 # 43 # number of key cards
        _l =  4 # 4 #  4 # 4  # number of people who has keycard
        print("N:",_N)
        print("n:",_n)
        print("s:",_s)
        print("m:",_m)
        print("l:",_l)
        print("probability:",self.__calc_probability(_N,_n,_s,_m,_l))
        sys.exit(1)

## test 3
#        _current_list = [(9,3),(8,4)]
#        self.__break_tuple_core(_current_list,59,7)
#        sys.exit(1)

    # calc probability
    # _N: total number of cards
    # _n: number of cards each player has
    # _s: number of players
    # _m: total number of key cards (all has to be distributed)
    # _l: number of people who has keycard (no more or less)
    def __calc_probability(self,_N,_n,_s,_m,_l):
        if _m < _l: # number of keycards is smaller than number of people to be distributed
            return 0.0
        if _N < _n*_s  or _s < _l:
            print("ERROR: wrong combination in __get_probability2")
            sys.exit(1)
        def perm(_n,_r):
            return factorial(_n)/factorial(_n-_r) #comb(_n,_r)*factorial(_r)
        def prod(_n,_s,_list_of_combination):
            _prod = 1
            _ss = _s
            for _num_cards,_num_player in _list_of_combination:
                _prod *= comb(_n,_num_cards)**_num_player
                _prod *= comb(_ss,_num_player)
                _ss -= _num_player
            return _prod
        _probability = 0.0
        _permN = perm(_N,_n*_s)
        print("_mp range= [",max(_l,_n*_s-_N+_m),":",min(_m,_n*_s),"]")
        print("_lp range= [",_l,":",min(_m,_s),"]")
        for _mp in range(max(_l,_n*_s-_N+_m),min(_m,_n*_s)+1): # number of distributing key cards
            for _lp in range(_l,min(_mp,_s)+1): # number of people 
                print("calc probability of (_mp,_lp)=(",_mp,",",_lp,")->(",_mp-_lp,",",_lp,")")
                _list_of_list_of_pattern = self.__create_pattern(_n,_mp,_lp)
                _prob_m_l = 0.0
                for _list_of_pattern in _list_of_list_of_pattern:
#                    print("_list_of_pattern:",_list_of_pattern)
                    _prod = prod(_n,_s,_list_of_pattern)
                    _perm1 = perm(_m,_mp)
                    _perm2 = perm(_N-_m,_n*_s-_mp)
                    _prob = _prod * _perm1 * _perm2 / _permN
#                    print("_prod:",_prod)
#                    print("_pem1:",_perm1)
#                    print("_pem2:",_perm2)
#                    print("_permN:",_permN)
#                    print("probablity:",_prob)
                    _prob_m_l += _prob
                _probability += _prob_m_l
#                print("probability of (_mp,_lp)=(",_mp,",",_lp,"), P=",_prob_m_l)
#                print(_list_of_list_of_pattern)
        return _probability

    ### create all possible pattern for
    # _n:  maximum number of cards one has
    # _mp: number of keycards to hand out
    # _lp: maximum numbef of people who has keycards
    def __create_pattern(self,_n,_mp,_lp):
        _first_list = self.__make_tuple(_mp-_lp,min(_mp-_lp,_n-1))
        _list_of_list_of_pattern = [copy.deepcopy(_first_list)]
        if _first_list != []:
            self.__break_tuple(_list_of_list_of_pattern,copy.deepcopy(_first_list),
                    _mp-_lp, # number of keycards in small matrix
                    _n-1, # maximum number of cards one has in small matrix
                    _lp)
            # add 1 to all num_keycards to recover original size
        self.__shift_keycard_num(_list_of_list_of_pattern,_lp)
        return _list_of_list_of_pattern

    # add 1 to all x in tuple (x,y) to recover original size
    def __shift_keycard_num(self,_list_of_list_of_tuple,_lp):
        for k in range(len(_list_of_list_of_tuple)):
            if _list_of_list_of_tuple[k] == []:
                _list_of_list_of_tuple[k] = [(0,_lp)]
            for i in range(len(_list_of_list_of_tuple[k])):
                _list_of_list_of_tuple[k][i] = (_list_of_list_of_tuple[k][i][0]+1,_list_of_list_of_tuple[k][i][1])
            _num_people = self.__count_num_player(_list_of_list_of_tuple[k])
            if _num_people < _lp:
                _list_of_list_of_tuple[k].append((1,_lp-_num_people))

    # create list of list of tuples with total _num numbers of cards to distribute
    # _mp: total number of keycards
    # _n: number of cards one can hold
    # _lp: max number of people to distribute keycards
    def __break_tuple(self,_list_of_list_of_tuple,_current_list,_mp,_n,_lp):
        _numOfSet = 0
        while _current_list != [(1,_mp)]:
            if _numOfSet != len(_list_of_list_of_tuple):
                _numOfSet = len(_list_of_list_of_tuple)
#                print("_numOfSet:",len(_list_of_list_of_tuple),
#                        "(_mp,_lp)=",(_mp,_lp),",",
#                        (self.__sum_tuple(_current_list),self.__count_num_player(_current_list)),
#                        "_current_list:",_current_list)
            self.__break_tuple_core(_current_list,_mp,_lp)
            if _current_list != [(1,_mp)]:
                print("accepted _current_list",_current_list,_list_of_list_of_tuple)
                _list_of_list_of_tuple.append(copy.deepcopy(_current_list))

    # seach from last tuple and decrease _num_people
    #   if _num_people == 1, go to upper tuple and decrease _num_people
    #   if _num_keycards == 1, return []
    def __break_tuple_core(self,_current_list,_mp,_lp):
        # from bottom tuple check if breaking possible
        for (_num_keycards,_num_people) in _current_list[::-1]:
            del _current_list[-1]
            if _num_keycards > 1: # if _num_keycards == 1, it can't break. go to next upper tuple
                if _num_people > 1: # if _num_people > 1, it can be decreased
                    _current_list.append((_num_keycards,_num_people-1)) # add decreased tuple
                _rest_mp = _mp - self.__sum_tuple(_current_list) # calculate _mp for lower tuple
                _current_list += self.__make_tuple(_rest_mp,_num_keycards-1) # fill lower tuples
                if self.__count_num_player(_current_list) > _lp: # num_player exceeds criterion _lp
                    self.__skip_tuple(_current_list,_mp,_lp)
                return

    # create a list of tuple
    #   witch all needed cards are distributed
    # _total: _n * _num_players
    # _num_keycards_max: max number of key card (always _num_keycards_max <= _n)
    # _num_people_max: max of number of people (always _num_people_max <= _s)
    def __make_tuple(self,_total,_num_keycards_max): #,_num_people_max):
        if _total == 0: return []
        _tuple_list = []
#        print("__make_tuple",_num_keycards_max)
        for _num_keycard in range(_num_keycards_max,0,-1):
#            print(_num_keycard)
            _num_people = int(_total / _num_keycard)
            if _num_people > 0:
                _total -= _num_keycard * _num_people
                _tuple_list.append((_num_keycard,_num_people))
                if _total == 0:
                    return _tuple_list

    # return max number of player for _irank-th tuple
    # if num_player in tuple exceed, decreasing num_player cannot help sum(num_player) <= _lp
    def __num_max_player_local(self,_tuple_list,_mp,_irank):
        _sum = 0
        for _i in range(_irank):
            _sum += _tuple_list[_i][0]*_tuple_list[_i][1]
        return int((_mp - _sum)/_tuple_list[_irank][0])

#    # check at where the number of poeple exceed _lp
#    #   and skip those
#    # this return _current_list with appropriate list of tuple
#    #    which satisfies criterion num_people <= _lp
#    #    or if it does not exist, return (_mp,1)
#    # _current_list: input list
#    # _mp: number of keycards
#    # _lp: max number of people who has keycards
#    def __skip_tuple(self,_current_list,_mp,_lp):
##        print("skip1",_current_list,_mp,_lp,self.__sum_tuple(_current_list),self.__count_num_player(_current_list))
#        _num_player = 0
#        for _irank in range(len(_current_list)):
#            _num_player += _current_list[_irank][1]
#            if _num_player > _lp:
##                print("num_player exceed. irank=",_irank)
#                if _irank > 0:
#                    self.__dec_num_player(_current_list,_mp,_irank)
#                    if self.__count_num_player(_current_list) > _lp:
##                        print("skip2")
#                        self.__skip_tuple(_current_list,_mp,_lp)
#                else:
#                    # return [(1,_mp)] --- id unchanged by indirect substitution
#                    del _current_list[:]
#                    _current_list += self.__make_tuple(_mp,1)
#                return
    # non recursive version
    # check at where the number of poeple exceed _lp
    #   and skip those
    # this return _current_list with appropriate list of tuple
    #    which satisfies criterion num_people <= _lp
    #    or if it does not exist, return (_mp,1)
    # _current_list: input list
    # _mp: number of keycards
    # _lp: max number of people who has keycards
    def __skip_tuple(self,_current_list,_mp,_lp):
        while self.__count_num_player(_current_list) > _lp:
            _num_player = 0
            for _irank in range(len(_current_list)):
                _num_player += _current_list[_irank][1]
                if _num_player > _lp:
                    if _irank > 0:
                        self.__dec_num_player(_current_list,_mp,_irank)
                        if self.__count_num_player(_current_list) > _lp:
                            break
                        else:
                            return
                    else:
                        del _current_list[:]
                        _current_list += self.__make_tuple(_mp,1)
                        return

#    # revised version of above
#    # check at where the number of poeple exceed _lp
#    #   and skip those
#    # this return _current_list with appropriate list of tuple
#    #    which satisfies criterion num_people <= _lp
#    #    or if it does not exist, return (_mp,1)
#    # _current_list: input list
#    # _mp: number of keycards
#    # _lp: max number of people who has keycards
#    def __skip_tuple(self,_current_list,_mp,_lp):
##        print("skip1",_current_list,_mp,_lp,self.__sum_tuple(_current_list),self.__count_num_player(_current_list))
#        _num_player = self.__count_num_player(_current_list)
#        if _num_player > _lp:
##            print("num_player exceeded:", _num_player, _lp)
#            del _current_list[:]
#            _current_list += self.__make_tuple(_mp,1)
        
#    # decrese number of player by one at _irank-th position
#    #   _current_list is updated
#    # if _irank is not given, the last tuple will be the target
#    # if number of keycard at _irank is 1, delete last tuple and return
#    # if number of player at _irank is 1, decrese number of player in former rank
#    # the rest of list is filled by appropriate tuple by __make_tuple
#    #    __make_tuple takes total number of keycards and max number of keycards
#    # it does not check if number of people is small enough
##    sys.setrecursionlimit(10000)
#    def __dec_num_player(self,_current_list,_mp,_irank=-1,num_rec=0):
#        print("@decnumplayer:",_current_list,"irank:",_irank,"num_rec:",num_rec)
#        if num_rec > 100:
#            print("error recursion")
#            sys.exit(1)
#        if _current_list == [(1,_mp)]: return
#        (_num_keycard,_num_player) = _current_list[_irank]
#        del _current_list[_irank:] # delete tuples _irank to end
#        if _num_keycard == 1:
#            print("num_rec=",num_rec)
#            self.__dec_num_player(_current_list,_mp,num_rec=num_rec+1)
#            return
#        if _num_player == 1:
#            if _current_list != []:
#                print("num_rec=",num_rec)
#                self.__dec_num_player(_current_list,_mp,len(_current_list)-1,num_rec=num_rec+1)
#            else:
#                _current_list += self.__make_tuple(_mp,_num_keycard-1)
#                print("num_rec=",num_rec)
#                self.__dec_num_player(_current_list,_mp,num_rec=num_rec+1)
#            return
#        else:
#            _current_list.append((_num_keycard,_num_player-1))
#            _rest_mp = _mp - self.__sum_tuple(_current_list)
#            _current_list += self.__make_tuple(_rest_mp,_num_keycard-1)
#            return

    # non recursive version
    # decrese number of player by one at _irank-th position
    #   _current_list is updated
    # if _irank is not given, the last tuple will be the target
    # if number of keycard at _irank is 1, delete last tuple and return
    # if number of player at _irank is 1, decrese number of player in former rank
    # the rest of list is filled by appropriate tuple by __make_tuple
    #    __make_tuple takes total number of keycards and max number of keycards
    # it does not check if number of people is small enough
#    sys.setrecursionlimit(10000)
    def __dec_num_player(self,_current_list,_mp,_irank=-1,num_rec=0):
        while _current_list != [(1,_mp)]:
            (_num_keycard,_num_player) = _current_list[_irank]
            del _current_list[_irank:] # delete tuples _irank to end

            if _num_keycard == 1:
                _irank = -1
                continue

            if _num_player == 1:
                if _current_list != []:
                    _irank = len(_current_list)-1
                    continue
                else:
                    _current_list += self.__make_tuple(_mp,_num_keycard-1)
                    _irank = -1
                    continue
            else:
                _current_list.append((_num_keycard,_num_player-1))
                _rest_mp = _mp - self.__sum_tuple(_current_list)
                _current_list += self.__make_tuple(_rest_mp,_num_keycard-1)
                return

    # decrese number of player by one at _irank-th position
    #   _current_list is updated
    # if _irank is not given, the last tuple will be the target
    # if number of player at _irank is 1, create _num_keycard[_irank]-1 tuple or decrese _num_keycard[_irank-1] if _num_keycard[_irank-1] = _num_keycard[_irank]-1
    # the rest of list is filled by appropriate tuple by __make_tuple
    def __dec_num_player_soft(self,_current_list,_mp,_irank=-1):
        (_num_keycard,_num_player) = _current_list[_irank]
        del _current_list[_irank:]
        if _num_keycard == 1:
            print("ERROR: pointed _irank is wrong")
            return
        if _num_player == 1: # case that cannot decrese num_player
            if _current_list != []: # case that _irank > 0
                if _num_keycard == _current_list[-1][1]-1: # num_keycards are neighbors for _irank-1 and _irank
                    self.__dec_num_player_soft(_current_list,_mp)
                else:
                    _rest_mp = _mp - self.__sum_tuple(_current_list)
                    _current_list += self.__make_tuple(_rest_mp,_num_keycard+1)
            else:
                _current_list += self.__make_tuple(_mp,_num_keycard-1)
                self.__dec_num_player(_current_list,_mp)
        else:
            _current_list.append((_num_keycard,_num_player-1))
            _rest_mp = _mp - self.__sum_tuple(_current_list)
            print("@dec_num_player",_rest_mp,_num_keycard-1)
            _current_list += self.__make_tuple(_rest_mp,_num_keycard-1)

    def __count_num_player(self,_list_of_tuple):
        _sum = 0
        for _tuple in _list_of_tuple:
            _sum += _tuple[1]
        return _sum

    # calculate total number of cards
    def __sum_tuple(self,_list_of_tuple):
        _sum = 0
        for _tuple in _list_of_tuple:
            _sum += _tuple[0]*_tuple[1]
        return _sum

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
        self._line_up_cards(_ged_field,
                _ged_played_cards,
                _ged_earned_cards,
                self._min_field_score_column)
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

