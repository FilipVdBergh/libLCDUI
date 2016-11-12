#!/usr/bin/python

import Adafruit_CharLCD
import libLCDUI

lcd = Adafruit_CharLCD.Adafruit_CharLCDPlate()
ui = libLCDUI.ui(lcd, width=16, height=2)

message = libLCDUI.text(0, 8, 6, 1)
progress = libLCDUI.horizontal_position_bar(1, 8, 8, 1, 0, 50)
volume = libLCDUI.vertical_position_bar(0,0,1,2,0,50)
alert = libLCDUI.text(0, 2, 8, 1)

message.write("Test ~[NOTE]")

ui.add_widget(message)
ui.add_widget(progress)
ui.add_widget(volume)
ui.add_widget(alert)

v = 0
while True:
    v += 1
    if v > 40:
        progress.hide()
        message.hide()
    if v > 50:
        v = 0
        progress.show()
        message.show()
    progress.write(v)
    alert.write(v)
    volume.write(v)
    ui.redraw()
