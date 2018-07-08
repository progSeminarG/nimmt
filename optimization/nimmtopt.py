import nimmtPackopt as nimmt
from nimmt_Shiraiopt import ShiraiAI
from nimmtPackopt import Game
import pandas as pd
from pandas import DataFrame,Series
import numpy as np

###
output="optstat.csv"
NUM_GAME=10
###

### 継承クラス (ここで基本クラスを継承して、様々な処理を行う) ###
from nimmt_Human import Human
from nimmt_Takahashi import TakahashiAI
from nimmt_Sakurai import SakuraiAI
from nimmt_Hirai import HiraiAI
from nimmt_Hoizumi import HoizumiAI
from nimmt_Kawada import KawadaAI
from nimmt_Shiraiopt import ShiraiAI
from nimmt_Takai import TakaiAI
from nimmt_Kikuchi import KikuchiAI
from nimmt_Random import Random

### create players ###
player0 = TakahashiAI()
player1 = SakuraiAI()
player2 = HoizumiAI()
player3 = TakaiAI()
player4 = HiraiAI()
player5 = KawadaAI()
#player6 = ShiraiAI()
player7 = KikuchiAI()
player8 = Random()

initial=[70,0.5,0.1,0.5,5.0,7.0,2.0,0.0,-6.0,4]
dif_list=[5,0.1,0.1,0.1,1,1,0.5,1,1,1]
wpth=[]
wpthtrue=[]

def memo(para):
    player6 = ShiraiAI(para)
    players_list = [player0, player1, player2, player3, player4, player5, player6, player7, player8]
    game=Game(players_list,NUM_GAME)
    game.stat()
    df = pd.read_csv("optstat.csv",header=0,encoding='utf-8')#make dataframe
    wp=df.iat[NUM_GAME+2, 7]
    wpth.append(wp)
    wpthtrue.append(wp)
    f=open("opt.csv","a")
    f.write(str(wpth[i])+"\n")
    f.close()

c=0
i=0
k=0
l=0
para=initial
print("\noptimization start!")
memo(para)
while c<=len(dif_list):
    print("\n"+str(i)+"th optimization")
    print("wpthtrue",wpthtrue)
    print("wpth",wpth)
    if i==0 or k==0:
        para[c]+=dif_list[c]
        i+=1
        memo(para)
        k+=1
        print("1---")
    elif wpth[i]>=wpth[i-1]+5 and k>=1 and l==0:
        k+=1
        para[c]+=dif_list[c]
        i+=1
        memo(para)
        print("2---")
    elif wpth[i]<wpth[i-1]+5 and k==1 and l==0:
        l+=1
        para[c]-=2*dif_list[c]
        wpth[i]=wpth[i-1]
        i+=1
        memo(para)
        print("3---")
    elif wpth[i]>=wpth[i-1]+5 and l>=1:
        l+=1
        para[c]-=dif_list[c]
        i+=1
        memo(para)
        print("4---")
    elif wpth[i]<wpth[i-1]+5 and k>1:
        para[c]-=dif_list[c]
        wpth[i]=wpth[i-1]
        c+=1
        k=0
        l=0
        print("5---")
    elif wpth[i]<wpth[i-1]+5 and l>1:
        para[c]+=dif_list[c]
        wpth[i]=wpth[i-1]
        c+=1
        k=0
        l=0
        print("6---")
    elif wpth[i]<wpth[i-1]+5 and k==1 and l==1:
        para[c]+=dif_list[c]
        wpth[i]=wpth[i-1]
        c+=1
        k=0
        l=0
        print("7---")
    else:
        print("ERROR!")
        print("i,c,k,l",i,c,k,l)
        break
        
