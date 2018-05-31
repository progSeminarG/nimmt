#!/usr/local/bin/python3
#coding:UTF-8

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


#継承クラス (ここで基本クラスを継承して、様々な処理を行う) version1.1
#牛の少ない列を戻す，差が1のところに置く

class ShiraiAI(Player):
    def put_card(self):
        self.my_cards.sort()
        fb=200
        print("field",self.dealer.field)
        print("cards",self.my_cards)
        for i in range(4):
    	    for k in range(len(self.my_cards)): #全てのカードと列の最大値との差を計算し1なら返す
    		    if self.my_cards[k]-self.dealer.field[i][len(self.dealer.field[i])-1]==1 and len(self.dealer.field[i])<5 :
    			    chose=self.my_cards[k]
    			    self.my_cards.remove(chose)
    			    return chose
    			    
    	    if len(self.dealer.field[i])==5:
    	        if fb > self.dealer.field[i][len(self.dealer.field[i])-1]:
    	            fb = self.dealer.field[i][len(self.dealer.field[i])-1]
        if self.my_cards[0] > fb:
            t = random.sample(range(len(self.my_cards)),1)[0]
            chose = self.my_cards[t]
            self.my_cards.remove(chose)
            return chose
        else:
            s=0
            while self.my_cards[s] < fb and s<len(self.my_cards)-1:
                s+=1
                print("s:",s)
            
            chose = self.my_cards[s]
            self.my_cards.remove(chose)
            return chose
            

    def taking_column(self):#chose min(caw)
        caw=[0,0,0,0]
        for i in range(4):
            caw[i] = self.ctcaw(self.dealer.field[i])
        col=caw.index(min(caw))
        return col

    def ctcaw(self,cards): #count caw
        _sum = 0
        for i in cards:
            if i == 55:
                _sum += 7
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
