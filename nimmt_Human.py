#!/usr/local/bin/python3

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
    def get_played_cards(self,dealer_input):
        self.played_cards = dealer_input


    def get_field(self): # 場の状況を得る
        self.field = self.dealer.field

### 継承クラス (ここで基本クラスを継承して、様々な処理を行う) ###
#from nimmtHuman import Human
class Human(Player):
    def put_card(self):
        self.print_field()
        self.my_cards.sort()
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
            print(i,_field[i])


