import pandas as pd
import numpy as np

from numpy import array
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('location2.csv', encoding='utf-8')
data = data[['x', 'y', 'id', 'address', 'category_group_code', 'category_group_name', 'category_name', 'place_name', 'road_address_name']]

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
  # 본인은 제외
  sim_index=sim_index[sim_index!=target_loca]
  # 중복 제거
  sim_index = np.unique(sim_index)

  # 결과 리턴, 카테고리 & 동까지 동일한거 우선으로
  result=data.iloc[sim_index].sort_values(['sim_cate', 'sim_addr'], ascending = [True, True])[:10]

  # 결과중에 본인 제외
  result = result[result['id'] != id]

  # 확인용 데이터프레임 출력
  print(result)

  # 실제로 어떤 값을 리턴해야 백엔드에서 게시글 불러오는게 가능한지???



### 사용할 장소들
# # 가미우동 / 돈까스,우동 / 서울 마포구 서교동
# recomm(data, 13337463)

# # 연남동느루 / 양식 / 서울 마포구 연남동
# recomm(data, 851863430)

# # 레드버튼 홍대점 / 보드카페 / 서울 마포구 서교동
# recomm(data, 953386352)

# # 피오니 홍대점 / 카페 / 서울 마포구 서교동
# recomm(data, 26235884)

# # 중경마라탕 강남역점 / 중국요리 / 서울 강남구 역삼동
# recomm(data, 1665040674)

# # 샐리오 / 샐러드 / 서울 강남구 역삼동
# recomm(data, 493674871)
