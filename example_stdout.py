#!/usr/bin/python

import libLCDUI
import time


ui = libLCDUI.ui(width=16, height=2)

bg      = libLCDUI.text(0, 0, 16, 2)
timer   = libLCDUI.text(0, 2, 6, 2)
message = libLCDUI.notify(0, 8, 6, 2, 2)

ui.add_widget(bg)
ui.add_widget(timer)
ui.add_widget(message)

bg.write("----------------", "----------------")

i=0
while True:
    ui.redraw()
    time.sleep(0.5)
    i += 1
    timer.write("Timer:", " %d " % (i // 2))
    if i % 8 == 0:
        message.write("DIV4!")

