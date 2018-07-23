#!/usr/local/bin/python3

# NUM_GAME (下に定義) の回数一気に python で実行するスクリプト

import argparse

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,argparse.MetavarTypeHelpFormatter):
    pass

parser = argparse.ArgumentParser(description="play nimmt.", formatter_class=CustomFormatter)

parser.add_argument('--num', type=int, dest='num_game', nargs='?', default=1, help="number of game")
parser.add_argument('--out', type=str, dest='outfile', nargs='?', default='stat.csv', help="output file")
parser.add_argument('--fig', type=str, dest='figfile', nargs='?', default='stat.png', help="output figure file (png)")

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

#players_list = [player0, player1, player2, player3, player4, player5, player6, player7, player8]
players_list = [player1, player2, player3, player4, player5, player6, player7, player8]

game = Game(players_list)
NUM_GAME = args.num_game
for i in range(NUM_GAME):
    game.play()
del game

import numpy
import pandas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys


# create formatted printing string
# pre: insert string in head
# list: printing 1D list
# sep: printing separater
# post: insert string in the end
# form: format of printing list
def __convert_string(pre="",list=[],sep=", ",post="",form="{:5.2f}"):
    _string = pre
    _sep_len = len(sep)
    for i in list:
        _string += str(form.format(i)) + sep
    _string = _string[:-_sep_len]
    _string += post
    return _string

# import datafile
datafile = pandas.read_csv(args.outfile,header=0,encoding='utf-8')
# calculate statistic values
average_list = __convert_string(pre="average: ", list=list(datafile.mean()),post="\n")
std_list     = __convert_string(pre="std:     ", list=list(datafile.std(ddof=False)),post="\n") # option: ddot=False -> 1/n, ddot=True -> 1/(n-1)

### create ploting data list ###
# format
_players_list = list(datafile.columns)
# xticks
xticks = [i for i in range(len(_players_list))]
xlabel = _players_list
# y[0], y[1], ...
_bottom = [0 for i in range(len(_players_list))]
plt.rcParams["font.size"] = 7
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for i in range(len(_players_list)):
    _list = []
    for player in _players_list:
        _count_rank = (datafile[player]==i).sum()
        _list.append(_count_rank)
    ax.bar(xticks, _list, tick_label=xlabel, bottom=_bottom, align="center", label=str(i))
    _bottom = [_bottom[i]+_list[i] for i in range(len(_players_list))]
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], title='Line', loc='upper left')

plt.legend()
# save as png
plt.savefig(args.figfile)


#plt.show()
sys.exit(1)

updatefile = open(args.outfile,"a")
updatefile.write(average_list)
updatefile.write(std_list)

#for player in players_list:

print(datafile["SakuraiAI"])
print(datafile["SakuraiAI"].value_counts().sort_index())
print(dict(datafile["SakuraiAI"].value_counts().sort_index()))

mylist=datafile["SakuraiAI"] == 0
print(mylist)
print(mylist.sum())

print("aaa")
print((datafile["SakuraiAI"]==0).sum())

sys.exit(1)
print(datafile)
print(type(datafile))
print(type(datafile.mean()))





