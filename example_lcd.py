#!/usr/bin/python

import Adafruit_CharLCD
import libLCDUI

lcd = Adafruit_CharLCD.Adafruit_CharLCDPlate()
ui = libLCDUI.ui(lcd, width=16, height=2)

message = libLCDUI.text(6, 1)
progress = libLCDUI.horizontal_position_bar(8, 1, 0, 50)
volume = libLCDUI.vertical_position_bar(1,2,0,50)
alert = libLCDUI.text(8, 2)
listtest = libLCDUI.list(10, 2)

message.write("Test ~[NOTE]")
listtest.write("Option 1", "Option 2", "Option 3", "Option 4", "Option 5")
listtest.set_indicator("~[RIGHT_SMALL]")
ui.set_color(0.2, 0.8, 0.1)

#ui.add_widget(message,0,8)
#ui.add_widget(progress,1,8)
ui.add_widget(volume,0,0)
ui.add_widget(alert,0,1)
ui.add_widget(listtest,0,4)

for widget in ui.list_widgets():
    print widget.name

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
    alert.write(["V=",v])
    volume.write(v)
    listtest.move_down()
    ui.redraw()
