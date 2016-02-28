#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kr0c'

import requests
import cStringIO
import cPickle
from PIL import Image
from bs4 import BeautifulSoup


class DoubanLogin(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.douban.com/',
            'Connection': 'keep-alive',
        }
        # douban use https by default, for the sake of efficiency, I prefer http.
        self.url_login = 'http://www.douban.com/accounts/login'
        # Form Data to POST
        self.payload = {
            'form_email': 'example@email.com',
            'form_password': 'password',
            'remember': 'on'
        }

    def login(self):
        # create a session, and it'll be saved to keep connection status(headers & cookies)
        session = requests.session()
        session.headers.update(self.headers)

        # if needs captcha
        try:
            # get url_captcha, captcha-solution should be POST together with captcha_id
            login_page = BeautifulSoup(session.get(self.url_login).content, 'lxml')
            url_captcha = login_page.find('img', id='captcha_image')['src']
            captcha_id = url_captcha[38:65]

            # show captcha image
            img_buf = requests.get(url_captcha, stream=True, headers=self.headers).content
            Image.open(cStringIO.StringIO(img_buf)).show()
            print '[+] 验证码显示成功！'
            captcha_solution = raw_input('[+] 请输入验证码：\n>>> ')
            
            # add captcha-solution & captcha-id to Form Data
            self.payload['captcha-solution'] = captcha_solution
            self.payload['captcha-id'] = captcha_id
        # if no captcha
        except:
            pass

        # login and return session
        login = session.post(self.url_login, data=self.payload)
        login_code = BeautifulSoup(login.content, 'lxml').find('html')['lang']

        if login_code == 'zh-cmn-Hans':
            print '[+] 登录成功！'

            # 将session写入文件: session.txt
            with open('session.txt', 'wb') as f:
                cPickle.dump(session.headers, f)
                cPickle.dump(session.cookies.get_dict(), f)
                print '[+] 将session写入文件: session.txt'

            return session

        elif login_code == 'zh-CN':
            print '[-] 登录失败：验证码错误！'
            exit()
        else:
            print '[-] 登录异常：请重新启动程序！'
            exit()

if __name__ == '__main__':
    DoubanLogin().login()