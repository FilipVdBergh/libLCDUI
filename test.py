import libLCDUI
import time

ui = libLCDUI.ui(0)

info = libLCDUI.text("Info", (0, 0), (10, 2))
volume = libLCDUI.text("Volume", (0, 11), (2, 1))
warning = libLCDUI.notify("Warning", (0,0), (10,2), 5, 0)

ui.add_widget(info)
ui.add_widget(volume)
ui.add_widget(warning)
ui.print_widgets()

warning.write("Connection Lost")
print (warning.get())

while True:
    print(warning.get())
    time.sleep(0.1)