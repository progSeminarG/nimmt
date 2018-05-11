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
class Random(Player):
    def put_card(self):
        _putting_card = random.choice(self.my_cards)
        self.my_cards.remove(_putting_card)
        return _putting_card

    def taking_column(self):
        return random.randrange(4)

    def print_field(self):
        _num_field = self.dealer.num_field
        _field = self.dealer.field
        print("current field is:")
        for i in range(_num_field):
            print(_field[i])


