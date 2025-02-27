import time,platform

from DrissionPage import ChromiumPage, ChromiumOptions

from DrissionPage.common import Keys

from verifycode_predict import predict_one,decode

from runTest.m_stop_screencast import stop

from runTest.m_paddleocr import fuzzy_match

from runTest.m_pyautogui import locate_all

from runTest.m_sendFlow import sendFlow

# 浏览器操作对象(执行测试步骤)
class WebDriver:
    def __init__(self,testEnv,testSet,stop_skip_event,formatLog):
        
        # 初始化页面配置
        # 如果是linux
        if platform.system() == "Linux": 
            co = ChromiumOptions()
            co.auto_port()
            co.ignore_certificate_errors(True)
            co.set_argument("--headless=new")
            co.set_argument("--no-sandbox")
            co.set_argument('--window-size', '1920,1080')
        # 如果是windows
        else:                               
            co = ChromiumOptions()
            co.auto_port()
            if testSet["runMode"] == "无头模式":
                co.set_argument('--window-size', '1920,1080')
                co.headless(True)
            else:
                co.set_argument('--start-maximized')

        # 创建页面对象
        self.page = ChromiumPage(co)
        self.testEnv = testEnv
        self.testSet = testSet
        self.stop_skip_event = stop_skip_event
        self.formatLog = formatLog
        self.mapping_action = {
            "无需定位":{"发送流量":self.sendFlow,"访问网页":self.get_url,"登录":self.login,"退出登录":self.logout,"刷新页面":self.refresh,"初始化脚本":self.tag_add_init_js,"等待":self.sleep,"选择时间":self.select_time,"断言当前页面url包含指定内容":self.assert_url_exclude,"断言当前页面url不包含指定内容":self.assert_url_not_exclude,"断言当前页面title包含指定内容":self.assert_title_exclude,"断言当前页面title不包含指定内容":self.assert_title_not_exclude},
            "文字识别":{"动作链:点击":self.xy_click,"动作链:右击":self.xy_r_click,"动作链:点击并输入":self.xy_cilck_input,"动作链:点击清空并输入":self.xy_cilck_clear_input,"动作链:输入文本":self.xy_input,"动作链:移动鼠标":self.xy_move_to,"动作链:滚动滚轮":self.xy_scroll,"动作链:单击鼠标中键":self.xy_m_click,"动作链:双击左键":self.xy_db_click,"动作链:按键":self.xy_key,"断言元素出现在页面上":self.assert_find_ele,"断言元素未出现在页面上":self.assert_not_find_ele},
            "目标检测":{"动作链:点击":self.xy_click,"动作链:右击":self.xy_r_click,"动作链:点击并输入":self.xy_cilck_input,"动作链:点击清空并输入":self.xy_cilck_clear_input,"动作链:输入文本":self.xy_input,"动作链:移动鼠标":self.xy_move_to,"动作链:滚动滚轮":self.xy_scroll,"动作链:单击鼠标中键":self.xy_m_click,"动作链:双击左键":self.xy_db_click,"动作链:按键":self.xy_key,"断言元素出现在页面上":self.assert_find_ele,"断言元素未出现在页面上":self.assert_not_find_ele},
            "绝对坐标":{"动作链:点击":self.xy_click,"动作链:右击":self.xy_r_click,"动作链:点击并输入":self.xy_cilck_input,"动作链:点击清空并输入":self.xy_cilck_clear_input,"动作链:输入文本":self.xy_input,"动作链:移动鼠标":self.xy_move_to,"动作链:滚动滚轮":self.xy_scroll,"动作链:单击鼠标中键":self.xy_m_click,"动作链:双击左键":self.xy_db_click,"动作链:按键":self.xy_key},
            "图像识别":{"动作链:点击":self.xy_click,"动作链:右击":self.xy_r_click,"动作链:点击并输入":self.xy_cilck_input,"动作链:点击清空并输入":self.xy_cilck_clear_input,"动作链:输入文本":self.xy_input,"动作链:移动鼠标":self.xy_move_to,"动作链:滚动滚轮":self.xy_scroll,"动作链:单击鼠标中键":self.xy_m_click,"动作链:双击左键":self.xy_db_click,"动作链:按键":self.xy_key,"断言图像在当前页面已出现":self.assert_find_ele,"断言图像在当前页面未出现":self.assert_not_find_ele},
            "文本": {"点击": self.tag_click, "右击": self.tag_click_right,"双击": self.tag_double_click,"点击偏移":self.tag_click_at,"点击上传":self.tag_to_upload,"点击新标签页":self.tag_for_new_tab,"点击并切换到新标签页":self.tag_for_new_tab_and_change,"输入":self.tag_input,"清空":self.tag_clear,"清空并输入":self.tag_clear_input,"拖拽":self.tag_drag,"拖拽至":self.tag_drag_to,"悬停":self.tag_hover,"设置value":self.tag_set_value,"选中":self.tag_check,"执行js代码":self.tag_run_js,"异步执行js代码":self.tag_run_async_js,"初始化脚本":self.tag_add_init_js,"滚动至元素可见":self.tag_scroll_to_see,"选择文本":self.tag_select_by_text,"移动鼠标至元素":self.tag_move_to_ele,"断言元素出现在页面上":self.assert_find_ele,"断言元素未出现在页面上":self.assert_not_find_ele},
            "ID":{"点击": self.tag_click, "右击": self.tag_click_right,"双击": self.tag_double_click,"点击偏移":self.tag_click_at,"点击上传":self.tag_to_upload,"点击新标签页":self.tag_for_new_tab,"点击并切换到新标签页":self.tag_for_new_tab_and_change,"输入":self.tag_input,"清空":self.tag_clear,"清空并输入":self.tag_clear_input,"拖拽":self.tag_drag,"拖拽至":self.tag_drag_to,"悬停":self.tag_hover,"设置value":self.tag_set_value,"选中":self.tag_check,"执行js代码":self.tag_run_js,"异步执行js代码":self.tag_run_async_js,"初始化脚本":self.tag_add_init_js,"滚动至元素可见":self.tag_scroll_to_see,"选择文本":self.tag_select_by_text,"移动鼠标至元素":self.tag_move_to_ele,"断言元素出现在页面上":self.assert_find_ele,"断言元素未出现在页面上":self.assert_not_find_ele},
            "XPATH": {"点击": self.tag_click, "右击": self.tag_click_right,"双击": self.tag_double_click,"点击偏移":self.tag_click_at,"点击上传":self.tag_to_upload,"点击新标签页":self.tag_for_new_tab,"点击并切换到新标签页":self.tag_for_new_tab_and_change,"输入":self.tag_input,"清空":self.tag_clear,"清空并输入":self.tag_clear_input,"拖拽":self.tag_drag,"拖拽至":self.tag_drag_to,"悬停":self.tag_hover,"设置value":self.tag_set_value,"选中":self.tag_check,"执行js代码":self.tag_run_js,"异步执行js代码":self.tag_run_async_js,"初始化脚本":self.tag_add_init_js,"滚动至元素可见":self.tag_scroll_to_see,"选择文本":self.tag_select_by_text,"移动鼠标至元素":self.tag_move_to_ele,"断言元素出现在页面上":self.assert_find_ele,"断言元素未出现在页面上":self.assert_not_find_ele},
            "CSS": {"点击": self.tag_click, "右击": self.tag_click_right,"双击": self.tag_double_click,"点击偏移":self.tag_click_at,"点击上传":self.tag_to_upload,"点击新标签页":self.tag_for_new_tab,"点击并切换到新标签页":self.tag_for_new_tab_and_change,"输入":self.tag_input,"清空":self.tag_clear,"清空并输入":self.tag_clear_input,"拖拽":self.tag_drag,"拖拽至":self.tag_drag_to,"悬停":self.tag_hover,"设置value":self.tag_set_value,"选中":self.tag_check,"执行js代码":self.tag_run_js,"异步执行js代码":self.tag_run_async_js,"初始化脚本":self.tag_add_init_js,"滚动至元素可见":self.tag_scroll_to_see,"选择文本":self.tag_select_by_text,"移动鼠标至元素":self.tag_move_to_ele,"断言元素出现在页面上":self.assert_find_ele,"断言元素未出现在页面上":self.assert_not_find_ele},
            "自定义":{"点击": self.tag_click, "右击": self.tag_click_right,"双击": self.tag_double_click,"点击偏移":self.tag_click_at,"点击上传":self.tag_to_upload,"点击新标签页":self.tag_for_new_tab,"点击并切换到新标签页":self.tag_for_new_tab_and_change,"输入":self.tag_input,"清空":self.tag_clear,"清空并输入":self.tag_clear_input,"拖拽":self.tag_drag,"拖拽至":self.tag_drag_to,"悬停":self.tag_hover,"设置value":self.tag_set_value,"选中":self.tag_check,"执行js代码":self.tag_run_js,"异步执行js代码":self.tag_run_async_js,"初始化脚本":self.tag_add_init_js,"滚动至元素可见":self.tag_scroll_to_see,"选择文本":self.tag_select_by_text,"移动鼠标至元素":self.tag_move_to_ele,"断言元素出现在页面上":self.assert_find_ele,"断言元素未出现在页面上":self.assert_not_find_ele}
        }
        self.mapping_key = {"ENTER":Keys.ENTER, "BACKSPACE":Keys.BACKSPACE,"ESCAPE":Keys.ESCAPE,"SPACE":Keys.SPACE,"TAB":Keys.TAB,
                  "HOME":Keys.HOME,"END":Keys.END,"INSERT":Keys.INSERT,"DELETE":Keys.DELETE, "PAGE_UP":Keys.PAGE_UP,"PAGE_DOWN":Keys.PAGE_DOWN,
                  "CTRL_A":Keys.CTRL_A,"CTRL_C":Keys.CTRL_C,"CTRL_V":Keys.CTRL_V,"CTRL_X":Keys.CTRL_X,"CTRL_Z":Keys.CTRL_Z,
                  "F1":Keys.F1,"F2":Keys.F2,"F3":Keys.F3,"F4":Keys.F4,"F5":Keys.F5,"F6":Keys.F6,"F7":Keys.F7
                  ,"F8":Keys.F8,"F9":Keys.F9,"F10":Keys.F10,"F11":Keys.F11,"F12":Keys.F12,
                  "NUMPAD0":Keys.NUMPAD0,"NUMPAD1":Keys.NUMPAD1,"NUMPAD2":Keys.NUMPAD2,"NUMPAD3":Keys.NUMPAD3,"NUMPAD4":Keys.NUMPAD4,
                  "NUMPAD5":Keys.NUMPAD5,"NUMPAD6":Keys.NUMPAD6,"NUMPAD7":Keys.NUMPAD7,"NUMPAD8":Keys.NUMPAD8,"NUMPAD9":Keys.NUMPAD9}
        self.stepdata = None


    # 执行测试步骤
    def start_step(self,stepdata):
        self.stepdata = stepdata
        self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"定位模式:"+stepdata["locatMode"]+" 动作："+stepdata["action"])
        time.sleep(self.stepdata["preSleep"])
        result = self.mapping_action[stepdata["locatMode"]][stepdata["action"]]()
        return result
    
    # 设置停止或者跳过用例
    def set_stop_skip_event(self,FailAction):
        eventAction = self.testSet.get(FailAction)
        self.formatLog.writeStepLog("WARN",self.stepdata["stepName"],eventAction)
        if eventAction == "停止测试":
            self.stop_skip_event["stop_event"].set()
        elif eventAction == "跳过用例":
            self.stop_skip_event["skipCase"] = True
        elif eventAction == "继续执行":
            ...
        else:
            self.formatLog.writeLog("ERROR","设置停止或者跳过用例错误")

    # # 获取当前鼠标坐标
    # def get_current_xyValue(self):
    #     print("当前x坐标",self.page.actions.curr_x)
    #     print("当前y坐标",self.page.actions.curr_y)
    #     return self.page.actions.curr_x,self.page.actions.curr_y

    # # 计算需要移动的xy偏移值
    # def get_move_xyValue(self,next_x,next_y):
    #     current_x,current_y = self.get_current_xyValue()
    #     move_x = next_x - current_x
    #     move_y = next_y - current_y
    #     print("需要移动的坐标",move_x,move_y)
    #     return move_x,move_y

    # 开始录屏
    def start_screencast(self):
        if self.testSet["screencastValue"] == "否":
            self.formatLog.writeLog("INFO","不进行录屏")
            return
        self.formatLog.writeLog("INFO","开始录屏")
        time.sleep(0.5)
        self.page.screencast.set_save_path('screencast')  # 设置视频存放路径
        time.sleep(0.5)
        self.page.screencast.set_mode.video_mode()  # 设置录制
        time.sleep(0.5)
        self.page.screencast.start()  # 开始录制
        time.sleep(0.5)

    # 停止录屏
    def stop_screencast(self,video_name):
        if self.testSet["screencastValue"] == "否":
            return
        self.formatLog.writeLog("INFO","停止录屏")
        try:
            time.sleep(2)
            # 修改了源库停止录屏的方法,使之能生成支持浏览器播放的视频
            stop(self.page.screencast,video_name)
        except:
            self.formatLog.writeLog("ERROR","录屏失败!!!")

    # 截屏
    def start_screenshot(self,detailReportID):
        if self.testSet["screenshotValue"] == "否":
            self.formatLog.writeLog("INFO","不进行步骤截图")
            return
        for i in range(self.testSet["screenshotRetry"]):
            try:
                self.page.get_screenshot(path="screenshot",name=detailReportID+".png")
                break
            except:
                self.formatLog.writeLog("WARN","步骤截图失败 重试:"+str(i+1))
                time.sleep(1)
                continue
        else:
            self.formatLog.writeLog("ERROR","步骤截屏失败!!!")

    # 二进制截屏
    def get_img_binary(self):
        for j in range(self.testSet["screenshotRetry"]):
            try:
                return self.page.get_screenshot(as_bytes=True)
            except:
                self.formatLog.writeStepLog("WARN",self.stepdata["stepName"],"截屏失败 重试:"+str(j))
                time.sleep(1)
                continue
        else:
            self.formatLog.writeStepLog("ERROR",self.stepdata["stepName"],"截屏失败!!!")
            raise

    # 标签 此方法用于添加初始化脚本，在页面加载任何脚本前执行。未验证
    def tag_add_init_js(self):
        print("初始化脚本 开发中")
        # self.page.add_init_js()
        return True

    # tcpreplay发送流量
    def sendFlow(self):
        print("发送流量")
        sendFlow(hostname=self.testEnv["sendFlowHostName"],username=self.testEnv["sendFlowUserName"],password=self.testEnv["sendFlowPassWord"],command=self.stepdata["AssertOrActionValue"])
        return True

    # 睡眠
    def sleep(self):
        time.sleep(int(self.stepdata["AssertOrActionValue"]))
        return True

    # 访问网页
    def get_url(self):
        if self.stepdata["AssertOrActionValue"]:
            url = self.stepdata["AssertOrActionValue"]
        else:
            url="http://"+self.testEnv["testEnvIP"]

        try:
            self.page.get(url=url,show_errmsg=True,retry=0,timeout=10)
            return True
        except Exception as e:
            if "ERR_CERT_AUTHORITY_INVALID" in str(e):
                self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"跳过隐私页面!!!")
                self.page.ele("tag:button@text():高级").click()
                self.page.ele("继续前往").click()
                return True
            elif "ERR_CONNECTION_TIMED_OUT" in str(e):
                self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"网页访问超时 结束测试!!!")
                self.set_stop_skip_event("getUrlFailAction")
                raise
            else:
                self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"网页访问未知错误 结束测试!!!")
                self.set_stop_skip_event("getUrlFailAction")
                raise
                

    # 刷新页面
    def refresh(self):
        self.page.refresh()

    def login0(self):
        self.page.ele('tag:input@placeholder:请输入您的登录名').input(self.stepdata["AssertOrActionValue"].split("/")[0])
        self.page.ele('tag:input@placeholder:请输入您的密码').input(self.stepdata["AssertOrActionValue"].split("/")[1])
        with open ("code.png","wb") as f:
            f.write(self.page.ele('t:img').src())
        code=decode(predict_one(r'code.png','verifycode_model_20.pth'))
        self.page.ele('tag:input@placeholder=请输入验证码').input(code)
        self.page.ele('立 即 登 录').click()


    # 登录
    def login(self):
        if "网络全流量溯源" in self.page.title:
            self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"已经登录")
            return True
        for i in range(self.testSet["loginRetry"]):
            self.login0()
            if self.page.ele('登录失败',timeout=1):
                self.formatLog.writeStepLog("WARN",self.stepdata["stepName"],"登录失败 尝试再次登录"+str(i+1))
                self.refresh()
                self.login0()
            else:
                self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"登录成功")
                time.sleep(2)
                return True
        else:
            self.formatLog.writeStepLog("FAIL",self.stepdata["stepName"],"登录失败 结束测试")
            self.set_stop_skip_event("loginFailAction")
            raise

    # 退出登录
    def logout(self):
        self.page.set.cookies.clear()
        self.page.refresh()
        return True

    # 选择时间
    def select_time(self):
        Interval_time = int(self.stepdata["AssertOrActionValue"].replace("最近","").replace("分钟",""))
        starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime( time.time() - Interval_time * 60))
        endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"开始选择时间")
        self.page.ele('.^timeSliderWrap').click()
        self.page.ele('tag:input@placeholder:开始日期').input(starttime,clear=True)
        self.page.ele('tag:input@placeholder:结束日期').input(endtime,clear=True)
        self.page.ele('确 定').click()
        self.page.ele('应 用').click()
        self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"选择时间成功:"+starttime+"; "+endtime)
        return True

    # 查找元素
    def locatElement(self):
        self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"开始查找元素 定位模式:"+self.stepdata["locatMode"]+" 定位值:"+self.stepdata["locatValue"]+" 元素序号:"+str(self.stepdata["elementNumber"]))
        if self.stepdata["locatMode"] == '文本':
            self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"开始标签定位..")
            for i in range(self.testSet["locatRetry"]):
                if "输入" in self.stepdata["action"]:
                    eles = self.page.eles("tag:input@placeholder="+self.stepdata["locatValue"])
                else:
                    eles = self.page.eles(self.stepdata["locatValue"])
                if len(eles) < self.stepdata["elementNumber"]:
                    time.sleep(1)
                    self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"未找到序号为:"+str(self.stepdata["elementNumber"])+" 的元素 "+self.stepdata["locatValue"]+" 重试:"+str(i+1))
                    continue
                else:
                    return eles[self.stepdata["elementNumber"] -1]
            self.formatLog.writeStepLog("FAIL",self.stepdata["stepName"],"未找到元素")
            return
        ################################
        locatMode =self.stepdata["locatMode"].replace("ID","#").replace("XPATH","xpath:").replace("CSS","css:").replace("自定义","")
        if locatMode in ['#','xpath:','css:','']:
            self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"开始标签定位..")
            for i in range(self.testSet["locatRetry"]):
                eles = self.page.eles(locatMode + self.stepdata["locatValue"])
                if len(eles) < self.stepdata["elementNumber"]:
                    time.sleep(1)
                    self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"未找到序号为:"+str(self.stepdata["elementNumber"])+" 的元素 "+self.stepdata["locatValue"]+" 重试:"+str(i+1))
                    continue
                else:
                    return eles[self.stepdata["elementNumber"] -1]
            self.formatLog.writeStepLog("FAIL",self.stepdata["stepName"],"未找到元素")
            return
        ################################
        if locatMode == '文字识别':
            self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"开始文字识别..")
            for i in range(self.testSet["locatRetry"]):
                xylist = fuzzy_match(img=self.get_img_binary(),text=self.stepdata["locatValue"],ocrMatch=self.testSet["ocrMatch"],formatLog=self.formatLog)
                if len(xylist) < self.stepdata["elementNumber"]:
                    time.sleep(1)
                    self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"未找到序号为:"+str(self.stepdata["elementNumber"])+" 的元素 "+self.stepdata["locatValue"]+" 重试:"+str(i+1))
                    continue
                else:
                    currentConfidence = xylist[self.stepdata["elementNumber"] -1][-1][-1]
                    yoloConfidence = float(self.testSet["yoloConfidence"]/100)
                    if currentConfidence < yoloConfidence:
                        self.formatLog.writeStepLog("WARN",self.stepdata["stepName"],"文字识别置信度不足 预期置信度:"+str(yoloConfidence)+" 当前置信度:"+str(currentConfidence))
                        continue
                    next_x = (xylist[self.stepdata["elementNumber"] -1][0][0][0] + xylist[self.stepdata["elementNumber"] -1][0][2][0])/2
                    next_y = (xylist[self.stepdata["elementNumber"] -1][0][0][1] + xylist[self.stepdata["elementNumber"] -1][0][2][1])/2
                    self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"定位到的xy坐标:"+str(next_x)+","+str(next_y)+" 当前置信度:"+str(currentConfidence))
                    return (next_x,next_y)
            self.formatLog.writeStepLog("FAIL",self.stepdata["stepName"],"未找到元素")
            return 
        ################################
        if locatMode == '目标检测':
            self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"开始目标检测..")
            for i in range(self.testSet["locatRetry"]):
                xyBoxs = locate_all(img_binary=self.get_img_binary(),image_path="yoloImages/"+self.stepdata["yoloValue"]+".jpg",confidence=float(self.testSet["yoloConfidence"]/100),formatLog=self.formatLog,distance=10)
                if len(xyBoxs) < self.stepdata["elementNumber"]:
                    time.sleep(1)
                    self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"未找到序号为:"+str(self.stepdata["elementNumber"])+" 的元素 "+" 重试:"+str(i+1))
                    continue
                else:
                    next_x = xyBoxs[self.stepdata["elementNumber"] -1].left + xyBoxs[self.stepdata["elementNumber"] -1].width/2
                    next_y = xyBoxs[self.stepdata["elementNumber"] -1].top + xyBoxs[self.stepdata["elementNumber"] -1].height/2
                    self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"定位到的xy坐标:"+str(next_x)+","+str(next_y))
                    return (next_x,next_y)
            self.formatLog.writeStepLog("FAIL",self.stepdata["stepName"],"未找到元素")
            return 
        ################################
        if locatMode == '绝对坐标':
            self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"开始定位绝对坐标..")
            next_x = self.stepdata["xValue"]
            next_y = self.stepdata["yValue"]
            self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"定位到的xy坐标:"+str(next_x)+","+str(next_y))
            time.sleep(1)
            return (next_x,next_y)
        ################################
        if locatMode == '图像识别':
            self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"开始图像识别..")
            for i in range(self.testSet["locatRetry"]):
                xyBoxs = locate_all(img_binary=self.get_img_binary(),image_path="locatImages/"+self.stepdata["stepID"]+".png",confidence=float(self.testSet["imgConfidence"]/100),formatLog=self.formatLog,distance=10)
                if len(xyBoxs) < self.stepdata["elementNumber"]:
                    time.sleep(1)
                    self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"未找到序号为:"+str(self.stepdata["elementNumber"])+" 的元素 "+" 重试:"+str(i+1))
                    continue
                else:
                    next_x = xyBoxs[self.stepdata["elementNumber"] -1].left + xyBoxs[self.stepdata["elementNumber"] -1].width/2
                    next_y = xyBoxs[self.stepdata["elementNumber"] -1].top + xyBoxs[self.stepdata["elementNumber"] -1].height/2
                    self.formatLog.writeStepLog("INFO",self.stepdata["stepName"],"定位到的xy坐标:"+str(next_x)+","+str(next_y))
                    return (next_x,next_y)
            self.formatLog.writeStepLog("FAIL",self.stepdata["stepName"],"未找到元素")
            return 
        ################################
        self.formatLog.writeStepLog("ERROR",self.stepdata["stepName"],"未知的定位方式")
        raise "未知的定位方式"

    

