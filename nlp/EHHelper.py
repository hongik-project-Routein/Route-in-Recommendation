class EHHelper:
    @staticmethod
    def EmitTagAndSpecialCh(str):
        str = EHHelper.RemoveTag(str)
        str = EHHelper.RemoveHtmlSpecialCh(str)
        str = EHHelper.RemoveSymbol(str)
        return str
    @staticmethod
    def RemoveTag(src):
        try:
            while True:
                s,e = EHHelper.FindTag(src)
                if s<e:
                    src = src[:s]+src[e+1:]
                else:
                    src = src[:e]+src[e+1:]
        except:
            return src
    @staticmethod
    def FindTag(src):
        s = src.index('<')
        e = src.index('>')
        return s,e
    @staticmethod
    def RemoveSymbol(src):
        dest = ""
        for elem in src:
            if str.isalpha(elem) or str.isspace(elem):
                dest+=elem
        return dest
    @staticmethod
    def RemoveHtmlSpecialCh(src):
        try:
            while True:
                s,e = EHHelper.FindHtmlSpecialCh(src)
                if s<e:
                    src = src[:s]+src[e+1:]
                else:
                    src = src[:e]+src[e+1:]
        except:
            return src
    @staticmethod
    def FindHtmlSpecialCh(src):
        s = src.index('&')
        e = src.index(';')
        return s,e
    @staticmethod
    def MssqlstrToStrKor(src):
        try:
            src = src.encode('ISO-8859-1')
            src = src.decode('euc-kr')
        except:
            return ""
        else:
            return src
