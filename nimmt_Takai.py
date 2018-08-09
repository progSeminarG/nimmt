#! /usr/bin/env python3

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
class TakaiAI(Player):
    def put_card(self):
        i = 0
        while True:
            if len(self.dealer.field[i]) == 5:
                i = i + 1
                if i == 3:
                    _putting_card = max(self.my_cards)
                    break
            elif len(self.dealer.field[i]) == 4:
                for j in range(len(self.my_cards)):
                    if max(self.dealer.field[i]) + 1 == self.my_cards[j]:
                        _putting_card = self.my_cards[j]
                        break
                i = i + 1
                if i == 3:
                    _putting_card = max(self.my_cards)
                    break
            elif len(self.dealer.field[i]) == 3:
                for j in range(len(self.my_cards)):
                    if max(self.dealer.field[i]) + 2 == self.my_cards[j] or max(self.dealer.field[i]) + 1 == self.my_cards[j]:
                        _putting_card = self.my_cards[j]
                        break
                i = i + 1
                if i == 3:
                    _putting_card = max(self.my_cards)
                    break
            elif len(self.dealer.field[i]) == 2:
                for j in range(len(self.my_cards)):
                    if max(self.dealer.field[i]) + 3 == self.my_cards[j] or max(self.dealer.field[i]) + 1 == self.my_cards[j] or max(self.dealer.field[i]) + 2 == self.my_cards[j]:
                        _putting_card = self.my_cards[j]
                        break
                i = i + 1
                if i == 3:
                    _putting_card = max(self.my_cards)
                    break
            elif len(self.dealer.field[i]) == 1:
                for j in range(len(self.my_cards)):
                    if max(self.dealer.field[i]) + 1 == self.my_cards[j] or max(self.dealer.field[i]) + 2 == self.my_cards[j] or max(self.dealer.field[i]) + 3 == self.my_cards[j] or max(self.dealer.field[i]) + 4 == self.my_cards[j]:
                        _putting_card = self.my_cards[j]
                        break
                i = i + 1
                if i == 3:
                    _putting_card = max(self.my_cards)
                    break
                    
        self.my_cards.remove(_putting_card)
        return _putting_card

    def taking_column(self):
        number = []
        n = 5
        m = 10
        o = 11
        for i in range(4):
            number.append(0)
            for j in range(10):
                n = n + 10 * j
                number[i] = self.dealer.field[i].count(n) * 2 + number[i]
            for j in range(10):
                m = m + 10 * j
                number[i] = number[i] + self.dealer.field[i].count(n) * 3
            for j in range(9):
                o = o + 11 * j
                number[i] = number[i] + self.dealer.field[i].count(n) * 5
            number[i] = number[i] + self.dealer.field[i].count(55) * 7
        for i in range(4):
            if number[i] == min(number):
                return i


    def print_field(self):
        _num_field = self.dealer.num_field
        _field = self.dealer.field
        print("current field is:")
        for i in range(_num_field):
            print(_field[i])


