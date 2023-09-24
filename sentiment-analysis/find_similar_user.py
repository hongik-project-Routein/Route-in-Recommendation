# 라이브러리 설정
import random
import pandas as pd
import statistics
import matplotlib.pyplot as plt
%matplotlib inline

from sklearn.metrics.pairwise import cosine_similarity
import operator

# bigquery에 저장된 테이블 pyspark로 불러옴
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .config('spark.jars.packages','com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.22.0,com.google.cloud.bigdataoss:gcs-connector:hadoop3-1.9.5,com.google.guava:guava:r05') \
    .getOrCreate()

table = "carbon-inkwell-290604.route_in.sentimental_score"
df = spark.read.format("com.google.cloud.spark.bigquery").option("table",table).load()

from pyspark.sql import functions as F

pd_df = df.toPandas()
pd_df['score'] = pd_df.score.astype(float)
pd_df.round(5)

# 테이블 피벗
pi_pd_df = pd_df.pivot_table(index='userId', columns='mapId', values='score').fillna(0)

# 비슷한 성향 유저 찾기
def find_sim_users(user_id, matrix, k=5):
    # 현재 유저에 대한 데이터프레임 만들기
    # matrix의 index = user_id -> 현재 1명 유저에 대한 평가 정보 찾기
    user = matrix[matrix.index == user_id]
    
    # matrix index 값이 user_id와 다른가?
    # 일치하지 않는 값들은 other_users
    other_users = matrix[matrix.index != user_id]
    
    # 대상 user, 다른 유저와의 cosine 유사도 계산 
    # list 변환
    similarities = cosine_similarity(user,other_users)[0].tolist()
    
    # 다른 사용자의 인덱스 목록 생성
    other_users_list = other_users.index.tolist()
    
    # 인덱스/유사도로 이뤄진 딕셔너리 생성
    # dict(zip()) -> {'other_users_list1': similarities, 'other_users_list2': similarities}
    user_similarity = dict(zip(other_users_list, similarities))
    
    # 딕셔너리 정렬
    # key=operator.itemgetter(1) -> 오름차순 정렬 -> reverse -> 내림차순
    user_similarity_sorted = sorted(user_similarity.items(), key=operator.itemgetter(1))
    user_similarity_sorted.reverse()
    
    # 가장 높은 유사도 k개 정렬하기
    top_users_similarities = user_similarity_sorted[:k]
    users = [i[0] for i in top_users_similarities]
    
    return users
    # 현재 유저에 대한 정보 찾기
    user = matrix[matrix.index == user_id]

# 테스트
find_sim_users("user1", pi_pd_df, k=5)
