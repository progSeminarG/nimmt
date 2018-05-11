#!/usr/local/bin/python3

import sys
import argparse
import csv
import re
import numpy
from scipy.stats import rankdata

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,argparse.MetavarTypeHelpFormatter):
    pass

parser = argparse.ArgumentParser(description="analysing score of nimmt.", formatter_class=CustomFormatter)

parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('--file', type=str, dest='infile', nargs='?', default='score.txt', help="input file")
parser.add_argument('--out', type=str, dest='outfile', nargs='?', default='score_summary.csv', help="output file")

args = parser.parse_args()

class Dataset(object):
    def __init__(self):
        self.infile = args.infile
        self.outfile = args.outfile
        self.get_scores() #self.data
        self.num_players = len(self.data[0])
        self.num_games = len(self.data)
        self.get_ranking() #self.ranking
        self.sumup_ranking() #self.stats = [[player1's stats],[player2's stas',...]
        self.output_stats()

    def get_scores(self):
        with open(self.infile,'r') as f:
            reader = csv.reader(f)
            self.data = []
            for row in reader:
                if re.search('final score: \[',str(row)):
                    rowdata = []
                    for i in row:
                        rowdata.append(int(re.sub('^final score: \[','',re.sub('\]','',i))))
                    self.data.append(rowdata)

    def get_ranking(self):
        self.ranking = []
        for one_game_scores in self.data:
            numpy_one_game_scores = numpy.array(one_game_scores)
            ranking = rankdata(numpy_one_game_scores,method='min') -1
            self.ranking.append(ranking.tolist())

    def sumup_ranking(self):
        self.stats = [[0 for i in range(self.num_players)] for j in range(self.num_players)]
        for one_game_rank in self.ranking:
            iplayer = 0
            for irank in one_game_rank:
                self.stats[iplayer][irank] += 1
                iplayer += 1

    def output_stats(self):
        with open(self.outfile,'w') as f:
            for i in range(self.num_players):
                f.write(", player"+str(i))
            f.write("\n")
            for iranking in range(self.num_players):
                f.write(str(iranking+1))
                for iplayer in range(self.num_players):
                    f.write(", "+str(self.stats[iplayer][iranking]))
                f.write("\n")

data = Dataset()
