from konlpy.tag import Hannanum, Komoran, Kkma, Okt, Mecab

text = '홍길동 전화번호는 Kt 1234-5678번 입니까?'
hannanum = Hannanum()
print(hannanum.pos(text))

komoran = Komoran()
print(komoran.pos(text))

kkma = Kkma()
print(kkma.pos(text))

okt = Okt()
print(okt.pos(text))

mecab = Mecab()
print(mecab.pos(text))
