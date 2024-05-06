# 定位选项，传递给前端
locat_option = [
    {
        "value": '标签定位',
        "states": [
            {
                "value": '文本'
            },
            {
                "value": 'ID'
            },
            {
                "value": 'XPATH'
            },
            {
                "value": 'CSS'
            },
            {
                "value": '自定义'
            }
        ]
    },
    {
        "value": '文字识别'
    },
    {
        "value": '目标检测'
    },
    {
        "value": '绝对坐标'
    },
    {
        "value": '图像识别'
    },
    {"value": '无需定位'}
]


# 操作和断言选项，传递给前端
action_option= [
    {
        "value": '操作',
        "states": [
            {
                "value": '发送流量'
            },
            {
                "value": '访问网页'
            },
            {
                "value": '登录'
            },
            {
                "value": '点击'
            },
            {
                "value": '输入'
            },
            {
                "value": '等待'
            },
            {
                "value": '双击'
            },
            {
                "value": '刷新页面'
            },
            {
                "value": '滚动屏幕'
            },
            {
                "value": '选择时间'
            },
            {
                "value": '移动鼠标'
            },
            {
                "value": '强制点击'
            },
            {
                "value": '关闭浏览器'
            }
        ]
    },
    {
        "value": '断言',
        "states": [
            {
                "value": '元素出现在页面上'
            },
            {
                "value": '元素未出现在页面上'
            },
            {
                "value": '当前页面url包含指定内容'
            },
            {
                "value": '当前页面url不包含指定内容'
            },
            {
                "value": '图像在当前页面已出现'
            },
            {
                "value": '图像在当前页面未出现'
            },
        ]
    }
]


# find_ele	定位单个元素
# find_eles	定位多个元素
# input_	输入
# click_	点击
# select_ele	选择下拉框
# execute_js	执行js代码
# get_title	获取页面标题
# get_page	获取页面源码
# get_url	获取当前页面url
# imp_wait	设置隐式等待
# sleep_	强制等待
# refresh	刷新页面
# assert_title_include_str	断言当前页面标题包含指定内容
# assert_title_not_include_str	断言当前页面标题不包含指定内容
# assert_element_not_present	断言指定元素未出现
# assert_element_present	断言指定元素已出现
# assert_image_present	断言图像在当前页面已出现
# assert_image_not_present	断言图像在当前页面没有出现
# close_window	关闭当前页面
# kb_str	键盘方式输入字符
# kb_hotkey	键盘方式键入按键(tab/enter...)
# click_image	点击图像
# input_image	输入图像
# click_x_y	点击坐标
# scroll_screen	滚动屏幕
# double_click_	双击
# move_mouse_	移动鼠标到某个元素
# click_n	点击页面第n个元素
# select_time	选择时间
# quit_browser	关闭浏览器
