# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/07
# @File : anchor.py

import aiohttp
import asyncio

from django.contrib import messages
from django.core.handlers import exception
from django.shortcuts import HttpResponse, redirect


async def anchor_online(request):
    try:
        headers = {
            "authority": "api.livehouse.click",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://api.livehouse.click",
            "pragma": "no-cache",
            "referer": "https://api.livehouse.click/zoom/account/anchoraccount/",
            "sec-ch-ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                          "118.0.0.0 Safari/537.36",
            "x-csrftoken": "TWo2YbgUY18zhEOQ0vyw5ADqFmCx0go2C69ZGFItbZAgOYdqUfZMPZTzJifFlBYj",
            "x-requested-with": "XMLHttpRequest"
        }
        cookies = {
            "csrftoken": "TWo2YbgUY18zhEOQ0vyw5ADqFmCx0go2C69ZGFItbZAgOYdqUfZMPZTzJifFlBYj",
            "sessionid": "oou1c5vxh0au2dc6m92ybm6l16f4bve7"
        }

        # 0 空闲   1 繁忙   2 离线
        data = {
            "acc_status": "0",
            "": ""
        }

        async def anchor_online(url):
            async with aiohttp.ClientSession() as sess:
                async with sess.post(url=url, headers=headers, cookies=cookies, data=data, ssl=False) as response:
                    page_text = await response.text()
                    print(url, page_text)

        # def done(f):
        #     msg = '批量主播上线执行失败'
        #     messages.add_message(request, messages.ERROR, msg)

        tasks = []
        uids = ['523', '526', '528', '499', '454', '61', '47', '43', '106']

        for uid in uids:
            url = f"https://api.livehouse.click/zoom/account/anchoraccount/{uid}/patch/"
            c = anchor_online(url)
            task = asyncio.ensure_future(c)
            tasks.append(task)
            # task.add_done_callback(done)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

    except exception as s:
        msg = '批量主播上线执行失败'
        messages.add_message(request, messages.ERROR, msg)
    finally:
        return redirect('home')
