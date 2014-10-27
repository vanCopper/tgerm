#-*- coding: utf-8 -*-
#!/usr/bin/env python
from os import system
from threading import Timer  

import time 
import curses

# 初始化窗口
screen = curses.initscr()
# 使用颜色模式
curses.start_color()
# 设置配色
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
# 禁止用户窗口输入
curses.noecho()
screen.border(0)

def memory_stat():  
    mem = {}  
    f = open("/proc/meminfo")  
    lines = f.readlines()  
    f.close()  
    for line in lines:  
        if len(line) < 2: continue  
        name = line.split(':')[0]  
        var = line.split(':')[1].split()[0]  
        mem[name] = int(var)  
    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']  
    return mem  

timer_interval=1  
def run():  
    mem = memory_stat()
    
    screen.addstr(1,1, "---------Memory----------", curses.color_pair(1))
    screen.addstr(1,30, "timestamp:  " + str(time.time()), curses.color_pair(2))
    column = 2

    for (k,v) in  mem.items(): 
        screen.addstr(column, 1, k + ":" + str(v) + " kB")
        column += 1

    screen.refresh()

if __name__=='__main__': 
    while True:  
        time.sleep(timer_interval)  
        run() 
