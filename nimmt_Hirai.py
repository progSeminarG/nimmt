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
#from nimmtHuman import Human
class Human(Player):
    def put_card(self):
        self.print_field()
        while True:
            print("your hand is:",self.my_cards)
            print("choose a card to play:")
            _putting_card = int(input())
            print("you entered",_putting_card)
            if _putting_card in self.my_cards:
                return self.my_cards.pop(self.my_cards.index(_putting_card))
            else:
                print("choose what you have!")
    def taking_column(self):
        self.print_field()
        while True:
            print("choose a column to take: [0,1,2,3]")
            _taking_column = int(input())
            if _taking_column in [0,1,2,3]:
                return _taking_column
            else:
                print("choose 0 or 1 or 2 or 3!")

    def print_field(self):
        _num_field = self.dealer.num_field
        _field = self.dealer.field
        print("current field is:")
        for i in range(_num_field):
            print(_field[i])
#失点が一番低い列をとる
#６枚目ではない４列のそれぞれの最後尾のカードより大きく値が最も近いカードを選ぶ
#どの列の最後尾のカードよりも持ち札の値が低い時、中間値を出す。(改善の余地あり)
class OldHirai_AI(Player):
    def get_know_dealer(self,dealer_input): # ディーラーのインスタンスを得る
        self.dealer = dealer_input
    def get_hand(self,my_cards_input): # ディーラー側で呼んで、手札を得る
        self.my_cards = my_cards_input
    def rV(self,a,b):
        if(a-b>0):
            return int(-50*math.cos((a-b)/103*math.pi/2))
        else:
            return int(50*math.cos((a-b)/103*math.pi/2))
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
            for i in range(len(self.my_cards)):
                for j in range(len(most_right_field)):
                    value[i][j] = self.rV(self.my_cards[i],most_right_field[j])
                    if len(self.dealer.field[j])==5:
                        value[i][j]=value[i][j]-50
            point = [max(value[i]) for i in range(len(self.my_cards))]
            app = point[0]
            index = 0
            for i in range(len(self.my_cards)):
                if app > self.my_cards[i]:
                    app=self.my_cards[i]
                    index = i
        return self.my_cards.pop(index)
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
#基本戦術
#場にカードが埋まってないときはとにかく一番でかいカードを出すようは一番初めに一番でかいカードを出す。
#場を釣り上げると他のプレイヤーは低い数字のカードを出さざるを得ないのでそれに便乗して低い数字のカードを出す
#体感的に５枚目を出せると一番強い。よって５枚目を頑張って出すことを考える次に四枚目三枚目
#でかいカードはなるべく早めに切った方がいい
#あまりにも小さすぎる数字のカード（例えば１とか２とか）は最後まで持っておいた方がよい
#一番困るのはでかいカードを最後までもっていた場合である。最終的に列を引き取ることになるから損害はかなりでかい。
class Hirai_AI(Player):
    def get_know_dealer(self,dealer_input): # ディーラーのインスタンスを得る
        self.dealer = dealer_input
    def get_hand(self,my_cards_input): # ディーラー側で呼んで、手札を得る
        self.my_cards = my_cards_input
    def most_right_field(self):
        return [
                max(self.dealer.field[i]) for i in range(len(self.dealer.field))
                ]
    def research_column(self,card):
        mrf=self.most_right_field()
        index=0
        approx=mrf[0]
        for i in mrf:
            if i<card and approx<i:
                approx=i
                index=mrf.index(i)
        return index
    def put_card(self): # ディーラー側で呼んで、どのカードを出すか知らせる
        values = [i for i in self.my_cards]
        points = [10,20,30,40,50,-100]
        for card in self.my_cards:
            column=self.research_column(card)
            cardNum = self.my_cards.index(card)
            length=len(self.dealer.field[column])
            values[cardNum]+=points[length]
        return self.my_cards.pop(values.index(max(values)))
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

