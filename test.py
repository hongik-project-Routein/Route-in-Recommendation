from google.cloud import language_v1

import pandas as pd
import numpy as np

from numpy import array
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Google Cloud Natural Language API 클라이언트 생성
client = language_v1.LanguageServiceClient()

def analyze_sentiment(text):
    # 주어진 텍스트의 감정분석
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment
    return sentiment.score

def process_json(json_data):
    # 주어진 JSON 데이터를 처리하여 긍정적인 score가 반환되는 경우에만 pin의 id를 리스트화
    pins = json_data.get('pin', [])
    positive_pin_ids = []
    
    for pin in pins:
        sentiment_score = analyze_sentiment(pin.get('content', ''))
        if sentiment_score > 0:
            print(pin.get('content'), "/" , pin.get('place_id'), "/" , sentiment_score)
            pin_id = pin.get('place_id')
            if pin_id is not None:
                positive_pin_ids.append(pin_id)
    
    return positive_pin_ids


# 데이터 불러옴
data = pd.read_csv('location2.csv', encoding='utf-8')

# 데이터 전처리
data['detailed_cate'] = data.category_name.str.split(' > ').str[-1]
data['dong'] = data.address.str.split(' ').str[:3]
data['dong'] = data['dong'].astype(str).apply(lambda col: col.strip('[]').strip('\''))
data['dong'] = data['dong'].astype(str).apply(lambda col: col.replace("\', \'", " "))

counter_vector = CountVectorizer(ngram_range=(1,1))
# 종류 벡터화
c_vec_d_cate = counter_vector.fit_transform(data['detailed_cate'])
c_vec_d_cate.shape
# 코사인 유사도 추출
similar_cate = cosine_similarity(c_vec_d_cate).argsort()[:,::-1]

def recomm(data, id, top = 30):
  # 사용자가 선호한 장소의 detailed_category 뽑기
  target_cate = data[data['id'] == id]['detailed_cate'].values[0]
  print(target_cate)
  # 같은 detailed_category이면 1, 아니면 2
  data["sim_cate"] = np.where(data['detailed_cate'] == target_cate, 1, 2)

  # 사용자가 선호한 장소의 동까지 주소 뽑기
  target_dong = data[data['id'] == id]['dong'].values[0]
  # 동이 일치하면 1, 아니면 2
  data["sim_addr"] = np.where(data['dong'] == target_dong, 1, 2)
  
  # 사용자가 선호한 장소의 세부 카테고리 뽑아내기
  target_loca = data[data['id'] == id].index.values

  # category 코사인 유사도 
  sim_index=similar_cate[target_loca,:top].reshape(-1)
  
  sim_index=sim_index[sim_index!=target_loca] # 본인은 제외
  sim_index = np.unique(sim_index) # 중복 제거

  # 결과 리턴, 카테고리 & 동까지 동일한거 우선으로
  result=data.iloc[sim_index].sort_values(['sim_cate', 'sim_addr'], ascending = [True, True])[:5]

  # 결과중에 본인 제외
  result = result[result['id'] != id]

  # 확인용 데이터프레임 출력
  print(result) # 실제로 어떤 값을 리턴해야 백엔드에서 게시글 불러오는게 가능한지???

def all(json_content):
    # json 데이터 감정 분석 -> 긍정적인 핀 리스트 -> 리스트 돌면서 장소 추천
    posi_pin_ids = process_json(json_content)
    for posi_pin_id in posi_pin_ids:
        recomm(data, posi_pin_id)


json_data = {
    "post": {
        "content": "111111111111111111"
    },
    "pin": [
        {
            "id": 1,
            "lat": 37.1234,
            "lng": 127.5678,
            "name": "가미우동",
            "place_id": 13337463,
            "content": "행복한 하루"
        },
        {
            "id": 2,
            "lat": 37.1224,
            "lng": 127.8754,
            "name": "레드버튼 홍대점",
            "place_id": 953386352,
            "content": "보드게임으로 불태운 하루!!!!"
        },
        {
            
            "id": 3,
            "lat": 37.1224,
            "lng": 127.8754,
            "name": "중경마라탕 강남역점",
            "place_id": 1665040674,
            "content": "위생 최악이고 맛도 없음 ... 별로임"
        }
    ]
}

# 위 JSON 데이터 기준으로, 우동집이랑 보드게임만 추천해주는 결과를 받아볼 수 있음 
all(json_data)
