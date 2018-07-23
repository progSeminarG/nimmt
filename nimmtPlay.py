#!/usr/local/bin/python3

# NUM_GAME (下に定義) の回数一気に python で実行するスクリプト

import argparse

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,argparse.MetavarTypeHelpFormatter):
    pass

parser = argparse.ArgumentParser(description="play nimmt.", formatter_class=CustomFormatter)

parser.add_argument('--num', type=int, dest='num_game', nargs='?', default=1, help="number of game")
parser.add_argument('--out', type=str, dest='outfile', nargs='?', default='stat.csv', help="output file")

args = parser.parse_args()

class Game(object):
    def __init__(self,players):
        self.SCORE_THRESH = 66
        self.players_list = players
        self.file = open(args.outfile,"w+")
        memberlist = ""
        for player in self.players_list:
            memberlist += player.__class__.__name__ + ", "
        memberlist = memberlist[:-2] + "\n"
        self.file.write(memberlist)

    def __del__(self):
        self.file.close()

    def play(self):
        game_score = []
        game_score_sum = [0]*len(self.players_list)
        igame = 0
        while True:
            igame += 1
            print("##### game",igame,"start #####")
            dealer = Dealer(self.players_list)
            for i in range(dealer.num_hand): # 1 ゲームのループ (手札がなくなるまで)
                print("--- turn:",i,"/",dealer.num_hand,"---")
                dealer.print_field() # 場の状況の表示。
                dealer.receive_cards() # プレイヤーからカードを受け取る。
                dealer.open_cards() # プレイヤーに出されたカードを知らせる (get_played_cards メソッドを使う)。
                dealer.print_played_cards() # 受け取ったカードの表示。
                dealer.line_up_cards() # 集めたカードを配置する。
                print("score:",dealer.score)
            dealer.print_score()
            game_score.append(dealer.score)
            game_score_sum = [x+y for (x,y) in zip(game_score_sum,dealer.score)]
            if max(game_score_sum) >= self.SCORE_THRESH:
                print("final score:",game_score_sum)
                print("##### game end #####")
                ranking = sorted(range(len(self.players_list)),key=lambda k:game_score_sum[k])
                for i in ranking:
                    print('{:>2}. {:-<12}({:02}){:>3} |'.format(
                            ranking.index(i)+1,
                            self.players_list[i].__class__.__name__,
                            i,
                            game_score_sum[i]),
                            end=''
                            )
                    for j in range(igame):
                        print('{:>4}'.format(game_score[j][i]),end='')
                    print()
                scorelist = ""
                for iplayer in range(len(players_list)):
                    scorelist += str(ranking.index(iplayer)) + ", "
                scorelist = scorelist[:-2] + "\n"
                self.file.write(scorelist)
#                for i in range(len(players_list)-1):
#                    rank = str(ranking.index(i))
#                    self.file.write(rank)
#                    self.file.write(",")
#                rank = str(ranking.index(len(players_list)-1))
#                self.file.write(rank)
#                self.file.write("\n")
                break

### 継承クラス (ここで基本クラスを継承して、様々な処理を行う) ###
from nimmt_Dealer import Dealer, Player # 必須: dealer class

from nimmt_Human import Human
from nimmt_Takahashi import TakahashiAI
from nimmt_Sakurai import SakuraiAI
from nimmt_Hirai import HiraiAI
from nimmt_Hoizumi import HoizumiAI
from nimmt_Kawada import KawadaAI
from nimmt_Shirai import ShiraiAI
from nimmt_Takai import TakaiAI
from nimmt_Kikuchi import KikuchiAI
from nimmt_Muto import MutoAI

### create players ###
player0 = TakahashiAI()
player1 = SakuraiAI()
player2 = Player() #HoizumiAI()
player3 = TakaiAI()
player4 = HiraiAI()
player5 = KawadaAI()
player6 = ShiraiAI()
player7 = KikuchiAI()
player8 = MutoAI()
#player9 = Player()

players_list = [player0, player1, player2, player3, player4, player5, player6, player7, player8]

game = Game(players_list)
NUM_GAME = args.num_game
for i in range(NUM_GAME):
    game.play()
del game

