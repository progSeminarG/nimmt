#!/usr/local/bin/python3

import random
import sys
import copy
from itertools import chain

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
        else:
            self.__category = 'h' # high category
            self.__left_neighbor = _local_sequence[_index-1]
            self.__column = self.__most_right_field.index(self.__left_neighbor) # putting column
            self.__right_neighbor = self.__max_card+1 if _index == self.__num_field else _local_sequence[_index+1]
            _local_sequence = sorted(self.__unknown_cards + [self.__left_neighbor] + [self.__number])
            self.__position = _local_sequence.index(self.__number) \
                - _local_sequence.index(self.__left_neighbor) \
                + self.__num_cards_column[self.__column]
    @property
    def number(self):
        return self.__number #1,..,104
    @property
    def category(self):
        return sefl.__category #'l'ow,'h'igh
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
        _num_try = 100
        self.__score_for_my_cards = []
        for _card in self.__my_cards:
            _score_summed = self.__play_random_pack(_card,_num_try)
            self.__score_for_my_cards.append(_score_summed)
        _min_index = self.__score_for_my_cards.index(min(self.__score_for_my_cards))
        return self.__my_cards.pop(_min_index)

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

