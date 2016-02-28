#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kr0c'

import cPickle


def load(path):
    print '[+] 从文件加载任务: %s' % path
    try:
        with open(path, 'rb') as f:
            tmp = cPickle.load(f)
            return tmp
    except:
        print '[!] 无任务文件, 创建: %s' % path
        return set()


def save(path, data):
    with open(path, 'wb') as f:
        cPickle.dump(data, f)