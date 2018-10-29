import random
import sys
import math
from operator import itemgetter


class Player(object):
    ### 必須メソッド (4 つ) ###
    def get_know_dealer(self, dealer_input):  # ディーラーのインスタンスを得る
        self.dealer = dealer_input

    def get_hand(self, my_cards_input):  # ディーラー側で呼んで、手札を得る
        self.my_cards = my_cards_input

    def put_card(self):  # ディーラー側で呼んで、どのカードを出すか知らせる
        return self.my_cards.pop(0)

    def taking_column(self):  # 一番小さい数を出したときにディーラー側で呼んで、どの列を引き取るか知らせる
        return 0


class KawadaAI(Player):
    def __init__(self):
        self.all_cards_list = [0]+[1]*104

    # number of card's cost
    def usi_num_of_card(self, card):
        if card % 55 == 0:
            return 7
        elif card % 11 == 0:
            return 5
        elif card % 10 == 0:
            return 3
        elif card % 5 == 0:
            return 2
        else:
            return 1

    # number of lane's cost
    def usi_num_of_list(self, cardslist):
        score = 0
        for i in range(len(cardslist)):
            score = score+self.usi_num_of_card(cardslist[i])
        return score

    # convert date of field
    def convert_field_date(self, num):  # [列の端,枚数,列の牛頭,元の列,幅]*4
        self.converted_field = [0]*4
        for i in range(len(self.dealer.field)):
            j = len(self.dealer.field[i])
            score = self.usi_num_of_list(self.dealer.field[i])
            self.converted_field[i] = [self.dealer.field[i][j-1], j, score, i]
        self.converted_field.sort(key=itemgetter(1))
        lengths = [self.converted_field[0][0], self.converted_field[1][0]-self.converted_field[0][0],
                  self.converted_field[2][0]-self.converted_field[1][0], self.converted_field[3][0]-self.converted_field[2][0], 104-self.converted_field[3][0]]
        for i in range(4):
            sum = 0
            if i == 3:
                up = 105
            else:
                up = self.converted_field[i+1][0]+1
            down = self.converted_field[i][0]+1
            for j in range(down, up):
                sum = sum + self.all_cards_list[j]
            self.converted_field[i].append(lengths[i+1])
            self.converted_field[i].append(sum)
        self.converted_field.sort(key=itemgetter(num))

    # renew all cards list
    def all_cards_kosin(self):  # すべてのカードのリストから既出のカードを削除
        if len(self.my_cards) == 10:
            self.all_cards_list = [0]+[1]*104
            for i in range(0, len(self.my_cards)):
                self.all_cards_list[self.my_cards[i]] = 0
            for i in range(0, len(self.dealer.field)):
                for j in range(0, len(self.dealer.field[i])):
                    self.all_cards_list[self.dealer.field[i][j]] = 0
        else:
            for i in range(0, self.dealer.num_players):
                self.all_cards_list[self.dealer.played_cards[i]] = 0

    # caliculate risk of my cards
    def cards_risk(self):  # 既出のカードから手持ちのカードの安全性を評価
        self.convert_field_date(0)
        risks = [0]*len(self.my_cards)
        self.my_cards_field = [0]*len(self.my_cards)
        for i in range(0, len(self.my_cards)):  # 手持ちのカードだけ試行
            for j in range(4):  # 対象のfieldを探す
                if self.my_cards[i] > self.converted_field[j][0]:
                    self.my_cards_field[i] = j+1
            if self.my_cards_field[i] == 0:
                risks[i] = 1000
            else:
                sum = self.converted_field[self.my_cards_field[i]-1][1]
                for j in range(self.my_cards_field[i], self.my_cards[i]):
                    sum = sum+self.all_cards_list[j]
                risks[i] = sum-4
        return risks

    def get_know_dealer(self, dealer_input):  # ディーラーのインスタンスを得る
        self.dealer = dealer_input

    def get_hand(self, my_cards_input):  # ディーラー側で呼んで、手札を得る
        self.my_cards = my_cards_input
        self.my_cards = sorted(self.my_cards)
        print("kawada", self.my_cards)

    def put_card(self):  # ディーラー側で呼んで、どのカードを出すか知らせる
        self.all_cards_kosin()
        risks = self.cards_risk()
        ret = random.randint(0,len(self.my_cards)-1)
        for i in range(0, len(self.my_cards)):
            if self.usi_num_of_card(self.my_cards[i]) == 1:
                ret = i
        safety_ans = False
        for i in range(len(self.my_cards)):
            if risks[len(self.my_cards)-i-1] <= 0:
                if safety_ans is True:
                    if risks[ret] >= risks[len(self.my_cards)-i-1]:
                        ret = len(self.my_cards)-i-1
                else:
                    ret = len(self.my_cards)-i-1
                    safety_ans = True
        if safety_ans is False:
            self.convert_field_date(0)
            for i in range(len(self.my_cards)):
                if self.my_cards_field[i] != 0 and self.converted_field[self.my_cards_field[i]-1][1] == 5:
                    if risks[i] >= 20 and risks[i] <= 999:
                        ret =i
                        safety_ans = True
        for i in range(len(self.my_cards)):
            if risks[len(self.my_cards)-1-i] == 1000 and safety_ans == False and self.usi_num_of_card(self.my_cards[len(self.my_cards)-1-i]) == 1:
                ret = len(self.my_cards)-1-i

        '''
        if len(self.my_cards) == 10:
            self.convert_field_date(0)
            lengths = [self.converted_field[0][0], self.converted_field[1][0]-self.converted_field[0][0],
                      self.converted_field[2][0]-self.converted_field[1][0], self.converted_field[3][0]-self.converted_field[2][0], 104-self.converted_field[3][0]]
            main = 0
            sub = 0
            length = 100
            firstresp = False
            for i in range(5):
                if lengths[i] < length:
                    length = lengths[i]
                    sub = main
                    main = i
            for i in range(10):
                if self.my_cards_field[9-i] == main:
                    ret = 9-i
                    firstresp = True
            if firstresp == False:
                for i in range(10):
                    if self.my_cards_field[9-i] == sub:
                        ret = 9-i'''

        return self.my_cards.pop(ret)

    def taking_column(self):  # 一番小さい数を出したときにディーラー側で呼んで、どの列を引き取るか知らせる
        self.convert_field_date(2)
        ret=self.converted_field[0][3]
        return ret

    def get_field(self):  # 場の状況を得る
        self.field = self.dealer.field

'''
＜仕様の変更＞....2018/10/05
all_cards_listの作成後、各手持ちカードのriskを数値化
安全なカードをだす
無ければ7枚目を狙う
それもなければfieldより小さい大きいカードで2枚目を狙う
を追加
'''
