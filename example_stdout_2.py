#!/usr/bin/python

import libLCDUI
import symbols
import time

ui = libLCDUI.ui(width=20, height=4)

status    = libLCDUI.text(3, 0, 20, 1)
list      = libLCDUI.list(0, 0, 20, 3)
ui.add_widget(status)
ui.add_widget(list)

list.write("Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Final option")
list.add_item("Really final")

key = ""

while True:
    time.sleep(0.1)
    if key == "":
        pass
    elif key in "uU":
        list.move_up()
    elif key in "dD":
        list.move_down()
    elif key in "gG":
        print("Got option number %s: '%s'" % (list.get_selected(False), list.get_selected(True)))
        break
    status.write("U(p) D(own) G(et):%s" % key)
    ui.redraw()
    key = input("Button?")