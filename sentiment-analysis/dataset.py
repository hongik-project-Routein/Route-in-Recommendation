from sklearn.feature_extraction.text import TfidfTransformer

df1 = pd.read_csv('/home/smin/smin-test/route-in/csv/review_data.csv')
df2 = pd.read_csv('/home/smin/smin-test/route-in/csv/review_data2.csv')

def text_cleansing(text): 
    re_text = re.compile('[^ ㄱ-ㅣ가-힣]+')

    # 지정한 정규식에 해당하지 않은 것은 길이가 0인 문자열로 변환
    res = re_text.sub('', text)
    return res

## 학습용
# 첫번째 데이터셋 전처리
df1["clean_review"] = df1["review"].apply(lambda x : text_clearing(x))
df1.drop("review", axis=1, inplace=True)
df1['sentiment_score'] = df1['score'].apply(lambda x: 0 if x <= 3 else 1) # 리뷰점수 3 이하는 부정(0)으로, 4이상은 긍정(1)
df1 = df1[['clean_review', 'sentiment_score']]

# 두번째 데이터셋 전처리
df2["clean_review"] = df2["origin_reivew"].apply(lambda x : text_clearing(x))
df2.drop("origin_reivew", axis=1, inplace=True)
df2.rename(columns = {"senti_int" : "sentiment_score"}, inplace = True)
df2 = df2[['clean_review', 'sentiment_score']]


# 데이터셋 합치기
all_df = pd.concat([df1, df2]).reset_index(drop=True)
