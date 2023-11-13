# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/07
# @File : feishu.py

import datetime
import json

import requests


def feishu_send_massage(message):
    # 私人群聊
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/548cccf2-2fa1-4c8e-a31f-f135b8e562c7"
    # url = "https://open.feishu.cn/open-apis/bot/v2/hook/46654635-7e10-4235-8ccb-5e945eca2177"
    headers = {"Content-Type": "application/json"}
    payload_message = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": "**【时间】** " + str(datetime.datetime.now().strftime('%Y-%m-%d')) + '\n' + message,
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "elements": [
                        {
                            "content": "[详情查看日志](https://testbird.feishu.cn/base/"
                                       "WY81bWh0zaTQ3JsqSxWcK5eGnRm?table=tblQb2bnWMnPIiy8&view=vewUeX9AwM)",
                            "tag": "lark_md"
                        }
                    ],
                    "tag": "note"
                }
            ],
            "header": {
                "template": "yellow",
                "title": {
                    "content": "【今日测试进度】",
                    "tag": "plain_text"
                }
            }
        }

    }

    res = requests.post(url, headers=headers, data=json.dumps(payload_message))
    print(res.json())


if __name__ == '__main__':
    message = ""
    feishu_send_massage(message)
