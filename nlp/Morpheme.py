class Morpheme:
    def __init__(self,word):
        self.word = word #단어 
        self.ref = 1           #참조 개수
    def IsEqual(self,other): #같은 단어를 갖는 형태소인지 판별
        return self.word ==  other.word
    def Merge(self,other): # 병합하기
        if self.IsEqual(other):
            self.ref = self.ref + other.ref
    # ref(참조 개수) 순으로 정렬할 수 있게 비교 메서드
    def __lt__(self,other):
        return self.ref>other.ref
