#!/usr/local/bin/python3

import numpy
import pandas
import matplotlib
import matplotlib.pyplot as plt
import sys

class ReadPlot(object):
    def __init__(self,datafile="stat.csv",figfile="stat.png"):
        self.__datafile = datafile
        self.__figfile = figfile
        self.__readfile(datafile=datafile)

    def __readfile(self,datafile="stat.csv"):
        self.__data = pandas.read_csv(datafile,header=0,encoding='utf-8',skipinitialspace=True)
        self.__players_class_list = list(self.__data.columns)
        self.__num_players = len(self.__players_class_list)
        self.__players_name_list = [name.replace("AI","") for name in self.__players_class_list]
        # calculate statistic values
        self.__average_list = list(self.__data.mean())
        self.__ranking = sorted(range(self.__num_players),key=lambda k:self.__average_list[k])
        self.__std_list = list(self.__data.std(ddof=False))
        self.__num_games = len(self.__data)

    @property
    def data(self):
        return self.__data

    def plot(self):
        fig, ax = plt.subplots() # create plot space and axis
        plt.rcParams["font.size"] = 7 # font size except ticks
        plt.tick_params(labelsize=7) # font size of ticks
        fig.subplots_adjust(bottom=0.2) # modify bottom margin
        plt.ylim([0,self.__num_games]) # y-range
        _xticks = [i for i in range(self.__num_players)] # x-tics = [0, 1, 2, ...]
        _xlabel = [self.__players_name_list[i] for i in self.__ranking] # x-label (list of names)
        _bottom = [0 for i in range(self.__num_players)] # [0,0,0,...]
        for ith in range(self.__num_players): # loop for ith-rank: from 1st, 2nd, 3rd, ...
            _list = []
            for irank in self.__ranking: # loop for each players: from top player to the last
                _player = self.__players_class_list[irank] # get column name of irank-th player
                _count_rank = (self.__data[_player]==ith).sum() # get column data which is ith and count
                _list.append(_count_rank) # append to _list
            # plot bar-graph.
            # x-position, y-height, x-label, offset, align, label for legend
            ax.bar(_xticks, _list, tick_label=_xlabel, bottom=_bottom, align="center", label=str(ith))
            for j in range(len(_list)):
                if _list[j] >= self.__num_games*0.04: # if there is a space in bin
                    # print number of ith-game
                    ax.annotate(_list[j], (_xticks[j],_bottom[j]+_list[j]/2),ha='center',va='center',color='white')
            _bottom = [_bottom[i]+_list[i] for i in range(self.__num_players)] # update offset
        ax.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=True) # delete x-ticks
        ax.text(-1,-self.__num_games*0.1,'ave.',ha='center',va='center') # print 'ave.'
        ax.text(-1,-self.__num_games*0.15,'std.',ha='center',va='center') # print 'std.'
        # print ave. and std. for each player
        for i in range(self.__num_players):
            ax.text(_xticks[i],-self.__num_games*0.11,self.__average_list[self.__ranking[i]],ha='center',va='center')
            ax.text(_xticks[i],-self.__num_games*0.16,'{:.2f}'.format(self.__std_list[self.__ranking[i]]),ha='center',va='center')
        # set legend format
        ax.legend(bbox_to_anchor=(0.,1.,1.,0.05),ncol=self.__num_players,borderaxespad=0.,mode='expand',edgecolor='None')
        # save as png
        plt.savefig(self.__figfile)

        print("data plotted:",self.__figfile)