##################################################################################

    # 标签 用于左键点击元素
    def tag_click(self):
        self.locatElement().click()
        return True
    
    # 标签 此方法实现右键单击元素。
    def tag_click_right(self):
        self.locatElement().click.right()
        return True

    # 标签 此方法实现左键多次点击元素。未验证
    def tag_double_click(self):
        self.locatElement().click.multi(2)
        return True

    # 标签 此方法用于带偏移量点击元素，偏移量相对于元素左上角坐标。不传入offset_x和offset_y时点击元素中间点。
    def tag_click_at(self):
        self.locatElement().click.at(int(self.stepdata["xValue"]),int(self.stepdata["yValue"]))
        return True

    # 标签 此方法用于点击元素，触发文件选择框并把指定的文件路径添加到网页
    def tag_to_upload(self):
        self.locatElement().click.to_upload("testFile/"+self.stepdata["AssertOrActionValue"])
        return True
    
    # 标签 在预期点击后会出现新 tab 的时候，可用此方法点击，会等待并返回新 tab 对象。
    def tag_for_new_tab(self):
        self.locatElement().click.for_new_tab()
        return True

    # 标签 在预期点击后会出现新 tab 的时候，可用此方法点击，会等待并返回新 tab 对象并切换到新的tag对象。
    def tag_for_new_tab_and_change(self):
        newtab = self.locatElement().click.for_new_tab()
        self.page = newtab
        return True

    # 标签 此方法用于清空元素文本，可选择模拟按键或 js 方式。
    def tag_clear(self):
        self.locatElement().clear()
        return True

    # 标签 此方法用于向元素输入文本或组合键，也可用于输入文件路径到上传控件。
    def tag_input(self):
        self.locatElement().input(self.stepdata["AssertOrActionValue"])
        return True
    
    # 标签 此方法用于输入前是否清空元素。
    def tag_clear_input(self):
        self.locatElement().input("AssertOrActionValue",clear=True)
        return True
    
    # #  标签 使用组合键或要传入特殊按键前，先要导入按键类Keys。
    # def tag_click_at(self):
    #     self.page.input((Keys.CTRL, 'a', Keys.DEL))

    # 标签 此方法用于拖拽元素到相对于当前的一个新位置，可以设置速度。未验证
    def tag_drag(self):
        self.locatElement().drag(1,1,1)
        return True

    # 标签 此方法用于拖拽元素到另一个元素上或一个坐标上。未验证
    def tag_drag_to(self):
        self.locatElement().drag_to()
        return True
    
    # 标签 此方法用于模拟鼠标悬停在元素上，可接受偏移量，偏移量相对于元素左上角坐标。不传入offset_x和offset_y值时悬停在元素中点。
    def tag_hover(self):
        self.locatElement().hover()
        return True
    
    # 标签 此方法用于设置元素value值。js控制的标签可能失效
    def tag_set_value(self):
        print("开发中")
        # self.locatElement().set.value()
        return True
      
    # 标签 此方法用于选中或取消选中元素。未验证
    def tag_check(self):
        print("开发中")
        # self.locatElement().check()
        return True
    
    # 标签 此方法用于对元素执行 js 代码，代码中用this表示元素自己。
    def tag_run_js(self):
        self.locatElement().run_js(self.stepdata["AssertOrActionValue"])
        return True

    # 标签 此方法用于以异步方式执行 js 代码，代码中用this表示元素自己。
    def tag_run_async_js(self):
        self.locatElement().run_async_js(self.stepdata["AssertOrActionValue"])
        return True

    # 标签 此方法用于滚动页面直到元素可见。
    def tag_scroll_to_see(self):
        self.locatElement().scroll.to_see()
        return True
    
    # 标签 此方法用于按文本选择列表项。如为多选列表，可多选。只能对select标签操作
    def tag_select_by_text(self):
        print("开发中")
        return True
        # self.locatElement().select.by_text()
    

    # 坐标 移动鼠标至元素
    def tag_move_to_ele(self):
        self.page.actions.move_to(self.locatElement())
        return True



