#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kr0c'

import time
import cPickle
import get_user_info
from multiprocessing.managers import BaseManager
from login import DoubanLogin

DELAY_TIME = 5
SERVER_ADDR = '127.0.0.1'
PORT = 5000


def worker():
    # load 'session.txt', or call login() to generate it
    try:
        with open('session.txt', 'rb') as f:
            headers = cPickle.load(f)
            cookies = cPickle.load(f)
    except:
        print '[-] 无session.txt文件, 调用login()...'
        session = DoubanLogin().login()
        headers = session.headers
        cookies = session.cookies

    # connect to manager
    BaseManager.register('get_task_queue')
    BaseManager.register('get_result_queue')
    print 'Connect to server %s:5000...' % server_addr
    worker = BaseManager(address=(SERVER_ADDR, PORT), authkey='douban')
    worker.connect()
    task = worker.get_task_queue()
    result = worker.get_result_queue()

    # start listening
    print '[-] Waiting...'
    while True:
        try:
            id_ = task.get()
            print '[~] Running task...'
            info = get_user_info.get_info(id_, headers=headers, cookies=cookies)
            print '[+] Information returned.\n'
            result.put(info)
            print '[-] Waiting...'
            time.sleep(DELAY_TIME)

        except Exception, e:
            print e
            exit()

    print '[+] Worker exit.'

if __name__ == '__main__':
    worker()