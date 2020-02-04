from __future__ import unicode_literals, print_function
import csv, os
import pandas as pd
import plotnine
from plotnine import *
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

data = list(csv.reader(open(r'C:\GOD\programming\NLP\DecoSentA\SSAbased_Trend\1-SO-SSAbasedTrend-InputSample.t.csv', 'r', encoding='cp949')))[1:]
pol_data = pd.read_csv(r'C:\GOD\programming\NLP\DecoSentA\SSAbased_Trend\1-SO-SSAbasedTrend-InputSample.t.csv', names=['date','pol'])[1:]

#data의 논항들 리스트화
pv = list(set(pol_data.pol.tolist())) 

##데이터 프레임 정렬

startDate = data[0][0]
endDate = data[-1][0] 
tempDt =pd.to_datetime(startDate,dayfirst=True)
tempDt = dt.datetime.date(tempDt)
endDt = pd.to_datetime(endDate,dayfirst=True)
dtList = []
while True:
    tempStr = str(tempDt)
    dtList.append(tempStr)
    tempDt += dt.timedelta(days=1) ##이 숫자를 변형해서 주기 설정 가능 , 단, weeks(주)단위가 최대
    if tempDt >= endDt:
        tempStr = str(tempDt)
        dtList.append(tempStr)
        break

res = []

for x in data:
    temp = {}
    for y in dtList:
        if y in x:
            temp['date'] = y
        else:
            continue 
    for z in pv:
        if z in pv:
            temp[z] = x.count(z)
        else:
            continue
    res.append(temp)
pol_df = pd.DataFrame(res)
pol_df = pol_df.groupby(['date'], as_index=False).sum()
pol_df['date'] = pd.to_datetime(pol_df['date'])
pol_df = pol_df.set_index('date', inplace=False)


##날짜 범위 설정해주기
n = input('숫자 + D(Days), W(Weeks), M(Month), Y(Years) (ex: 3일간격 = 3D): ')
n_pol_df = pol_df.resample(n).sum()
n_pol_df = n_pol_df.reset_index('date')
print(n_pol_df)


#그래프 그리기

pol_graph = (
    ggplot(n_pol_df,aes(x='date'))
    + stat_smooth(aes(y='POSITIVE', group=1),se=False,color='#33cccc') #평균 선 그리기
    + stat_smooth(aes( y='NEGATIVE', group=2),color='crimson', se=False) #평균 선 그리기
    + geom_line(aes(y='POSITIVE'),color='#33cccc',alpha=0.3)
    + geom_line(aes(y='NEGATIVE'),color='crimson',alpha=0.3)
    + geom_point(aes(y='POSITIVE'),color='#33cccc', size=2,alpha=0.3) #alpha는 투명도 0부터1까지
    + geom_point(aes(y='NEGATIVE'),color='crimson', size=2,alpha=0.3)
    + ylab("Sentiment")
    + xlab("Date")
    + theme(axis_line = element_line(color = 'black'))
    + theme_bw()  
    + theme(panel_background = element_rect(),
            plot_background = element_rect(),
            strip_background = element_rect(),
            panel_grid_major_x = element_line(size=0.1, color = 'grey',linetype='-'),
            panel_grid_minor_x = element_rect(),
            panel_spacing = float(1),
            axis_line = element_line(size=0.6, color = 'black'),
            legend_key = element_rect(fill='white'),
            axis_ticks = element_line(color='black'),
            figure_size = (16,8),
            )
    + theme(axis_line = element_line(color = 'black'))
)

print(pol_graph)

##csv파일로 출력
n_pol_df.to_csv(r'C:\GOD\programming\NLP\DecoSentA\SSAbased_Trend\result.csv')

os.startfile(r'C:\GOD\programming\NLP\DecoSentA\SSAbased_Trend\result.csv')