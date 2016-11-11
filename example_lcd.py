#!/usr/bin/python

import Adafruit_CharLCD
import libLCDUI
import time

lcd = Adafruit_CharLCD.Adafruit_CharLCDPlate()
ui = libLCDUI.ui(lcd, width=16, height=2)

message = libLCDUI.text(0, 1, 15, 1)
progress = libLCDUI.horizontal_progress_bar(1, 8, 8, 1, 0, 50)
volume = libLCDUI.vertical_progress_bar(0,0,1,2,0,20)
alert = libLCDUI.text(0, 3, 8, 1)

message.write("Test of libLCDUI.")

#ui.add_widget(message)
ui.add_widget(progress)
ui.add_widget(volume)
ui.add_widget(alert)

ui.print_all_info()

i = 0
v = 0
while True:
    i += 1
    v += 1
    if v > 20:
        v = 0
    if i > 40:
        progress.hide()
    if i > 50:
        i = 0
        progress.show()
    progress.write(i)
    alert.write(i)
    volume.write(v)
    ui.redraw()
