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

class SakuraiAI(Player):

###実装済み機能メモ###
###実装済み機能メモ1:一番牛の少ない列を選ぶ
###実装済み機能メモ2:手札に評価をする。とりあえず小さい数ほど素の評価は高めに設定。
###実装済み機能メモ3:安パイ(長さ4の列の頭が30の時の31みたいな)に高評価をする。逆に、長さ5の時は低評価にする。
###実装済み機能メモ4:場の頭のカードと自分の手札の最小のものとの間の、既プレイカードの割合に生じて配点する。
###実装済み機能メモ5:最初のターンではデカいカードを出したい、けど本当にデカいのは残しておきたい気持ち
###実装済み機能メモ6:小さいカードで列を引き取るときは、ほかの人が先に更新する余地を作ろうとする。

    def __init__(self):
        self.__all_played_cards = set([])#今のゲームで使用済みのカードのセット
        self.__flag = 0#最初のターンだけ0
        self.__eval_my_card = []#i番目の自分の手札の評価、点数

    def __add_played_cards(self):#使用済みのカードをself.__all_played_cardsに格納する。
        if self.__flag == 0:#最初のターンはplayed_cardsが空だから、初期場の四枚だけ保存
            for column in self.dealer.field:
                for card in column:
                    self.__all_played_cards.add(card)
            self.__flag = 1
        else:#played_cardsを追加する。self.__flagを+1する。self.__flagが初期手札枚数よりデカければゲーム終了とみなして初期化する
            for card in self.dealer.played_cards:
                self.__all_played_cards.add(card)
            self.__flag += 1
            if self.__flag >= self.dealer.num_hand:
                self.__flag = 0
                self.__all_played_cards.clear()

    def __check_safety_card(self):#おもに既プレイカードを使って手札を評価する。
        for column in self.dealer.field:
            greater_cards = [card for card in self.my_cards if card > max(column)]#columnの頭より大きい自分の手札
            if len(greater_cards) != 0:
                greater_played = [card for card in self.__all_played_cards if card > max(column) and card < min(greater_cards)]#columnの頭以上greater_cardsの最小未満の既プレイカード
                target_index = self.my_cards.index(min(greater_cards))
                if max(column) + len(greater_played) + 1 == min(greater_cards):#安パイの時の処理
                    self.__eval_my_card[target_index] *= -1
                    if len(column) == self.dealer.num_max_column:
                        self.__eval_my_card[target_index] -= 100
                    else:
                        self.__eval_my_card[target_index] += 100
                else:#列の頭～min(greater_cards)の間のカードの使用率に応じて配点
                    if len(column) != self.dealer.num_max_column:
                        self.__eval_my_card[target_index] += self.__scoring_function_1([min(greater_cards),max(column),len(greater_played)])
                    else:
                        self.__eval_my_card[target_index] -= self.__scoring_function_1([min(greater_cards),max(column),len(greater_played)])

    def __smaller_pickup(self,eval):#evalより評価の高いカードがなければ、数字の小さい手札を対象に採点する
        pickuped_cards = [card for card in self.my_cards if self.__eval_my_card[self.my_cards.index(card)]>eval]
        min_field = min([max(column) for column in self.dealer.field])
        if len(pickuped_cards) == 0:
            pickuped_cards = [card for card in self.my_cards if card<self.dealer.max_card*0.25 and card<min_field]
            if len(pickuped_cards) !=0:
                for card in pickuped_cards:
                    self.__eval_my_card[self.my_cards.index(card)] += self.__scoring_function_2([card,self.dealer.max_card*0.1,eval,self.dealer.max_card*0.001])

    def __scoring_function_0(self,value_list):#カードの数字ごとの素の評価
        turn = value_list[0]
        x = value_list[1]
        a = value_list[2]
        amp_a = value_list[3]
        scl_a = value_list[4]
        b = value_list[5]
        amp_b = value_list[6]
        scl_b = value_list[7]
        if turn == 0:
            return amp_a*math.exp(-scl_a*(x-a)**2) + amp_b*math.exp(-scl_b*(x-b)**2)#最初のターンはなるべく大きい数を出したいけど、めちゃ大きいのは非常時用に取っておきたいっていう気持ち
        return -20*x/self.dealer.max_card + 10 + (1 - 2*random.random())*10

    def __scoring_function_1(self,value_list):#self.__check_safety_cardの、列の頭～min(greater_cards)の間のカードの使用率に応じて配点する関数
        x = value_list[0]
        y = value_list[1]
        z = value_list[2]
        if x - y - 1 < self.dealer.max_card*0.15:
            return -(-40*(x - y - z - 1)/(x - y - 1) + 5)
        else:
            return -40*(x - y - z - 1)/(x - y - 1) + 20

    def __scoring_function_2(self,value_list):#__smaller_pickupの中の評価　小さいやつを出すけど、あわよくばほかの人に更新してもらいたい感じの関数
        x = value_list[0]
        y = value_list[1]
        amp = value_list[2]
        scl = value_list[3]
        return amp*math.exp(-scl*(x-y)**2) + amp*0.3*math.exp(-scl*0.1*(x-y*0.5)**2)

    def put_card(self):
        self.__eval_my_card = [self.__scoring_function_0([self.__flag,i,self.dealer.max_card*0.9,100,0.01,self.dealer.max_card*1.0,-100,0.01]) for i in self.my_cards]#素の評価をする
        self.__add_played_cards()
        self.__check_safety_card()
        self.__smaller_pickup(30)

        a = self.__eval_my_card.index(max(self.__eval_my_card))#一番評価の高いカードを出す
        self.__eval_my_card.pop(a)
        return self.my_cards.pop(a)

    def taking_column(self): # 一番小さい数を出したときにディーラー側で呼んで、どの列を引き取るか知らせる
        return self.__scoring_column()

    def __scoring_column(self):#一番牛の少ない列番号を返す
        min_Caw = -1
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
            if min_Caw>caw or min_Caw<0:
                target = self.dealer.field.index(column)
                min_Caw = caw
        return target
