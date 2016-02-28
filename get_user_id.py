#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kr0c'

import re
import requests


# ought to login or set cookies first
# given a user_id, return it's relative user_id(type: set)
def get_id(id_, headers, cookies, proxies=None):
    # get whole follows, but only 1st page of followers(to avoid page turning)
    url_contacts = 'http://www.douban.com/people/' + id_ + '/contacts'          # follow
    url_rev_contacts = 'http://www.douban.com/people/' + id_ + '/rev_contacts'  # follower
    pattern = re.compile(r'<dd>.*?people/(.*?)/', re.S)
    id_contacts = re.findall(pattern, requests.get(url_contacts, headers=headers, cookies=cookies, proxies=proxies).content)
    id_rev_contacts = re.findall(pattern, requests.get(url_rev_contacts, headers=headers, cookies=cookies, proxies=proxies).content)

    # combine id from contacts and rev_contacts, then return a set(user_id)
    follow = set(id_contacts)
    follower = set(id_rev_contacts)
    user_id = (follow | follower)
    print '[+] 正在获取用户社交关系...'
    print '[+] 关注:%d    粉丝: %d    朋友: %d' % (len(follow), len(follower), len(follow)+len(follower)-len(user_id))
    return user_id

if __name__ == '__main__':
    test_id = '130949863'
    get_id(test_id, None, None)