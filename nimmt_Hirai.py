#!/usr/local/bin/python3
import  random
import sys
import math
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
#失点が一番低い列をとる
#６枚目ではない４列のそれぞれの最後尾のカードより大きく値が最も近いカードを選ぶ
#どの列の最後尾のカードよりも持ち札の値が低い時、中間値を出す。(改善の余地あり)
class HiraiAI(Player):
    def get_know_dealer(self,dealer_input): # ディーラーのインスタンスを得る
        self.dealer = dealer_input
    def get_hand(self,my_cards_input): # ディーラー側で呼んで、手札を得る
        self.my_cards = my_cards_input
    def put_card(self): # ディーラー側で呼んで、どのカードを出すか知らせる
        
        most_right_field = [
                max(self.dealer.field[i]) for i in range(len(self.dealer.field))
                ]
        min_field = min(most_right_field)
        if min(self.my_cards) < min_field:
            self.my_cards.sort()
            median = math.floor(len(self.my_cards)/2)
            return self.my_cards.pop(median)
        else:
            value = [[0 for j in range(len(most_right_field))] for i in range(len(self.my_cards))]
            '''for i in range(len(self.my_cards)):
                for j in range(len(most_right_field)):
                    value[i][j] = most_right_field[j] - self.my_cards[i] 
                    if len(self.dealer.field[i])==5:
                        value[i][j]=value[i][j]-50'''
            return self.my_cards.pop(0)
    def taking_column(self): # 一番小さい数を出したときにディーラー側で呼んで、どの列を引き取るか知らせる
        min_Caw = 100
        caw = 0
        target = 0
        for column in self.dealer.field:
            caw = 0
            for card in column:
                caw += 1
                if card%11 == 0:
                    caw += 4
                if card%10 == 0:
                    caw += 2
                if card%5 == 0:
                    caw += 1
            if min_Caw>caw:
                target = self.dealer.field.index(column)
                min_Caw = caw
        return target


