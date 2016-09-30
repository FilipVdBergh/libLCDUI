import libLCDUI
import time

ui = libLCDUI.ui(0)

info = libLCDUI.textArea("Info", (0, 0), (10, 2))
volume = libLCDUI.textArea("Volume", (0,11), (2,1))
warning = libLCDUI.notify("Warning", (0,0), (10,2), 5, 0)

ui.register_widget(info)
ui.register_widget(volume)
ui.register_widget(warning)
ui.printRegisteredWidgets()

warning.write("Connection Lost")
print (warning.get())

while True:
    print(warning.get())
    time.sleep(0.1)