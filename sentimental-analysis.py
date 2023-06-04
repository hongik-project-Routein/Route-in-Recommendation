from google.cloud import language_v1

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
    # text = json_data.get('post')
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

# 주어진 JSON 데이터 예시
json_data = {
    "post": {
        "content": "111111111111111111"
    },
    "pin": [
        {
            "id": 1,
            "lat": 37.1234,
            "lng": 127.5678,
            "place_id": 1234,
            "content": "행복한 하루"
        },
        {
            "id": 2,
            "lat": 37.1224,
            "lng": 127.8754,
            "place_id": 2345,
            "content": "비와서 너무 슬픔"
        }
    ]
}

json_data_2 = {
    "post": {
        "content": "2222222222222222222222"
    },
    "pin": [
        {
            "id": 3,
            "lat": 37.1234,
            "lng": 127.5678,
            "place_id": 3456,
            "content": "너무맛있음..."
        },
        {
            "id": 4,
            "lat": 37.1224,
            "lng": 127.8754,
            "place_id": 4567,
            "content": "죽기 전에 꼭 드셔보세요!!!!!"
        },
        {
            "id": 5,
            "lat": 37.1224,
            "lng": 127.8754,
            "place_id": 5678,
            "content": "ㅋㅋㅋㅋㅋㅋㅋㅋ"
        },
        {
            "id": 6,
            "lat": 37.1224,
            "lng": 127.8754,
            "place_id": 6789,
            "content": "다신 안온다 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ"
        },
        {
            "id": 7,
            "lat": 37.1224,
            "lng": 127.8754,
            "place_id": 7890,
            "content": "존맛 ㅠㅠ"
        },
    ]
}

positive_pin_ids = process_json(json_data)
negative_pin_ids = process_json(json_data_2)

print("==================")
print(positive_pin_ids)
print("------------------")
print(negative_pin_ids)
