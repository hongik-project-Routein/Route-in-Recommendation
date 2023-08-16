from Morpheme import Morpheme
from EHHelper import EHHelper

class MorphemeParser:
    @staticmethod
    def Merge(morphes):
        remoes = list()# 병합한 형태소를 보관할 컬렉션
        for morph in morphes:# 원본 컬렉션에 있는 각각의 형태소를
            rcnt = len(remoes)# 병합한 컬렉션에 형태소 개수 구하기
            flag = False # morph와 같은 단어가 remoes에 없다고 가정
            # morph가 remoes컬렉션에 있다면 병합
            for index in range(0,rcnt):
                if remoes[index].word == morph.word:
                    remoes[index].Merge(morph)
                    flag = True # 병합하였음을 마킹
                    break            
            if flag == False: # morph와 같은 단어는 remoes에 없음
                remoes.append(morph)
        return remoes
    
    @staticmethod
    def Parse(src):
        morphes = list() 
        # 원본 문자열에 특수 기호를 제거 및 공백 기준으로 분리
        src = EHHelper.EmitTagAndSpecialCh(src)
        msrc = src.split(' ')
        # 각 단어를 형태소 컬렉션에 추가
        for elem in msrc:
            if str.isalpha(elem):
                morphes.append(Morpheme(elem))
        # 중복 형태소를 합치는 공정
        morphes = MorphemeParser.Merge(morphes)
        return morphes
