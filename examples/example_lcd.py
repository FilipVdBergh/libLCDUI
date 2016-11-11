#!/usr/bin/python

import Adafruit_CharLCD
import libLCDUI
import time

#lcd = Adafruit_CharLCD.Adafruit_CharLCDPlate()
#ui = libLCDUI.ui(lcd, width=16, height=2)
ui = libLCDUI.ui(width=20, height=2)

song     = libLCDUI.text(0, 0, 16, 1)
artist   = libLCDUI.text(0, 0, 18, 1)
artist.set_name("Artist")
timec    = libLCDUI.text(1, 0, 6, 1)
progress = libLCDUI.horizontal_position_bar(1, 7, 9, 1, 0, 36)
volume   = libLCDUI.horizontal_progress_bar(1, 4, 8, 1, 0, 100)
volumet  = libLCDUI.text(0, 3, 10, 2)

song.write("Take Five")
artist.write("~[NOTE] Dave Brubeck ~[NOTE] And His Jazz Masters")
timec.write("00:00")
progress.write(0)
volume.write(50)
volumet.write("  Volume:  ", "           ")

ui.add_widget(song)
ui.add_widget(timec)
ui.add_widget(progress)
ui.add_widget(artist)
ui.add_widget(volumet)
ui.add_widget(volume)

artist.start_countdown(5)
volume.hide()
volumet.hide()

ui.print_all_info()

i=0
v=50
while True:
    time.sleep(1)
    i += 1
    progress.write(i)
    timec.write(i)
    ui.redraw()
    if int(i) == 10:
        volume.start_countdown(4)
        volumet.start_countdown(4)

