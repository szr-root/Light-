# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/12/08
# @File : new_feishu.py


import datetime
import json

import requests


def get_tenant_access_key():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    data = {
        "app_id": "cli_a5e31a42b17fd00b",
        "app_secret": "MvSmkpP4mNwu95ylDapfMdeRs7a7IDTB"
    }
    res = requests.post(url,data=data)
    return res.json().get('tenant_access_token')


def new_feishu_send_massage(url, done, doing, wait):
    headers = {"Content-Type": "application/json"}
    payload_message = {
        "msg_type": "interactive",
        "card": {"config": {
            "wide_screen_mode": True,
            "enable_forward": True
        },
            "header": {
                "template": "purple",
                "title": {
                    "tag": "plain_text",
                    "content": "【今日测试进度】" + str(datetime.datetime.now().strftime('%Y-%m-%d'))
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": ":DONE:**已完成** \n" + done
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": ":OnIt:**进行中**\n" + doing,
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": ":OneSecond:**暂停**\n" + wait,
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "<at id='ou_4037658cee3b5093c32f0a09d3f02dfb'>刘承杨</at> "
                                   "<at id='ou_88af1af1676296fc2a5af7b531f83112'>李小双</at> "
                                   "<at id='ou_5b4235f822555cc87870e3d563777c4d'>卢可涵</at>"
                                   " <at id='ou_93c7d0628d19b69994de0ca9d9cecd3b'>陈娟</at> ",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "elements": [
                        {
                            "content": "[详情查看测试进度表](https://testbird.feishu.cn/base/OTPdbmgCoaTPCSstsjlc9BZqn2d?"
                                       "table=tblR4fnG1hz8e1Ez&view=vewXxBNTOK&chunked=false)",
                            "tag": "lark_md"
                        }
                    ],
                    "tag": "note"
                }
            ]}
    }

    res = requests.post(url=url, headers=headers, data=json.dumps(payload_message))
    print(res.json())


def get_record(state, user_token):
    url = 'https://open.feishu.cn/open-apis/bitable/v1/apps/OTPdbmgCoaTPCSstsjlc9BZqn2d/tables/tblR4fnG1hz8e1Ez/records'
    headers = {
        'Authorization': 'Bearer ' + user_token
    }
    if state == '已完成':
        params = {
            'view_id': 'vewXxBNTOK',
            'filter': f' AND(CurrentValue.[进展]="已完成",CurrentValue.[实际完成日期]=TODAY())',
            'sort':'["重要紧急程度 ASC"]',
            'page_size': '200'
        }
    else:
        params = {
            'view_id': 'vewXxBNTOK',
            'filter': f'CurrentValue.[进展]="{state}"',
            'sort': '["重要紧急程度 ASC"]',
            'page_size': '200'
        }
    res = requests.get(url, headers=headers, params=params)
    items = res.json()['data'].get('items')
    tasks_detail = []
    if items is not None:
        for item in items:
            if item.get('fields') == '':
                continue
            if state == '已完成':
                task = item['fields'].get('任务描述')
                state = item['fields'].get('进展')
                name = ', '.join(item['fields'].get('任务执行人', ''))

                now = item['fields'].get('最新进展记录', '')
            else:
                task = item['fields'].get('任务描述')
                state = item['fields'].get('进展')
                if item['fields'].get('任务执行人', ''):
                    name = ', '.join(item['fields'].get('任务执行人', ''))
                else:
                    name = ''
                now = item['fields'].get('最新进展记录', '')
                if now:
                    now = now.replace('\n', '')

            if item['fields'].get('重要紧急程度') == 'admin':
                task = "【admin】" + task
            if state == '待开始' or state == '已停滞':
                tasks_detail.append(f'{task} ,{state}。{now}\n')
            else:
                tasks_detail.append(f'{task} ,{state}。 {now} --- {name}\n')

    return tasks_detail


def get_messages(user_token):
    doing = get_record("进行中", user_token)
    wait_todo = get_record("待开始", user_token) + get_record("已停滞", user_token)
    done = get_record("已完成", user_token)

    done_list = ''
    doing_list = ''
    wait_todo_list = ''
    if done:
        i = 1
        for item in done:
            done_list += f'{i}. {item}'
            i += 1

    if len(doing) is not None:
        i = 1
        for item in doing:
            doing_list += f'{i}. {item}'
            i += 1

    if len(wait_todo) is not None:
        i = 1
        for item in wait_todo:
            wait_todo_list += f'{i}. {item}'
            i += 1

    return done_list, doing_list, wait_todo_list


if __name__ == '__main__':
    tenant_access_token = get_tenant_access_key()

    # user_token = 'u-cqIm1x7KhcLUt0KsyPzcyYk03keQ4kNbOMw0lkyE00ma'
    # 私人群聊
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/548cccf2-2fa1-4c8e-a31f-f135b8e562c7"

    # 测试组群聊
    # url = "https://open.feishu.cn/open-apis/bot/v2/hook/46654635-7e10-4235-8ccb-5e945eca2177"

    # 大群群聊
    # url= "https://open.feishu.cn/open-apis/bot/v2/hook/cbc3f551-2292-4e04-a1bd-8ae608176263"

    done, doing, wait = get_messages(tenant_access_token)
    new_feishu_send_massage(url, done, doing, wait)
