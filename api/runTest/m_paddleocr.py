from paddleocr import PaddleOCR

from thefuzz import fuzz

ocr = PaddleOCR(use_angle_cls=False, lang="ch",ocr_version="PP-OCRv4")  

def toOcr(img):
    print("开始ocr")
    result = ocr.ocr(img, cls=False)[0]
    return result

# 进行模糊匹配
def fuzzy_match(img,text,formatLog):
    try:
        orcResult = toOcr(img)
        TextList = list(map(lambda x: x[1][0], orcResult))
        scorelist = [fuzz.ratio(text, s) for s in TextList]
        highest_score = max(scorelist)
        formatLog.writeLog("INFO","最高得分:"+str(highest_score))
        if highest_score < 60:
            formatLog.writeLog("INFO","匹配结果差")
            return []
        result = [j for score,j in zip(scorelist,orcResult) if score == highest_score]
        return result
    except Exception as e:
        formatLog.writeLog("INFO","文字识别错误:"+str(e))
        return []