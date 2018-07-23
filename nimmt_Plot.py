#!/usr/local/bin/python3

# NUM_GAME (下に定義) の回数一気に python で実行するスクリプト
#pandasを用いてcsvを解析し，平均順位，1位を取った割合，各々の順位を取った回数を計算する
#デフォルトではstat.csvにデータを出力する（既にある場合は消される）
#matplotlib,numpyを用いて棒グラフで視覚化する

import random
import os
import sys
import copy
import csv
import pandas as pd
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import numpy as np


dataset = pd.read_csv(output,header=0,encoding='utf-8')#make dataframe
f=open(output,"a")
f.write("average:,")
average=list(range(len(players_list)))#initial
for i in range(len(players_list)-1):
    data_list=dataset.iloc[0:NUM_GAME+1,i+1].values.tolist()#CSVの列をリストで取り出す
    ave=sum(data_list) / len(data_list)
    average[i]=ave
    avest=str(ave)
    f.write(avest+",")
data_list=dataset.iloc[0:NUM_GAME+1,len(players_list)].values.tolist()#端にカンマを入れさせない
ave=sum(data_list) / len(data_list)
average[len(players_list)-1]=ave
avest=str(ave)
f.write(avest)
f.write('\n')


for k in range(len(players_list)):
    ss=str(k)
    f.write("num_"+ ss + ":, ")
    for i in range(len(players_list)-1):
        data_list=dataset.iloc[0:NUM_GAME+1,i+1].values.tolist()#CSVの列をリストで取り出す
        count=data_list.count(k)
        ct=str(count)
        f.write(ct)
        f.write(",")
    data_list=dataset.iloc[0:NUM_GAME+1,len(players_list)].values.tolist()#端にカンマを入れさせない
    count=data_list.count(k)
    ct=str(count)
    f.write(ct)
    f.write('\n')
f.close()

ct1st=list(range(len(players_list)))#initial
for i in range(len(players_list)):
    data_list=dataset.iloc[0:NUM_GAME+1,i+1].values.tolist()#CSVの列をリストで取り出す
    ct1st[i]=data_list.count(0)


df = pd.read_csv(output,header=0,encoding='utf-8')
color=['red','skyblue','springgreen','forestgreen','limegreen','lightgreen','mediumspringgreen','greenyellow','black']
w = 0.4
X = range(len(players_list)) 
Y=list(range(len(players_list)))#initial
Y[0]=df.iloc[NUM_GAME+1,1:len(players_list)+1].values.tolist()
plt.bar(X, Y[0], color=color[0], width=w,label=0, align="center")
bt=np.array([0.]*len(players_list))
for i in range(len(players_list)-1):
	bt+=np.array(Y[i])
	Y[i+1]=df.iloc[NUM_GAME+i+2,1:len(players_list)+1].values.tolist()
	plt.bar(X, Y[i+1], color=color[i+1],bottom=bt, width=w,label=i+1, align="center")

plt.legend(bbox_to_anchor=(1.1,0.6))
name=[]
for i in range(len(players_list)):
    name.append(str(players_list[i].__class__.__name__))
plt.xticks(X,name,fontsize=7)

for i in range(len(players_list)):
    plt.text(i, 0.1*NUM_GAME, average[i], ha='center', va='bottom')


for i in range(len(players_list)):
    st=str(100*ct1st[i]/NUM_GAME)
    plt.text(i, 0.05*NUM_GAME, st+"%", ha='center', va='center')

plt.show()


