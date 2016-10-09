#!/usr/bin/python

import libLCDUI
import symbols
import time

ui = libLCDUI.ui(width=20, height=4)

status    = libLCDUI.text(3, 0, 18, 1)
list      = libLCDUI.list(0, 0, 18, 3)

list.write("Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Final option")
list.add_item("Really final")

position  = libLCDUI.vertical_position_bar(0,19,1,4,0,list.get_number_of_items())

ui.add_widget(status)
ui.add_widget(list)
ui.add_widget(position)

ui.print_widgets()

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
    position.write(list.get_selected())
    ui.redraw()
    key = input("Button?")