import pandas as pd
import numpy as np

from numpy import sqrt 
from numpy import array
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('location2.csv', encoding='utf-8')
data = data[['x', 'y', 'id', 'address', 'category_group_code', 'category_group_name', 'category_name', 'place_name', 'road_address_name']]

reviews = {
    'user_1': {
        '26235884': 1,
        '26485620': 0,
        '27248379': 0,
        '10368349': 0,
        '27272711': 1,
        '10368349': 1,
    },
    'user_2': {
        '26235884': 1,
        '26485620': 1,
        '27248379': 1,
        '10368349': 1,
        '27272711': 0,
        '10368349': 0,
    },
    'user_3': {
        '26485620': 0,
        '27248379': 1,
        '10368349': 0,
        '2057792795': 0,
        '27272711': 1,
    },
    'user_4': {
        '26235884': 1,
        '26485620': 1,
        '10368349': 1,
        '2057792795': 0,
    },
    'user_5': {
        '26485620': 0,
        '27248379': 0,
        '2057792795': 1,
        '10368349': 0,
        '27272711': 1,
    },
    'user_6': {
        '26235884': 1,
        '26485620': 1,
        '27248379': 1,
        '10368349': 1,
        '2057792795': 0,
        '27272711': 1,
    },
    'user_7': {
        '26235884': 0,
        '26485620': 1,
        '2057792795': 0,
        '10368349': 0,
        '27272711': 0,
    },
    'user_8': {
        '26485620': 1, 
        '27272711': 1,
        '10368349': 0},
}

def sim_pearson(data, name1, name2):
    sumX=0 # X의 합
    sumY=0 # Y의 합
    sumPowX=0 # X 제곱의 합
    sumPowY=0 # Y 제곱의 합
    sumXY=0 # X*Y의 합
    count=0 # 장소 개수
    
    for i in data[name1]: # i = key
        if i in data[name2]: # 같은 장소를 평가했을때만
            sumX+=data[name1][i]
            sumY+=data[name2][i]
            sumPowX+=pow(data[name1][i],2)
            sumPowY+=pow(data[name2][i],2)
            sumXY+=data[name1][i]*data[name2][i]
            count+=1
    
    return ( sumXY- ((sumX*sumY)/count) )/ sqrt( (sumPowX - (pow(sumX,2) / count)) * (sumPowY - (pow(sumY,2)/count)))

def top_review_match(data, name, index=3, sim_function=sim_pearson):
    li=[]
    for i in data: 
        if name!=i: # 자기 자신이 아닐때만
            li.append((sim_function(data,name,i),i)) #sim_function()을 통해 상관계수를 구하고 li[]에 추가
    li.sort() #오름차순
    li.reverse() #내림차순
    return li[:index]


def getRecommendation (data,person,sim_function=sim_pearson):
    result = top_review_match(reviews, person ,len(data))
    
    simSum=0 # 유사도 합을 위한 변수
    score=0 # 선호도(평점) 합을 위한 변수
    li=[] # 리턴을 위한 리스트
    score_dic={} # 유사도 총합을 위한 dic
    sim_dic={} # 평점 총합을 위한 dic
 
    for sim,name in result: # 튜플이므로 한번에 
        if sim<0 : continue # 유사도가 양수인 사람만
        for place in data[name]: 
            if place not in data[person]: # name이 평가를 내리지 않은 장소
                score+=sim*data[name][place] # 그사람의 장소 선호도 * 유사도
                score_dic.setdefault(place,0) # 기본값 설정
                score_dic[place]+=score # 합계
 
                # 조건에 맞는 사람의 유사도의 누적합
                sim_dic.setdefault(place,0) 
                sim_dic[place]+=sim
            score=0  # 장소가 바뀌었으니 초기화
    
    for key in score_dic: 
        score_dic[key]=score_dic[key]/sim_dic[key] # 평점 총합 / 유사도 총합
        li.append((score_dic[key],key)) # list((tuple)) 리턴
    li.sort() # 오름차순
    li.reverse() # 내림차순
    return li

# 테스트
getRecommendation(reviews, 'user_1')
