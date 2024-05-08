# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/14
# @File : anchor_onlie.py


import aiohttp
import asyncio
headers = {
    "authority": "api.livehouse.click",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://api.livehouse.click",
    "referer": "https://api.livehouse.click/zoom/account/anchoraccount/",
    "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "x-csrftoken": "DMGPgwRCu1xIkVf8h8HdzlFsj45ooIZ9clNybvR83DBNeqGedeTfIXhmNMtvX2wd",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "csrftoken": "DMGPgwRCu1xIkVf8h8HdzlFsj45ooIZ9clNybvR83DBNeqGedeTfIXhmNMtvX2wd",
    "sessionid": "6h4eb19athkiuc9b3h467vvkahcpa5sa"
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


tasks = []
uids = ['523', '526', '528', '499', '454', '61', '47', '43', '106', '129', '106']

for uid in uids:
    url = f"https://api.livehouse.click/zoom/account/anchoraccount/{uid}/patch/"
    c = anchor_online(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
