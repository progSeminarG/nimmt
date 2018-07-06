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
#修正平井式初期値設定
#基本的に自滅はしない(自滅を低評価)が，あまりに希望が持てない時は戦略的自滅を選ぶ
#定数型危険察知（5n+-7，104以上になって列が3枚以上なら低評価）
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
        #print("remains--",self.remains)
        self.game_num+=1
        if len(self.remains) == 104-(self.dealer.num_players*9+4):
            self.game_num=0
            self.remains.clear()


    def cal1(self):
        self.my_cards.sort()
        eval_list=list(range(len(self.my_cards)))
        for i in range(len(self.my_cards)):#修正平井式初期値設定2.5
            if self.my_cards[i]>=70 and i >= 0.5*len(self.my_cards):
                eval_list[i]=0.1*i
            else:
                eval_list[i]=0.5*i
        print("ini--",eval_list)
        fb=200
        fc=200
        print("cards:",self.my_cards)
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
            danger[i]=max(self.dealer.field[i])+5*(6-len(self.dealer.field[i]))
            for j in range(len(eval_list)):
                if danger[i]-7 < self.my_cards[j] < danger[i]+7: #PARA
                    eval_list[j]-=10#PARA
                if len(self.dealer.field[i])>=3 and danger[i]>104 and max(self.dealer.field[i])<self.my_cards[j]:#3枚以上でdangerが104超えたら全て低評価に
                    eval_list[j]-=10
        print("danger-",danger)
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
                eval_list[k]+=-count[k]/2#PARA
        print("count-",count)
        #戦略的自滅
        print("caw",caw)
        if max(eval_list)<=-6 and min(caw)<=4 and len(self.my_cards)>1:#PARA 
            risk=0
            for card in self.remains:
                if card<min(self.my_cards):
                    risk+=1
            if risk<=len(self.remains)/10:#PARA
                eval_list[0]+=100
        print("max(ev)",max(eval_list))
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
        print("eval_list:",eval_list)
        print("~INFORMATION~")
        s=eval_list.index(max(eval_list))
        chose=self.my_cards[s]
        self.my_cards.remove(chose)
        return chose


"""ニムト研究ノート
<試行回数>
ゲームを何回繰り返して統計を取れば，信用に値いするデータが得られるか．経験的には，100回でおおよそ信用できるものとなり，500回でほぼ安定し，1000回で安定する．同じプログラムを1000回，500回，100回，100回でまわしたところ次のようになった．
2.802,22.1%　2.708,22.8%　2.78,20.0%　2.93,19.0%
これをみれば500回で1%，100回で3%程度動くように思えるが，実際には500回で4%くらい動くこともあった．となれば1000回が信用に値するかも微妙であり，より深い考察が必要である．

<初期値>
同評価のカードができた時に何を出すのか．それを決定するために初期値を設定する．
･平井式初期値設定
for i in range(len(self.my_cards)):
    eval_list.append(1*i)
平井さんによって考案された，大きいカードを高評価する初期値設定．シンプルだが成果は非常に大きい．逆平井式や，同評価のカードをランダムに選ぶものも試したが，平井式が圧倒的に有効であった．特にランダムは最悪の結果に終わった．
ゲーム回数50回で平均順位を調べたところ，平井式は3.14，逆平井式は3.36，ランダムは3.66であった．しかし，50回程度の試行回数では偶然に左右されるところがそれなりに大きくなることが経験的に知られている．
平井式と逆平井式を同じゲームに含めて1000回行ったところ，平均順位は平井式が3.386，逆平井式が4.314，勝率は平井式が17.7%，逆平井式が9.9%であった．
･修正平井式初期値設定(modified HIRAI's initial list)
c=0
for i in range(len(self.my_cards)):
    if i<=0.25*len(self.my_cards)-1 or i>=0.75*len(self.my_cards):
        eval_list.append(0)
    else:
        c+=1
        eval_list.append(c)
平井式の欠点として，ゲームの後半に小さいカードが集中するというものがある．よってゲームの後半に威力を発揮するアルゴリズムには，偏った選択によってカードの多様性を奪う平井式は足枷となる．具体例を上げると，未使用カードから安全パイを探るアルゴリズムがそれに相当すると思われる．これを回避するために，平井式に代わる初期値設定の研究が始まった．
両極端を0にし，それ以外を平井式にしている．後半で完全な平井式に移行する．これには，ゲーム初期では同評価値のカードが出現しやすくなり，よってその場合はpython3の仕様に基づきランダムに選ばれるという短所がある．ランダムは最悪の出し方であるという説がある．
・修正平井式2
for i in range(len(self.my_cards)):
    eval_list.append(c)
    if self.my_cards[i]>=70:
        eval_list[i]=0
大きいものを温存するというのが修正平井式の目的であり，それの基準を数値にした．小さいものは普通に避けられるので，処理をなくした．しかしこれには，大きいカードが多い時に温存しすぎるという欠点がある．どこかで平井式に移行しなくてはならない．mHIL,mHIL2を合わせたのが次のmHIL2.5である．
・修正平井式2.5
for i in range(len(self.my_cards)):#修正平井式初期値設定2.5
    if self.my_cards[i]>=70 and i >= 0.7*len(self.my_cards):
        eval_list[i]=0.1*i
    else:
        eval_list[i]=0.5*i
しかしこれは成果があがらなかった．パーセントの微調整が必要なようである．0.5にしたら500回で2.69,23.2%となった．しかし1000回で2.754,19.9%となった

<戦略的自滅>
末尾の最小値よりも小さいカードを出さず，また6枚目になるようなカードを出さない．これは自滅を防ぐ最低限の選択であるが，時に自滅を図った方が後のためになるときもあるように思う．これを戦略的自滅と呼ぶ．
(1) 戦略的自滅を牛が3以下，最大評価値-6以下において，残りのカードに最小カードよりも小さいものがlen(self.remains)/10以下のとき（A）と3以下（B）の2種類で調査した（試行回数500回）．Aでは2.708,22.8%であり，Bでは2.884,17.6%であった．戦略的自滅を図らないとき試行回数1000で2.946,19.4%であった（少しプログラムを変えていたかもしれないが忘れた）．Aを1000回回したところ，2.802,22.1%であった．多少積極的に戦略的自滅を図った方が良いことがわかる．
len(self.remains)/10+2で500回回すと2.776,20.0%となり，len(self.remains)/10-1では2.634,22.4%となった．1000回では後者は2.773,18.5%となった．（min(caw)の列なら-10という仕様も加えた．）
自分のカードと列末尾の間のカード枚数に応じてeval_list[k]-=count[k]/2という低評価をかし，戦略的自滅の基準である牛の数を4として500回回すと2.48,24.6%となった．5としたら2.718,20.4%となった．低評価は(count[k]/2-10),count-15も試した．間のカード枚数が少ないからよいというわけではなく，6枚目に置いてしまう危険性を考慮してのおとであった．しかし上記の低評価が最も良かった．6枚目を避けるようelif count[k]==5-len(self.dealer.field[min_difcol]):eval_list[k]-=10としても悪化した．

"""

