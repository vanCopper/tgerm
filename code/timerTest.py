#!/usr/bin/env python  
  
  
from threading import Timer  
import time  
  
timer_interval=1  
def delayrun():  
    print 'running'  
    return

if __name__=='__main__': 
	t=Timer(timer_interval,delayrun)  
	t.start()  
	while True:  
	    time.sleep(0.1)  
	    print 'main running'  