import time
from DrissionPage import ChromiumPage,ChromiumOptions

from verifycode_predict import predict_one,decode


co = ChromiumOptions()
co.auto_port()
# co.ignore_certificate_errors(True)
co.set_argument('--start-maximized')
co.ignore_certificate_errors(True)
co.headless(True)
# 创建页面对象，并启动或接管浏览器
page = ChromiumPage(co)

url= 'https://10.0.0.181'
pwd = 'Machloop@24@'
model = 'model_v1.pth'

page.get(url)



n= 0
for i in range(8000):
    try:
        page.refresh()
        page.ele("#username").input("adm")
        page.ele("#password").input(pwd)
        imgbri = page.ele('t:img').src()
        with open ("code.png","wb") as f:
            f.write(imgbri)
        code=decode(predict_one(r'code.png',model))
        page.ele('tag:input@placeholder=请输入验证码').input(code)
        page.ele("立 即 登 录").click()
        if page.ele("登录失败",timeout=1):
            continue
        else:
            n+=1
            print(code,n)
            with open ("code2/"+code+".png","wb") as f:
                f.write(imgbri)
            page.set.cookies.clear()
    except:
        page.quit()
        page = ChromiumPage(co)
        page.get(url)


            
