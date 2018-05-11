import random
class KawadaAI(object):
    ### 必須メソッド (4 つ) ###
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
        if len(field_edge)!=0:#おける場所があればfieldの一番小さい数より大きい一番小さい数を出す
            min=sorted(field_edge)[0]#１番小さい数字定義
            gap=150
            for i in range (len(self.my_cards)):
                if self.my_cards[i]>min:
                    if self.my_cards[i]-min<gap:
                        gap=self.my_cards[i]-min
                        ret=i
        if len(field_edge)==0:#どこも出せなければ一番低い数を出す
            ret=0
            for i in range(len(self.my_cards)):
                if self.my_cards[i]<self.my_cards[ret]:
                    ret=i
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