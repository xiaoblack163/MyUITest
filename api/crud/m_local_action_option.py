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
    {   
        "value": '无需定位'
    }
]





# 操作和断言选项，传递给前端
locatOption_actionOption= {
        "无需定位":[
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
                        "value": '刷新页面'
                    },
                    {
                        "value": '登录'
                    },
                    {
                        "value": '退出登录'
                    },
                    {
                        "value": '等待'
                    },
                    {
                        "value": '执行js代码'
                    },
                    {
                        "value": '异步执行js代码'
                    },
                    {
                        "value": '初始化脚本'
                    },
                ]
            },
            {
                "value": '断言',
                "states": [
                    {
                        "value": '断言当前页面url包含指定内容'
                    },
                    {
                        "value": '断言当前页面url不包含指定内容'
                    },
                    {
                        "value": '断言当前页面title包含指定内容'
                    },
                    {
                        "value": '断言当前页面title不包含指定内容'
                    }
                ]
            }
        ],
        "标签定位":[
            {
                "value": '操作',
                "states": [
                    {
                        "value": '点击'
                    },
                    {
                        "value": '输入'
                    },
                    {
                        "value": '右击'
                    },
                    {
                        "value": '双击'
                    },
                    {
                        "value": '点击偏移'
                    },
                    {
                        "value": '点击上传'
                    },
                    {
                        "value": '点击出现新标签页'
                    },
                    {
                        "value": '点击并切换到新标签页'
                    },
                    {
                        "value": '清空'
                    },
                    {
                        "value": '清空并输入'
                    },
                    {
                        "value": '拖拽'
                    },
                    {
                        "value": '悬停'
                    },
                    # {
                    #     "value": '设置value'
                    # },
                    # {
                    #     "value": '选中'
                    # },
                    {
                        "value": '滚动至元素可见'
                    },
                    # {
                    #     "value": '选择文本'
                    # },
                    {
                        "value": '移动鼠标至元素'
                    }
                ]
            },
            {
                "value": '断言',
                "states": [
                    {
                        "value": '断言元素出现在页面上'
                    },
                    {
                        "value": '断言元素未出现在页面上'
                    }
                ]
            }
        ],
        "坐标定位":[
        {
            "value": '操作',
            "states": [
                {
                    "value": '动作链:点击'
                },
                {
                    "value": '动作链:点击并输入'
                },
                {
                    "value": '动作链:输入文本'
                },
                {
                    "value": '动作链:移动鼠标'
                },
                {
                    "value": '动作链:滚动滚轮'
                },
                {
                    "value": '动作链:右击'
                },
                {
                    "value": '动作链:单击鼠标中键'
                },
                {
                    "value": '动作链:双击左键'
                },
                {
                    "value": '动作链:按键'
                }
            ]
        },
        {
            "value": '断言',
            "states": [
                {
                    "value": '断言元素出现在页面上'
                },
                {
                    "value": '断言元素未出现在页面上'
                },
                {
                    "value": '断言图像在当前页面已出现'
                },
                {
                    "value": '断言图像在当前页面未出现'
                },
            ]
        }
    ]
}

# 当动作为此列表时,输入参数不能为空
checkActionValue = {"输入":"","清空并输入":"","动作链:点击并输入":"","动作链:输入文本":"","登录":"示例:\nadm/Machloop@123","点击上传":"示例:\nD:/filepath","等待":"示例:\n1","执行js代码":"示例:\nconsole.log('hello world')","异步执行js代码":"示例:\nconsole.log('hello world')","初始化脚本":"示例:\nconsole.log('hello world')","断言当前页面url包含指定内容":"",'断言当前页面url不包含指定内容':"","断言当前页面title包含指定内容":"",'断言当前页面title不包含指定内容':""}

# 当定位模式为此列表时,定位值不能为空
checkLocatValue = ["文本","ID","XPATH","CSS","自定义","文字识别","目标检测"]

# 目标检测选项
yoloOption = ["1","2","3","4","5"]
