#!/usr/bin/python

import libLCDUI
import time


ui = libLCDUI.ui(width=16, height=4)

timer    = libLCDUI.text(0, 0, 6, 1)
progress = libLCDUI.horizontal_position_bar(row=2,col=0,width=16,height=2,current_value=0,max_value=40,reverse_direction=False)
ui.add_widget(progress)
ui.add_widget(timer)


i=0
while True:
    ui.redraw()
    time.sleep(0.5)
    i += 1
    timer.write(" %d " % (i))
    progress.set_value(i)

