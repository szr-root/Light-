# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2024/05/07
# @File : sendmessage.py
import random
import time
import hashlib
import requests


# api.us-light-api.com


def sha1_encrypt(message):
    sha1 = hashlib.sha1()
    sha1.update(message.encode('utf-8'))
    encrypted_msg = sha1.hexdigest()
    return encrypted_msg


anchor_id_list = ['1755328', '101454', '12779636', '1955224', '152255123', '153876', '103767', '161140', '1855519',
                  '12242285', '1073249', '184573', '1122894']


def send_message(user_id):
    timestamp = str(int(time.time()))
    app_secret = 'iOuabjpujsMTOi'
    noce = str(random.randint(100000000, 999999999))
    signature = sha1_encrypt(app_secret + noce + timestamp)
    try:
        for anchor_id in anchor_id_list:
            res = requests.post(
                url=' https://api.us-light-api.com/message/private/publish.json',
                headers={
                    'Host': 'api.us-light-api.com',
                    'App-Key': 'bmdehs6pbel8s',
                    'Nonce': noce,
                    'Timestamp': timestamp,
                    'Signature': signature,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data={'fromUserId': anchor_id, 'toUserId': user_id, 'objectName': 'RC:TxtMsg',
                      'content': '{"content":"hello,这是一条测试消息","extra":"helloExtra"}', 'isPersisted': '1',
                      'disablePush': '0'}
            )
            if res.json().get('code') != 200:
                print(anchor_id, '发送失败')
                break
    except Exception as s:
        print(s)


send_message('37750090')
