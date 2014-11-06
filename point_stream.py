#!/usr/bin/python
import pyglet
from pyglet.gl import *
import collections
from threading import Thread
import time
import sys
import re

queue = collections.deque()

header = sys.stdin.readline().split(" ")
if len(header) < 1:
    sys.stderr.write("The first line of must start with either the string '2d' or '3d'\n")
    sys.stderr.flush()
    sys.exit(1)

header = [item.strip() for item in header]
if header[0] == "2d":
    num_dimensions = 2
elif header[0] == "3d":
    num_dimensions = 3
else:
    sys.stderr.write("The first line of must start with either the string '2d' or '3d'\n")
    sys.stderr.flush()
    sys.exit(1)

hw, hh = 1, 1
if len(header) >= 3:
    hw = float(header[1])
    hh = float(header[2])

window = pyglet.window.Window()
#event_loop = pyglet.app.EventLoop()

points = []

@window.event
def on_draw():
    global points

    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-hw, hw, -hh, hh, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPointSize(5)
    
    glLoadIdentity()
    try:
        points = queue.pop()
    except IndexError:
        pass
    if points == "done":
        sys.exit(0)

    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()
    
number = re.compile(r"-?\d+(.\d*)?")
def populate_queue(queue):
    while True:
        line = sys.stdin.readline().strip()
        if line == "done" or line == "\0":
            queue.append("done")
            sys.exit(0)

        line = (line.replace("(", "").replace(")", "")
                .replace("'", "").split(" "))
        points = []
        for i in range(0, len(line), 2):
            try:
                x = float(line[i])
                y = float(line[i+1])
            except:
                break
            point = (x, y)
                     
            points.append(point)

        queue.clear()
        queue.append(points)
    
worker = Thread(target=populate_queue, args=(queue,))

worker.setDaemon(True)
worker.start()

while True:
    pyglet.clock.tick()

    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()
    time.sleep(1.0/120)
