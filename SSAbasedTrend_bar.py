from __future__ import unicode_literals, print_function
import csv, os
import pandas as pd
import plotnine
from plotnine import *
import numpy as np
from matplotlib import pyplot as plt
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
pol_df['date'] = pd.to_datetime(pol_df['date'], format='%Y-%m-%d')
pol_df = pol_df.set_index('date', inplace=False)

##날짜 범위 설정해주기
n = input('숫자 + D(Days), W(Weeks), M(Month), Y(Years) (ex: 3일간격 = 3D): ')
n_pol_df = pol_df.resample(n).sum()
n_pol_df = n_pol_df.reset_index('date')
print(n_pol_df)

##그래프 그리기

plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (12, 8)

plt.figure()

x = np.arange(len(n_pol_df['date']))

plt.bar(x-0.0, n_pol_df['POSITIVE'], label='POSITIVE', width=0.3, color='blue')
plt.bar(x+0.2,n_pol_df['NEGATIVE'] , label='NEGATIVE', width=0.3, color='red')
plt.xticks(x, n_pol_df['date'])

plt.legend()
plt.xlabel('date')
plt.ylabel('sentiment')
plt.title('')

plt.show()

# ##csv파일로 출력
# pol_df.to_csv(r'F:\Programming\python\창회선배스터디\SSAbasedTrend\result.csv')

# os.startfile(r'F:\Programming\python\창회선배스터디\SSAbasedTrend\result.csv')