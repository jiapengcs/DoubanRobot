#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kr0c'

import time
import Queue
import cPickle
import task2file
from multiprocessing.managers import BaseManager
import get_user_id
import get_user_info
from login import DoubanLogin

INIT_ID = '130949863'
DELAY_TIME = 5


def manager():
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

    # create task queue and result queue
    task_queue = Queue.Queue()
    result_queue = Queue.Queue()

    # register
    BaseManager.register('get_task_queue', callable=lambda: task_queue)
    BaseManager.register('get_result_queue', callable=lambda: result_queue)

    # bound port 5000, set authkey
    manager = BaseManager(address=('', 5000), authkey='douban')
    manager.start()
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # load task file
    done = task2file.load('done.txt')
    todo = task2file.load('todo.txt')

    # initial task(if no task file)
    new = set([INIT_ID])
    todo = (todo | (new - (new & done)))
    count = 1

    try:
        while len(todo) != 0:
            try:
                # select an id_ then send it to worker's task queue
                id_ = todo.pop()
                task.put(id_)
                print '\n[+] ========  No.%d  ID: %s  ========' % (count, id_)
                print '[~] Send to task queue...'
                time.sleep(DELAY_TIME)
                new = get_user_id.get_id(id_, headers=headers, cookies=cookies)

                # set() operation, add new IDs to todo
                add = (new - (new & done))
                todo = (todo | add)
                print '[+] 新发现用户ID: %d 个' % len(add)
                print '[~] Receiving User Information...'
                data = result.get()

                # save user information to 'info.txt'
                get_user_info.write2file('info.txt', data)
                print '[+] 已将用户信息保存至: info.txt'
                # add id_ to done
                done.add(id_)
                count += 1

                # to avoid task set expanding too fast, write them to file in time
                task2file.save('todo.txt', todo)
                task2file.save('done.txt', done)

            except Exception, e:
                print e
                exit()

    finally:
        manager.shutdown()
        print '\n[+] Manager exit.'
        exit()

if __name__ == '__main__':
    manager()