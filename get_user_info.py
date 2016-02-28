#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kr0c'

import re
import requests
from bs4 import BeautifulSoup


# given a user_id, return user's information(type: tuple)
def get_info(user_id, headers, cookies, proxies=None):
    url = 'http://www.douban.com/people/' + user_id
    soup = BeautifulSoup(requests.get(url, headers=headers, cookies=cookies, proxies=proxies).content, 'lxml')
    # nickname, city, register, book, music, movie, review, group, follow, follower
    try:
        nickname = soup.head.title.string.encode('utf-8')[1:-1]
    except:
        nickname = 'Bug'
    try:
        city = soup.body.find(class_='user-info').a.string.encode('utf-8')
    except:
        city = 'Unknown'
    try:
        register = re.findall('<br/> (.*?)加入', soup.body.find('div', 'user-info').div.encode('utf-8'))[0]
    except:
        register = '0000-00-00'
        nickname = 'Quit|Ban'
    try:
        # book = soup.body.find(id='book').find_all('a')[2].string.encode('utf-8')[:-9]    # bug
        book = soup.body.find(id='book').h2.find_all(href=re.compile('collect'))[0].string.encode('utf-8')[:-9]
    except:
        book = 0
    try:
        music = soup.body.find(id='music').h2.find_all(href=re.compile('collect'))[0].string.encode('utf-8')[:-9]
    except:
        music = 0
    try:
        movie = soup.body.find(id='movie').h2.find_all(href=re.compile('collect'))[0].string.encode('utf-8')[:-9]
    except:
        movie = 0
    try:
        review = soup.body.find(id='review').h2.a.string.encode('utf-8')[6:]
    except:
        review = 0
    try:
        group = re.findall('小组\((.*?)\)', soup.body.find(id='group').h2.encode('utf-8'))[0]
    except:
        group = 0
    try:
        follow = soup.body.find(id='friend').a.string.encode('utf-8')[6:]
    except:
        follow = 0
    try:
        follower = soup.body.find(class_='rev-link').a.string.encode('utf-8')[len(nickname)+6: -9]
    except:
        follower = 0

    user_info = (user_id, nickname, city, register, book, music, movie, review, group, follow, follower)
    print '=============  ID: %s  ==============' % user_id
    print '[+] Nickname: %s\n[+] City: %s\n[+] Register: %s\n[+] Book: %s\n[+] Music: %s\n' \
          '[+] Movie: %s\n[+] Review: %s\n[+] Group: %s\n[+] Follow: %s\n[+] Follower: %s' \
          % (nickname, city, register, book, music, movie, review, group, follow, follower)
    print '==============  User Info  ================'
    return user_info


# write user info to file
def write2file(path, data):
    with open(path, 'ab') as f:
        for item in data:
            f.write('%s   ' % item)
        f.write('\n')

if __name__ == '__main__':
    test_id = '130949863'
    tmp = get_info(test_id, None, None)
    write2file('get_info.txt', tmp)