################################################################################


    # 坐标 点击
    def xy_click(self):
        self.page.actions.move_to(self.locatElement()).click()
        return True

    # 坐标 点击并输入
    def xy_cilck_input(self):
        self.page.actions.move_to(self.locatElement()).click().input(self.stepdata["AssertOrActionValue"])
        return True
    
    # 坐标 输入文本
    def xy_input(self):
        self.page.actions.move_to(self.locatElement()).input(self.stepdata["AssertOrActionValue"])
        return True
    
    # 坐标 点击清空并输入
    def xy_cilck_clear_input(self):
        self.page.actions.move_to(self.locatElement()).click()
        self.page.actions.type(Keys.CTRL_A)
        self.page.actions.type(Keys.BACKSPACE)
        self.page.actions.input(self.stepdata["AssertOrActionValue"])
        return True

    # 坐标 移动鼠标坐标
    def xy_move_to(self):
        self.page.actions.move_to(self.locatElement())
        return True
    
    # 坐标 滚动滚轮
    def xy_scroll(self):
        self.page.actions.scroll(self.stepdata["xValue"],self.stepdata["yValue"])
        return True
    
    # 坐标 右击
    def xy_r_click(self):
        self.page.actions.move_to(self.locatElement()).r_click()
        return True
    
    # 坐标 单击鼠标中键
    def xy_m_click(self):
        self.page.actions.move_to(self.locatElement()).m_click()
        return True

    # 坐标 双击鼠标左键
    def xy_db_click(self):
        self.page.actions.move_to(self.locatElement()).db_click()
        return True

   # 坐标 按键
    def xy_key(self):
        self.page.actions.type(self.mapping_key[self.stepdata["AssertOrActionValue"]])
        return True


####################################断言##############################################

    # 无需定位 断言 此方法用于等待 url 变成包含指定文本。
    def assert_url_exclude(self):
        return self.page.wait.url_change(text=self.stepdata["AssertOrActionValue"],exclude=False)

    
    # 无需定位 断言 此方法用于等待 url 变成不包含指定文本。
    def assert_url_not_exclude(self):
        return self.page.wait.url_change(text=self.stepdata["AssertOrActionValue"],exclude=True)

    
    # 无需定位 断言 此方法用于等待 title 变成包含指定文本。
    def assert_title_exclude(self):
        return self.page.wait.title_change(text=self.stepdata["AssertOrActionValue"],exclude=False)

    # 无需定位 断言 此方法用于等待 title 变成不包含指定文本。
    def assert_title_not_exclude(self):
        return self.page.wait.title_change(text=self.stepdata["AssertOrActionValue"],exclude=True)


    # 标签 断言 定位元素在当前页面出现
    def assert_find_ele(self):
        if self.locatElement():
            return True
        else:
            return False
        
    # 标签 断言 定位元素在当前页面未出现
    def assert_not_find_ele(self):
        if self.locatElement():
            return False
        else:
            return True

