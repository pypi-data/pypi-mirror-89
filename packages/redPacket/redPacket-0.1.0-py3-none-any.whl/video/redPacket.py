#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 15:37:48 2020

@author: epc
"""
import time
import random
import numpy as np

class demo():
    def __init__(self):
        self.font = {}
    def number(self):
        num = ['a','b','c','d','e','f','g','h','i','j','k',
           'l','m','n','o','p','q','r','s','t','u','v',
           'w','x','y','z']
        return num

    def redPacket(self):
        money = int(input('请输入红包金额：'))
        numb = int(input('请输入红包个数（最多26个）：'))
        t1 = time.time()
        for i in range(numb - 1):
            value = np.round(money * random.random() , 2)
            self.font.update({self.number()[i]:value})
            last = money - np.sum(list(self.font.values()))
            self.font.update({self.number()[numb - 1]:last})
            epoch = 1
        while last < 0:
            self.font.clear()
            for i in range(numb - 1):
                value = np.round(money * random.random() , 2)
                self.font.update({self.number()[i]:value})
            epoch += 1
            last = money - np.sum(list(self.font.values()))
            self.font.update({self.number()[numb - 1]:last})
            #print(self.font)
        t2 = time.time() - t1
        for k , v in self.font.items():
            print('{}得到{:.2f}元'.format(k , v))
        print('经过{}轮计算，共耗时{:.2f}s，红包已全部分发完毕！'.format(epoch , t2))
    

def game():
    redP = demo()
    redP.redPacket()
    while True:
        lab = input('是否继续游戏（按y继续，按n退出）：')
        if lab == 'y':
            redP.redPacket()
        elif lab == 'n':
            break
        else:
            print('输入错误，请重新输入......')
            lab = input('是否继续游戏（按y继续，按n退出）：')
            continue