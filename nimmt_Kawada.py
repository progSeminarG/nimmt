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

    def all_cards_kosin(self):  # すべてのカードのリストから既出のカードを削除
        if len(self.my_cards) == 10:
            for i in range(0, len(self.my_cards)):
                self.all_cards_list[self.my_cards[i]] = 0
            for i in range(0, len(self.dealer.field)):
                for j in range(0, len(self.dealer.field[i])):
                    self.all_cards_list[self.dealer.field[i][j]] = 0
        else:
            for i in range(0, self.dealer.num_players):
                self.all_cards_list[self.dealer.played_cards[i]] = 0

    def cards_risk(self):  # 既出のカードから手持ちのカードの安全性を評価
        risks = [0]*len(self.my_cards)
        my_cards_field = [0]*len(self.my_cards)
        fields_risk = []
        for i in range(0, len(self.dealer.field)):
            number = len(self.dealer.field[i])
            fields_risk.append([self.dealer.field[i][number-1], 6-number-2])
        fields_risk.sort(key=itemgetter(0))
        for i in range(0, len(self.my_cards)):  # 手持ちのカードだけ試行
            for j in range(0, len(self.dealer.field)-1):  # 対象のfieldを探す
                if self.my_cards[i] > fields_risk[j][0]:
                    my_cards_field[i] = j+1
            if my_cards_field[i] == 0:
                risks[i] = 100
            else:
                sum = 0
                for j in range(my_cards_field[i], self.my_cards[i]):
                    sum = sum+self.all_cards_list[j]
                risks[i] = sum-fields_risk[my_cards_field[i]-1][1]
        return risks

    def get_know_dealer(self, dealer_input):  # ディーラーのインスタンスを得る
        self.dealer = dealer_input

    def get_hand(self, my_cards_input):  # ディーラー側で呼んで、手札を得る
        self.my_cards = my_cards_input
        self.my_cards = sorted(self.my_cards)
        print("kawada", self.my_cards)

    def put_card(self):  # ディーラー側で呼んで、どのカードを出すか知らせる
        if len(self.my_cards) == 10:
            self.all_cards_list = [0]+[1]*104
        self.all_cards_kosin()
        risks = self.cards_risk()
        field_edge = []  # fieldの端の数字を並べる（ただし5枚以上の場は無視）
        for i in range(4):
            if len(self.dealer.field[i]) < 5:
                field_edge.append(self.dealer.field[i][len(self.dealer.field[i])-1])
        ret = random.randint(0, len(self.my_cards)-1)  # とりあえずランダムである条件を満たせばアルゴリズムに従う
        for i in range(0, 5):
            if self.my_cards[ret] % 5 == 0:
                ret = random.randint(0, len(self.my_cards)-1)
        gap = 150
        while len(field_edge) != 0 and gap == 150:  # おける場所があればfieldのある数より大きい一番小さい数を出す
            picfield_num = random.randint(0, len(field_edge)-1)
            pic = field_edge[picfield_num]  # 出すフィールドをランダムに決める
            field_edge.pop(picfield_num)  # 対象のフィールドの数をリストから削除し繰り返しを減らす
            for i in range(len(self.my_cards)):  # ローラ―作戦で段々に対象に近い数に更新していく
                if self.my_cards[i] > pic:
                    if self.my_cards[i]-pic < gap:
                        gap = self.my_cards[i]-pic
                        ret = i  # この時点でpicを超えた数字を持っていなければgapが初期設定150になるので繰り返し条件へ（提出可能フィールドリストがあれば）
        root = random.randint(1, 100)
        # not_five_check=0
        sanbuncheck = 0
        if len(field_edge) == 0 and gap == 150 and root <= 70:  # どこも出せなければ一番低い数を出す なるべく５の倍数以外
            # not_five_point=0
            # for i in range(len(self.my_cards)):
            partbox = [2, 2, 2, 2, 3, 3, 3, 4, 4, 5]
            # 確率操作で選ぶ帯の確率の重さ変動partboxにて調整可
            smy_cards = sorted(self.my_cards)
            piccard = smy_cards[int(len(self.my_cards)/partbox[random.randint(0, len(partbox)-1)])]
            subpiccard = smy_cards[int(len(self.my_cards)/partbox[random.randint(0, len(partbox)-1)])]
            # サブ数を控えてなるべく5の倍数避けるが2回だめならあきらめてランダムに投げる

            for i in range(0, len(self.my_cards)):
                if self.my_cards[i] == piccard and piccard % 5 != 0:
                    ret = i
                    sanbuncheck = 1
            for i in range(0, len(self.my_cards)):
                if sanbuncheck == 0 and self.my_cards[i] == subpiccard and subpiccard % 5 != 0:
                    ret = i
        for i in range(0, len(self.my_cards)):
            if risks[i] == 100:
                ret = i
        safety_ans = False
        for i in range(0, len(self.my_cards)):
            if risks[len(self.my_cards)-i-1] <= 0:
                ret = len(self.my_cards)-i-1
                safety_ans = True
        for i in range(0, len(self.my_cards)):
            if safety_ans == False and risks[i] >= 5 and risks[i] <= 10:
                ret = i
        return self.my_cards.pop(ret)

    def taking_column(self):  # 一番小さい数を出したときにディーラー側で呼んで、どの列を引き取るか知らせる
        fieldk = 0
        for fieldi in range(3):  # フィールドの各枚数を順に比較し枚数が少ない方を取る
                if len(self.dealer.field[fieldi]) < len(self.dealer.field[fieldk]):
                    fieldk = fieldi
                elif len(self.dealer.field[fieldi]) == len(self.dealer.field[fieldk]):  # 枚数が同じときは5の倍数が少ない方を取る
                    key_cards_counts = [0]*4
                    for i in range(4):
                        for k in range(len(self.dealer.field[i])):
                            if self.dealer.field[i][k] % 5 == 0:
                                key_cards_counts[i] = key_cards_counts[i]+1
                    if key_cards_counts[fieldi] < key_cards_counts[fieldk]:
                        fieldk = fieldi
        return fieldk

    def get_field(self):  # 場の状況を得る
        self.field = self.dealer.field

'''
＜仕様の変更＞....2018/10/05
all_cards_listの作成後、各手持ちカードのriskを数値化
安全なカードをだす
無ければ7枚目を狙う
それもなければfieldより小さい大きいカードで2枚目を狙う
を追加

今までのメソッドを残すかは今後検討し
一番小さいカードをどう処理するかも検討
手持ちのriskが高くて2枚目が狙えないときに出すか
安全な手持ちでも減点が少ない段階でわざと消費するか
'''


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
