from __future__ import unicode_literals, print_function
import csv, os
import pandas as pd
import plotnine
from plotnine import *
import matplotlib
import matplotlib.pyplot as plt
from mizani.breaks import date_breaks
from mizani.formatters import date_format


##자료 불러오기
pol_data = list(csv.reader(open(r'E:\Programming\python\창회선배스터디\SSAbasedTrend\1-SO-SSAbasedTrend-InputSample.t.csv', 'r', encoding='cp949')))[1:]


##데이터 날짜별로 pos,neg 개수 세서 변환
pol_res = {}

def insert_label(result_dict, date, label):
    if label == 'POSITIVE': result_dict[date][0] += 1
    else: result_dict[date][1] += 1
    return result_dict

for date, label in pol_data:
    if date in pol_res.keys(): pol_res = insert_label(pol_res, date, label)
    else:
        pol_res[date] = [0, 0]
        pol_res = insert_label(pol_res, date, label)


##dict데이터 list화
date_lst = list(pol_res.keys())
sent_lst = list(pol_res.values())
pos_lst = []
neg_lst = []

for x in range(0,len(sent_lst)):
    pos_lst.append(sent_lst[x][0])

for y in range(0, len(sent_lst)):
    neg_lst.append(sent_lst[y][1])


##list데이터 dataframe화
pol_df = pd.DataFrame({'date' : date_lst,
                      'Positive' : pos_lst,
                      'Negative' : neg_lst})

# pol_lst = pol_df.values.tolist() #전체 데이타프레임 list화

##그래프 그리기
pol_graph = (
    ggplot(pol_df)
    + geom_point(aes(x='date', y='Positive'),color='blue',alpha=0.5) #alpha는 투명도 0부터1까지
    + geom_line(aes(x='date', y='Positive'),color='blue',alpha=0.5,group=1)
    + geom_point(aes(x='date', y='Negative'),color='red',alpha=0.5)
    + geom_line(aes(x='date', y='Negative'),color='red',alpha=0.5,group=2)
    + scale_x_datetime(breaks=date_breaks('10 weeks')) #스트링 안에 주기를 설정하여 출력가능
    + xlab('date')
    + ylab('Sentiment')
    + geom_smooth(aes(x='date', y='Positive'),color='blue',method='lm',se=False) #평균 선 그리기
    + geom_smooth(aes(x='date', y='Negative'),color='red',method='lm',se=False) #평균 선 그리기
)
print(pol_graph)

##csv파일로 출력
pol_df.to_csv(r'E:\Programming\python\창회선배스터디\SSAbasedTrend\result.csv')

os.startfile(r'E:\Programming\python\창회선배스터디\SSAbasedTrend\result.csv')