# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/10
# @File : select_device_id.py

import requests
from lxml import etree

def get_device_id_users():
    url = 'https://api.livehouse.click/zoom/account/useraccount/' \
          '?_cols=id.nickname.dev_id.uid.coin.acc_status.user_country.sex.pkg.sort_tag.update_time.create_time.' \
          'fix_dev_id&_p_fix_dev_id__contains=41b772edefd283c3'

    headers = {
    'Cookie':'csrftoken=TWo2YbgUY18zhEOQ0vyw5ADqFmCx0go2C69ZGFItbZAgOYdqUfZMPZTzJifFlBYj;'
             ' sessionid=oou1c5vxh0au2dc6m92ybm6l16f4bve7'
    }


    page = requests.get(url, headers=headers).text

    # with open('./user.txt', 'w', encoding='utf-8') as f:
    #     f.write(page.text)

    tree = etree.HTML(page)
    uid_list = tree.xpath('//form[@id="changelist-form"]//tbody/tr/td[2]/a/text()')
    real_uid_list = []
    for uid in uid_list:
        real_uid_list.append(uid.strip())
    print(real_uid_list)
    return real_uid_list


def edit_device_id(url_list):
    url = f'https://api.livehouse.click/zoom/account/useraccount/{id}/update/'
    pass


if __name__ == '__main__':
    r = get_device_id_users()