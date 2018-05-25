import random
import sys
import math

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



class KawadaAI(Player):
    def get_know_dealer(self,dealer_input): # ディーラーのインスタンスを得る
        self.dealer = dealer_input
    def get_hand(self,my_cards_input): # ディーラー側で呼んで、手札を得る
        self.my_cards = my_cards_input
        self.my_cards = sorted(self.my_cards)
    def put_card(self): # ディーラー側で呼んで、どのカードを出すか知らせる
        field_edge=[]#fieldの端の数字を並べる（ただし5枚以上の場は無視）
        for i in range(4):
            if len(self.dealer.field[i])<5:
                field_edge.append(self.dealer.field[i][len(self.dealer.field[i])-1])
        ret=random.randint(0,len(self.my_cards)-1)#とりあえずランダムである条件を満たせばアルゴリズムに従う
        for i in range (0,5):
            if self.my_cards[ret]%5==0:
                ret=random.randint(0,len(self.my_cards)-1)
        gap=150
        while len(field_edge)!=0 and gap==150:#おける場所があればfieldのある数より大きい一番小さい数を出す
            picfield_num=random.randint(0,len(field_edge)-1)
            pic=field_edge[picfield_num]#出すフィールドをランダムに決める
            field_edge.pop(picfield_num)#対象のフィールドの数をリストから削除し繰り返しを減らす
            for i in range (len(self.my_cards)):#ローラ―作戦で段々に対象に近い数に更新していく
                if self.my_cards[i]>pic:
                    if self.my_cards[i]-pic<gap:
                        gap=self.my_cards[i]-pic
                        ret=i#この時点でpicを超えた数字を持っていなければgapが初期設定150になるので繰り返し条件へ（提出可能フィールドリストがあれば）
        root=random.randint(1,100)
        #not_five_check=0
        sanbuncheck=0
        if len(field_edge)==0 and gap==150 and root<=70:#どこも出せなければ一番低い数を出す なるべく５の倍数以外
            #not_five_point=0
            #for i in range(len(self.my_cards)):
            partbox=[2,2,2,2,3,3,3,4,4,5]#確率操作で選ぶ帯の確率の重さ変動partboxにて調整可
            smy_cards=sorted(self.my_cards)
            piccard=smy_cards[int(len(self.my_cards)/partbox[random.randint(0,len(partbox)-1)])]
            subpiccard=smy_cards[int(len(self.my_cards)/partbox[random.randint(0,len(partbox)-1)])]#サブ数を控えてなるべく5の倍数避けるが2回だめならあきらめてランダムに投げる

            for i in range(0,len(self.my_cards)):
                if self.my_cards[i]==piccard and piccard%5!=0:
                    ret=i
                    sanbuncheck=1
            for i in range(0,len(self.my_cards)):
                if sanbuncheck==0 and self.my_cards[i]==subpiccard and subpiccard%5!=0:
                    ret=i


                '''if self.my_cards[i]<self.my_cards[not_five_point] and self.my_cards[i]%5!=0:#最低値を返す→廃止
                    ret=i
                    not_five_check=1
        if not_five_check!=1 and self.my_cards[0]%5!=0 and root<=70:
            for i in range(len(self.my_cards)):
                if self.my_cards[i]<self.my_cards[ret]:
                    ret=i'''


        return self.my_cards.pop(ret)
    def taking_column(self): # 一番小さい数を出したときにディーラー側で呼んで、どの列を引き取るか知らせる
        fieldk=0
        for fieldi in range (3):#フィールドの各枚数を順に比較し枚数が少ない方を取る
                if len(self.dealer.field[fieldi])<len(self.dealer.field[fieldk]):
                    fieldk=fieldi
                elif len(self.dealer.field[fieldi])==len(self.dealer.field[fieldk]):#枚数が同じときは5の倍数が少ない方を取る
                    key_cards_counts=[0,0,0,0]
                    for i in range(4):
                        for k in range(len(self.dealer.field[i])):
                            if self.dealer.field[i][k]%5==0:
                                key_cards_counts[i]=key_cards_counts[i]+1
                    if key_cards_counts[fieldi]<key_cards_counts[fieldk]:
                        fieldk=fieldi
        return fieldk
    def get_field(self): # 場の状況を得る
        self.field = self.dealer.field


'''
なるべく安全な時に5の倍数を使い切りたい、
小さい数字は後半不利になるのでなるべく減らしておきたいが、
減りすぎると有利な選択肢が狭まってしまうのである程度の割合で残しておきたい
現状安パイはフィールドのうちランダムに選んで一番近い値を返すが
安全じゃないときに９割小さい数字、1割ランダム（5の倍数をなるべく避けたいので5回試行）
この確率をどう調整するかでも大きく変わると思う。'''


'''
安全じゃないときに一番小さいのを出してしまうので危険＝確実にアウト
になっているので、一番小さい数字はランダムにまかせて、ある程度の帯の数字を返すように変更したい
'''
