#!/usr/bin/python
import time
import sys
from math import sin, cos

print("2d 1.5 1.5")
for i in range(1000):
    theta = i/180.0*3.141592654
    for i in range(100):
        print str(sin(3*theta+i)), str(cos(5*theta+i)),
    print
    sys.stdout.flush()
    time.sleep(0.01)
print("done")
