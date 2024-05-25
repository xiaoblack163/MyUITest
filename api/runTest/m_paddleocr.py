from paddleocr import PaddleOCR

from thefuzz import fuzz

ocr = PaddleOCR(use_angle_cls=False, lang="ch",ocr_version="PP-OCRv4")  

def toOcr(img):
    result = ocr.ocr(img, cls=False)[0]
    return result


# 进行模糊匹配
def fuzzy_match(img,text,ocrMatch,formatLog):
    try:
        orcResult = toOcr(img)
        TextList = list(map(lambda x: x[1][0], orcResult))
        scorelist = [fuzz.ratio(text, s) for s in TextList]
        highest_score = max(scorelist)
        formatLog.writeLog("INFO","最高得分:"+str(highest_score))
        result = [j for score,j in zip(scorelist,orcResult) if score == highest_score]
        formatLog.writeLog("INFO","得分最高识别结果: "+str(result[0][-1]))
        if highest_score < ocrMatch:
            formatLog.writeLog("INFO","匹配结果差")
            return []
        return result
    except Exception as e:
        if "could not execute a primitive" in str(e):
            formatLog.writeLog("INFO","再次初始化文字识别")
            global ocr
            ocr = PaddleOCR(use_angle_cls=False, lang="ch",ocr_version="PP-OCRv4")
            return [] 
        else:
            formatLog.writeLog("INFO","文字识别错误:"+str(e))
            return []
        

