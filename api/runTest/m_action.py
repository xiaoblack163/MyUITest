from DrissionPage import ChromiumPage
from runTest.m_stop_screencast import stop
import time


ss = ChromiumPage()


# 浏览器操作对象(执行测试步骤)
class WebDriver:
    def __init__(self,testEnv,):
        # 创建页面对象
        self.paddleOrc = None
        self.pywebgui = None
        self.yolov8 = None
        self.page = None
        self.stepdata = None
        self.testEnv = testEnv
        self.mapping_action = {
            "无需定位":{"发送流量":self.sendFlow,"访问网页":self.get_url,"登录":self.login,"刷新页面":self.refresh,"关闭浏览器":self.quit,"等待":self.sleep},
            "文字识别":{"点击":"","输入":"","双击":""},
            "目标检测":{"点击":"","输入":"","双击":""},
            "绝对定位":{"点击":"","输入":"","双击":""},
            "图像识别":{"点击":"","输入":"","双击":""},
            "文本": {"点击": self.tag_click, "输入": "", "双击": ""},
            "ID": {"点击": self.tag_click, "输入": "", "双击": ""},
            "XPATH": {"点击": self.tag_click, "输入": "", "双击": ""},
            "CSS": {"点击": self.tag_click, "输入": "", "双击": ""},
            "自定义": {"点击": self.tag_click, "输入": "", "双击": ""},
        }

    # 执行步骤操作
    def start_step(self,stepdata):
        self.stepdata = stepdata
        self.mapping_action[stepdata["locatMode"]][stepdata["action"]]()
        return True

    # 开始录屏
    def start_screencast(self):
        print("开始录屏")
        try:
            self.page.screencast.set_save_path('screencast')  # 设置视频存放路径
        except:
            print("新建页面对象")
            self.page = ChromiumPage()
            self.page.set.window.max()
            self.page.screencast.set_save_path('screencast')  # 设置视频存放路径
        self.page.screencast.set_mode.video_mode()  # 设置录制
        self.page.screencast.start()  # 开始录制

    # 停止录屏
    def stop_screencast(self,video_name):
        try:
            print("停止录屏")
            time.sleep(1.5)
            # 修改了源库停止录屏的方法,使之能生成支持浏览器播放的视频
            stop(self.page.screencast,video_name)
        except:
            print("录屏失败!!!")

    # 截屏
    def start_screenshot(self,detailReportID):
        try:
            self.page.get_screenshot(path="screenshot",name=detailReportID+".png")
        except:
            print("截屏失败!!!")

    # tcpreplay发送流量
    def sendFlow(self):
        print("发送流量")

    # 睡眠
    def sleep(self):
        time.sleep(int(self.stepdata["AssertOrActionValue"]))

    # 获取url
    def get_url0(self):
        if self.stepdata["AssertOrActionValue"]:
            return self.stepdata["AssertOrActionValue"]
        else:
            return "http://"+str(self.testEnv)
        
    # 访问网页
    def get_url(self):
        try:
            self.page.get(self.get_url0())
        except:
            print("新建页面对象")
            self.page = ChromiumPage()
            self.page.set.window.max()
            self.page.get(self.get_url0())

    # 刷新页面
    def refresh(self):
        print("刷新页面")

    # 关闭浏览器
    def quit(self):
        print("关闭浏览器")

    # 登录
    def login(self):
        print("登录")

    # 查找元素
    def locatElement(self):
        print("开始查找元素:定位模式:",self.stepdata["locatMode"]," 定位值:",self.stepdata["locatValue"])
        if self.stepdata["locatMode"] == '文本':
            try:
                ele = self.page.eles(self.stepdata["locatValue"])[self.stepdata["elementNumber"] - 1]
            except:
                ele = self.page.eles("tag:input@placeholder:"+self.stepdata["locatValue"])[self.stepdata["elementNumber"] - 1]
            return ele
        locatMode =self.stepdata["locatMode"].replace("ID","#").replace("XPATH","xpath:").replace("CSS","css:").replace("自定义","")
        if locatMode in ['#','xpath:','css:','']:
            ele = self.page.eles(locatMode + self.stepdata["locatValue"])[self.stepdata["elementNumber"] - 1]
        elif locatMode == '文字识别':
            return "文字识别元素"
        elif locatMode == '目标检测':
            return "目标检测元素"
        elif locatMode == '绝对定位':
            return "绝对定位元素"
        elif locatMode == '图像识别':
            return "图像识别元素"
        return ele
    
    # 标签 用于左键点击元素
    def tag_click(self):
        self.locatElement().click()
    
    # 标签 此方法实现右键单击元素。
    def tag_click_right(self):
        self.locatElement().click.right()

    # 标签 此方法实现左键多次点击元素。
    def double_click(self):
        self.locatElement().click.multi(2)

    # 标签 此方法用于带偏移量点击元素，偏移量相对于元素左上角坐标。不传入offset_x和offset_y时点击元素中间点。
    def tag_click_at(self):
        self.locatElement().click.at()

    # 标签 此方法用于点击元素，触发文件选择框并把指定的文件路径添加到网页
    def tag_to_upload(self):
        self.locatElement().click.to_upload()

    # 标签 在预期点击后会出现新 tab 的时候，可用此方法点击，会等待并返回新 tab 对象。
    def tag_for_new_tab(self):
        self.locatElement().click.for_new_tab()

    # 标签 此方法用于清空元素文本，可选择模拟按键或 js 方式。
    def tag_clear(self):
        self.locatElement().clear()

    # 标签 此方法用于向元素输入文本或组合键，也可用于输入文件路径到上传控件。
    def tag_input(self):
        self.locatElement().input()
    
    # 标签 此方法用于输入前是否清空元素。
    def tag_clear_input(self):
        self.locatElement().input(clear=True)
    
    # #  标签 使用组合键或要传入特殊按键前，先要导入按键类Keys。
    # def tag_click_at(self):
    #     self.page.input((Keys.CTRL, 'a', Keys.DEL))

    # 标签 此方法用于拖拽元素到相对于当前的一个新位置，可以设置速度。
    def tag_drag(self):
        self.locatElement().drag(1,1,1)

    # 标签 此方法用于拖拽元素到另一个元素上或一个坐标上。
    def tag_drag_to(self):
        self.locatElement().drag_to()
    
    # 标签 此方法用于模拟鼠标悬停在元素上，可接受偏移量，偏移量相对于元素左上角坐标。不传入offset_x和offset_y值时悬停在元素中点。
    def tag_hover(self):
        self.locatElement().hover()
    
    # 标签 此方法用于设置元素value值。
    def tag_set_value(self):
        self.locatElement().set.value()
      
    # 标签 此方法用于选中或取消选中元素。
    def tag_check(self):
        self.locatElement().check()
    
    # 标签 此方法用于对元素执行 js 代码，代码中用this表示元素自己。
    def tag_run_js(self):
        self.locatElement().run_js()

    # 标签 此方法用于以异步方式执行 js 代码，代码中用this表示元素自己。
    def tag_run_async_js(self):
        self.locatElement().run_async_js()

    # 标签 此方法用于添加初始化脚本，在页面加载任何脚本前执行。
    def tag_add_init_js(self):
        self.locatElement().add_init_js()

    # 标签 此方法用于滚动页面直到元素可见。
    def tag_scroll_to_see(self):
        self.locatElement().scroll.to_see()
    
    
    # 标签 此方法用于按文本选择列表项。如为多选列表，可多选。
    def tag_select_by_text(self):
        self.locatElement().select.by_text()

