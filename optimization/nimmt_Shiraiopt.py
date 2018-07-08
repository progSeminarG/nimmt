#!/usr/local/bin/python3
#coding:UTF-8

import random
import math
import pandas as pd
from pandas import DataFrame,Series
import numpy as np

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
#修正平井式初期値設定
#基本的に自滅はしない(自滅を低評価)が，あまりに希望が持てない時は戦略的自滅を選ぶ
#定数型危険察知（5n+-7，104以上になって列が3枚以上なら低評価）
#未使用カードを用いて一般安全パイ察知

class ShiraiAI(Player):
    def __init__(self,para):
        self.game_num=0
        self.remains=list(range(1,105))
        self.para=para
        print("PARAMETER---",self.para)
        f=open("opt.csv","a")
        f.write("para_list:,"+str(self.para)+"\n")
        f.close()

    def ctcaw(self,cards): #count caw
        _sum = 0
        for i in cards:
            if i == 55:
                _sum += 7
            elif i % 11 == 0:
                _sum += 5
            elif i % 10 == 0:
                _sum += 3
            elif i % 5 == 0:
                _sum += 2
            else:
                _sum += 1
        return _sum

    def cawlist(self):
        cawlist=[0,0,0,0]
        for i in range(4):
            cawlist[i] = self.ctcaw(self.dealer.field[i])
        return cawlist
    
    def memory(self):#出されたカードを記憶し，未使用カードを知る
        if self.game_num==0:
            self.remains=list(range(1,105))
            for i in range(4):
                self.remains.remove(self.dealer.field[i][0])
        else:
            for card in self.dealer.played_cards:
                self.remains.remove(card)
        self.remains.sort()
        self.game_num+=1
        if len(self.remains) == 104-(self.dealer.num_players*9+4):
            self.game_num=0
            self.remains.clear()


    def cal1(self):
        self.my_cards.sort()
        eval_list=list(range(len(self.my_cards)))
        for i in range(len(self.my_cards)):#修正平井式初期値設定2.5
            if self.my_cards[i]>=self.para[0] and i >= self.para[1]*len(self.my_cards):#[0]=70[1]=0.5
                eval_list[i]=self.para[2]*i#[2]=0.1
            else:
                eval_list[i]=self.para[3]*i#[3]=0.5
        #print("ini--",eval_list)
        fb=200
        fc=200
        #print("cards:",self.my_cards)
        for i in range(4):
    	    if len(self.dealer.field[i])==5:#5枚ある列の最小値fb計算
    	        if fb > self.dealer.field[i][4]:
    	            fb = self.dealer.field[i][4]
    	    if fc > max(self.dealer.field[i]):#列の末尾fcの最小値
    	        fc=max(self.dealer.field[i])
        for i in range(len(self.my_cards)):#自滅するものを-10
            if self.my_cards[i]>fb or self.my_cards[i]<fc:
                eval_list[i]-=10
        danger=[0,0,0,0]
        #定数型危険察知
        for i in range(4):
            danger[i]=max(self.dealer.field[i])+self.para[4]*(6-len(self.dealer.field[i]))#[4]=5
            for j in range(len(eval_list)):
                if danger[i]-self.para[5] < self.my_cards[j] < danger[i]+self.para[5]: #[5]=7
                    eval_list[j]-=10#PARA
                if len(self.dealer.field[i])>=3 and danger[i]>104 and max(self.dealer.field[i])<self.my_cards[j]:#3枚以上でdangerが104超えたら全て低評価に
                    eval_list[j]-=10
        #print("danger-",danger)
        #一般安全パイ察知
        count=list(range(len(self.my_cards)))
        mindif=list(range(len(self.my_cards)))
        self.memory()
        caw=self.cawlist()
        for k in range(len(self.my_cards)):
            difcol=[0,0,0,0]
            count[k]=0
            for i in range(4):
                difcol[i]=self.my_cards[k]-max(self.dealer.field[i])
                if difcol[i]<0:
                    difcol[i]=200
            min_difcol=difcol.index(min(difcol))#置かれるであろう列番号
            mindif[k]=min(difcol)
            for card in self.remains:
                if min(difcol)==200:
                    count[k]=200
                    break
                if max(self.dealer.field[min_difcol])< card <self.my_cards[k]:
                    count[k]+=1
            if count[k]<=4-len(self.dealer.field[min_difcol]):
                eval_list[k]+=100+10*(3-count[k])#PARA
                if caw[min_difcol]==min(caw):#こういうときは避ける
                    eval_list[k]-=40
            elif count[k]!=200:
                eval_list[k]+=-count[k]/self.para[6]+self.para[7]#[6]=2[7]=0
        #print("count-",count)
        #戦略的自滅
        #print("caw",caw)
        if max(eval_list)<=self.para[8] and min(caw)<=self.para[9] and len(self.my_cards)>1:#[8]=-6[9]=4
            risk=0
            for card in self.remains:
                if card<min(self.my_cards):
                    risk+=1
            if risk<=len(self.remains)/10:#PARA
                eval_list[0]+=100
        #print("max(ev)",max(eval_list))
        return eval_list

    def taking_column(self):#chose min(caw)
        mc=[0,0,0,0]
        caw=self.cawlist()
        mincaw=min(caw)#min(caw)が複数あったら，末尾が大きい列を選ぶ:より多くの人のスコアを増やしたい
        for i in range(4):
            if caw[i]==mincaw:
                mc[i]=max(self.dealer.field[i])
        col=mc.index(max(mc))
        return col

    def put_card(self):#return max(eval_list)
        eval_list = self.cal1()
        #print("eval_list:",eval_list)
        #print("~INFORMATION~")
        s=eval_list.index(max(eval_list))
        chose=self.my_cards[s]
        self.my_cards.remove(chose)
        return chose


