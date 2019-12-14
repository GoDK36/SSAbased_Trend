from __future__ import unicode_literals, print_function
import csv, os
import pandas as pd
import plotnine
from plotnine import *
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

data = list(csv.reader(open(r'F:\Programming\python\창회선배스터디\SSAbasedTrend\1-SO-SSAbasedTrend-InputSample.t.csv', 'r', encoding='cp949')))[1:]
pol_data = pd.read_csv(r'F:\Programming\python\창회선배스터디\SSAbasedTrend\1-SO-SSAbasedTrend-InputSample.t.csv', names=['date','pol'])[1:]

#data의 논항들 리스트화
pv = list(set(pol_data.pol.tolist())) 

###날짜 기간 설정

n = int(input('days:'))
startDate = data[0][0]
endDate = data[-1][0] 
tempDt =pd.to_datetime(startDate,dayfirst=True)
tempDt = dt.datetime.date(tempDt)
endDt = pd.to_datetime(endDate,dayfirst=True)
dtList = []
while True:
    tempStr = str(tempDt)
    dtList.append(tempStr)
    tempDt += dt.timedelta(days=n) ##이 숫자를 변형해서 주기 설정 가능 , 단, weeks(주)단위가 최대
    if tempDt >= endDt:
        tempStr = str(tempDt)
        dtList.append(tempStr)
        break

##값들별로 리스트화 하기
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

#데이터프레임화 한 후 sumup해주기
pol_df = pd.DataFrame(res)
pol_df = pol_df.fillna(0)
pol_df = pol_df.groupby(['date'], as_index=False).sum() ##기준이되는 열로 병합해주기
pol_df = pol_df[1:]
pol_df = pol_df[['date','POSITIVE','NEGATIVE']]
print(pol_df)
##그래프 그리기

smthlv=int(input('smooth level:'))

pol_graph = (
    ggplot(pol_df,aes(x='date'))
    + stat_smooth(aes(y='POSITIVE'),color='blue',geom='smooth', position='identity',method='lm',se=False,n=smthlv,group=1) #평균 선 그리기
    + stat_smooth(aes( y='NEGATIVE'),color='red',method='lm',se=False,n=smthlv,group=2) #평균 선 그리기
    + geom_point(aes(x='date', y='POSITIVE'),color='blue',alpha=0.3) #alpha는 투명도 0부터1까지
    + geom_line(aes(x='date', y='POSITIVE'),color='blue',alpha=0.3,group=1)
    + geom_point(aes(x='date', y='NEGATIVE'),color='red',alpha=0.3)
    + geom_line(aes(x='date', y='NEGATIVE'),color='red',alpha=0.3,group=2)
    + xlab('date')
    + ylab('Sentiment')

)

print(pol_graph)
##csv파일로 출력
pol_df.to_csv(r'F:\Programming\python\창회선배스터디\SSAbasedTrend\result.csv')

os.startfile(r'F:\Programming\python\창회선배스터디\SSAbasedTrend\result.csv')