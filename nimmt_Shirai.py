#!/usr/local/bin/python3
#coding:UTF-8

import random
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


#継承クラス (ここで基本クラスを継承して、様々な処理を行う) version1.4
#修正平井さん式初期値設定（メジアン＋を重視）
#基本的に自滅はしないが，戦略的自滅も稀にある
#定数型危険察知（5n+-7）
#未使用カードを用いて一般安全パイ察知

class ShiraiAI(Player):
    def __init__(self):
        self.game_num=0
        self.remains=list(range(1,105))

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

    def memory(self):#出されたカードを記憶する
        if self.game_num==0:
            self.remains=list(range(1,105))
            for i in range(4):
                self.remains.remove(self.dealer.field[i][0])
        else:
            for card in self.dealer.played_cards:
                self.remains.remove(card)
        self.remains.sort()
        print("remains--",self.remains)
        self.game_num+=1
        if len(self.remains) == 104-(self.dealer.num_players*9+4):
            self.game_num=0
            self.remains.clear()


    def cal1(self):
        self.my_cards.sort()
        eval_list=[]
        for i in range(int(len(self.my_cards)/2)+1):#修正平井さん式初期値設定
            eval_list.append(1*i)
        for i in range(len(self.my_cards)-int(len(self.my_cards)/2)-1):
             eval_list.append(len(self.my_cards)-int(len(self.my_cards)/2)+1-i)
        #print("ini--",eval_list)
        fb=200
        fc=200
        s=0
        print("cards:",self.my_cards)
        for i in range(4):
    	    for k in range(len(self.my_cards)): #全てのカードと列の最大値との差を計算し1なら＋100
                if self.my_cards[k]-self.dealer.field[i][len(self.dealer.field[i])-1]==1 and len(self.dealer.field[i])<5 :
    	            eval_list[k]+=100 #PARA
    	    if len(self.dealer.field[i])==5:#5枚ある列の最小値fb計算
    	        if fb > self.dealer.field[i][4]:
    	            fb = self.dealer.field[i][4]
    	    if fc > max(self.dealer.field[i]):#列の末尾fcの最小値
    	        fc=max(self.dealer.field[i])
        while self.my_cards[s]<fb and s<len(self.my_cards)-1:#自滅しないものに＋10
            eval_list[s]+=10 #PARA
            s+=1
        if s == len(self.my_cards)-1 and self.my_cards[s]<fb:
            eval_list[s]+=10
        for i in range(len(self.my_cards)):
            if self.my_cards[i]<fc:
                eval_list[i]=eval_list[i]-10
        danger=[0,0,0,0]
        for i in range(4):#定数型危険察知
            danger[i]=max(self.dealer.field[i])+5*(6-len(self.dealer.field[i]))
            for j in range(len(eval_list)):
                if danger[i]-7 < self.my_cards[j] < danger[i]+7: #PARA
                    eval_list[j]=eval_list[j]-10#PARA
                if danger[i]>104 and max(self.dealer.field[i])<self.my_cards[j]:
                    eval_list[j]=eval_list[j]-10
        print("danger-",danger)
        count=list(range(10))#一般安全パイ察知
        self.memory()
        for k in range(len(self.my_cards)):
            difcol=[0,0,0,0]
            count[k]=0
            for i in range(4):
                difcol[i]=self.my_cards[k]-max(self.dealer.field[i])
                if difcol[i]<0:
                    difcol[i]=200
            #print("difcol-",difcol)
            min_difcol=difcol.index(min(difcol))
            print("mindif-",min(difcol))
            for card in self.remains:
                if max(self.dealer.field[min_difcol])< card <self.my_cards[k]:
                    count[k]=count[k]+1
                if min(difcol)==200:
                    count[k]=200
                    break
            if count[k]< 5-len(self.dealer.field[min_difcol]):
                eval_list[k]=eval_list[k]+100
        return eval_list

    def taking_column(self):#chose min(caw)
        caw=[0,0,0,0]
        mc=[0,0,0,0]
        for i in range(4):
            caw[i] = self.ctcaw(self.dealer.field[i])
        mincaw=min(caw)#min(caw)が複数あったら，末尾が大きい列を選ぶ:より多くの人のスコアを増やしたい
        for i in range(4):
            if caw[i]==mincaw:
                mc[i]=max(self.dealer.field[i])
        col=mc.index(max(mc))
        return col

    def put_card(self):#return max(eval_list)
        eval_list = self.cal1()
        print("list:",eval_list)
        print("~INFORMATION~")
        s=eval_list.index(max(eval_list))
        chose=self.my_cards[s]
        self.my_cards.remove(chose)
        return chose

