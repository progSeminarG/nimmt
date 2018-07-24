#!/usr/local/bin/python3

import argparse
import time
import contextlib
import sys

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,argparse.MetavarTypeHelpFormatter):
    pass

parser = argparse.ArgumentParser(description="play nimmt.", formatter_class=CustomFormatter)

parser.add_argument('--num', type=int, dest='num_game', nargs='?', default=1, help="number of game")
parser.add_argument('--out', type=str, dest='outfile', nargs='?', default='stat.csv', help="output file")
parser.add_argument('--fig', type=str, dest='figfile', nargs='?', default='stat.png', help="output figure file (png)")
parser.add_argument('-q', '--quiet', action="store_true", help='reduce print sequence')

args = parser.parse_args()

@contextlib.contextmanager
def silence(flagquiet):
    if flagquiet:
        __stdout_original = sys.stdout
        nullfile = open(os.devnull, 'w')
        sys.stdout = nullfile
        try:
            yield
        finally:
            sys.stdout = __stdout_original
    else:
        try:
            yield
        finally:
            pass

class Game(object):
    def __init__(self,players):
#        if args.quiet:
#            self.__stdout_original = sys.stdout
#            nullfile = open(os.devnull,'w')
#            sys.stdout = nullfile
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
#        if args.quiet: sys.stdout = self.__stdout_original

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
                # export data to file
                scorelist = ""
                for iplayer in range(len(players_list)):
                    scorelist += str(ranking.index(iplayer)) + ", "
                scorelist = scorelist[:-2] + "\n"
                self.file.write(scorelist)
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
player2 = HoizumiAI()
player3 = TakaiAI()
player4 = HiraiAI()
player5 = KawadaAI()
player6 = ShiraiAI()
player7 = KikuchiAI()
player8 = MutoAI()
#player9 = Player()

players_list = [player0, player1, player2, player3, player4, player5, player6, player7, player8]

import os
import sys

### create game and play ###
game = Game(players_list)
NUM_GAME = args.num_game
_time_start = time.time()
for i in range(NUM_GAME):
    with silence(args.quiet):
        game.play()
del game
_time_finish = time.time()
_time_spent = _time_finish - _time_start
_time_hour = int(_time_spent / 3600)
_time_spent -= _time_hour * 3600
_time_min = int(_time_spent/60)
_time_spent -= _time_min * 60
_time_sec = int(_time_spent)
print("time spent for {:>d} games: {:>d} h {:>d} min {:>d} sec.".format(NUM_GAME,_time_hour,_time_min,_time_sec))
print("data saved:",args.outfile)

from nimmt_Plot import ReadPlot
### plot data ###
stat_inst = ReadPlot(datafile=args.outfile,figfile=args.figfile)
stat_inst.plot()


