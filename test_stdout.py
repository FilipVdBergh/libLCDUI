import libLCDUI
import time

ui = libLCDUI.ui()


bg      = libLCDUI.text(0, 0, 20, 4)
volume  = libLCDUI.text(1, 1, 10, 2)
counter = libLCDUI.text(1, 10, 7, 2)
warning = libLCDUI.notify(1,3, 14, 2, 3, 0)


ui.add_widget(bg)
ui.add_widget(volume)
ui.add_widget(counter)
ui.add_widget(warning)

ui.print_errors()

bg.write("." * 20, "." * 20, "." * 20, "." * 20)
volume.write("Volume:", "  70%")

i=0
while True:
    ui.redraw()
    time.sleep(0.5)
    i += 1
    counter.write("Counter:", ("%d" % i).center(7, "-"))
    if i > 10:
        i = 0
        warning.write("  1 message:  ", "  > Battery low  ")
