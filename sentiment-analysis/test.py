from keras import models
from tensorflow.keras.layers import Embedding, Dense, LSTM, GRU, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.feature_extraction.text import TfidfTransformer

import urllib.request
import pickle

df1 = pd.read_csv('/data/naver_dining_review.csv')
df2 = pd.read_csv('/data/ds01.csv')

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

urllib.request.urlretrieve("https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt", filename="/home/smin/smin-test/route-in/csv/shop_rating.txt")
shop_df = pd.read_table('shop_rating.txt', names=['ratings', 'origin_reivew'])
shop_df.drop_duplicates(subset=['origin_reivew'], inplace=True) # 중복제거
shop_df["clean_review"] = shop_df["origin_reivew"].apply(lambda x : text_clearing(x))
shop_df.drop("origin_reivew", axis=1, inplace=True)
shop_df['sentiment_score'] = shop_df['ratings'].apply(lambda x: 0 if x <= 3 else 1) # 리뷰점수 3 이하는 부정(0)으로, 4이상은 긍정(1)
shop_df = shop_df[['clean_review', 'sentiment_score']]

urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", filename="/home/smin/smin-test/route-in/csv/ratings_train.txt")
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", filename="/home/smin/smin-test/route-in/csv/ratings_test.txt")
movie_df1 = pd.read_table('/home/smin/smin-test/route-in/csv/ratings_train.txt')
movie_df2 = pd.read_table('/home/smin/smin-test/route-in/csv/ratings_test.txt')

#쓸모없는 행 삭제
movie_df1 = movie_df1.drop(['id'], axis=1)
movie_df2 = movie_df2.drop(['id'], axis=1)
movie_df1.rename(columns = {"document": "clean_review", "label" : "sentiment_score"}, inplace = True)
movie_df2.rename(columns = {"document": "clean_review", "label" : "sentiment_score"}, inplace = True)


# 데이터셋 합치기
pdList = [df1, df2, shop_df, movie_df1, movie_df2]
all_df = pd.concat(pdList).reset_index(drop=True)
## 총 414587개


# 학습용, 테스트용 데이터셋 분리
train, test = train_test_split(all_df, test_size=0.2, random_state=210617)

# 학습용 데이터셋 라벨 분포 확인
train['sentiment_score'].value_counts().plot(kind = 'bar')
print(train.groupby('sentiment_score').size().reset_index(name = 'count'))

stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']

mecab = Mecab()
train_list = [] 
test_list = []

for sentence in train['clean_review']:
    temp_X = mecab.morphs(sentence, stem = True) 
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    train_list.append(temp_X)
for sentence in test['clean_review']:
    temp_X = mecab.morphs(sentence, stem = True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    test_list.append(temp_X)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_list)
tokenizer.fit_on_texts(test_list)

# 생성한 단어사전 저장
with open("all_reviews.pickle","wb") as fw:
    pickle.dump(tokenizer, fw)


# 단어로 쪼개진 문장 숫자로
t_train1 = tokenizer.texts_to_sequences(train_list)
t_test1 = tokenizer.texts_to_sequences(test_list)

# 정답으로 사용할 감정점수 분류
s_train = train['sentiment_score']
s_test = test['sentiment_score']

