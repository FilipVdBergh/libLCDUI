#!/usr/bin/python

import libLCDUI
import theme
import time

ui = libLCDUI.ui(width=16, height=4)

#timer    = libLCDUI.text(0, 0, 6, 1)
#progress = libLCDUI.horizontal_position_bar(row=2,col=0,width=16,height=2,current_value=0,max_value=40,reverse_direction=False)
#ui.add_widget(progress)
#ui.add_widget(timer)

message  = libLCDUI.text(0, 0, 10, 3)
count    = libLCDUI.text(0, 10, 6, 2)
progress = libLCDUI.horizontal_progress_bar(3, 0, 16, 1, 0, 16)
ui.add_widget(progress)
ui.add_widget(message)
ui.add_widget(count)


i=0
while i<=16:
    ui.redraw()
    time.sleep(0.1)
    key = input("Button?")
    message.write("Key:", key)
    count.write("Count:", i)
    progress.write(i)
    i=i+1
