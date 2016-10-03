# libLCDUI aims to ease UI creation for character LCDs.
# Written by Filip van den Bergh.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time

class ui(object):
    """Basic ui object. This object contains all drawable widgets and is responsible for the draw action."""
    def __init__(self, display=None, width=20, height=4, rgb=(1.0, 1.0, 1.0), log=False):
        self.display = display
        self.areas = []
        self.rgb = rgb
        self.width = width
        self.height = height
        self.log = log
        self.loglines = []
        self.displaylines = []
        self.clear()

    def clear(self):
        self.displaylines = []
        for n in range(self.height):
            self.displaylines.append(' ' * self.width)

    def add_widget(self, widget):
        if (widget.row + widget.height <= self.height) and (widget.col + widget.width <= self.width):
            self.areas.append(widget)
            return True
        else:
            self.loglines.append("Failed to add widget %s: widget out of bounds" % (widget))
            return False

    def print_widgets(self):
        print("All registered objects in ui:")
        for i, widget in enumerate(self.areas):
            print(i + 1, widget.get_type())

    def print_errors(self):
        print(self.loglines)

    def redraw(self):
        self.clear()
        for widget in self.areas:
            for i, line in enumerate(widget.get()):
                if i >= self.height:
                    #This ensures that no lines are written beyond the capacity of the defined lcd
                    break
                self.displaylines[widget.row+i] = self.displaylines[widget.row+i][:widget.col] + line + self.displaylines[widget.row+i][widget.col+len(line):]
        if self.display == None:
            print("Output to stdout:")
            for line in self.displaylines:
                print("|", line[:self.width], "|")

    def input_event(self, event):
        pass

class LCDUI_widget(object):
    """Base object for all LCDUI widgets."""
    def __init__(self, parent, row, col, width, height):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.parent = parent
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def get_type(self):
        return "%s" % (type(self))

    def write(self, *args):
        self.contents = []
        for lines in args:
            self.contents.append(lines)

    def get(self):
        if self.visible:
            for i, line in enumerate(self.contents):
                self.contents[i] = line[:self.width].ljust(self.width, " ")
            return self.contents
        else:
            return ""

class text(LCDUI_widget):
    """Areas are general-purpose displays without a timeout timer."""
    def __init__(self, row, col, width, height):
        super(text, self).__init__(self, row, col, width, height)
        self.contents = []

class notify(LCDUI_widget):
    """Notifies are temporary widgets. Call .show to start the display timer."""
    def __init__(self, row, col, width, height, timeout=0, type=0):
        super(notify, self).__init__(self, row, col, width, height)
        self.timeout = timeout
        self.type = type
        self.contents = []
        self.creationTime = time.time()

    def write(self, *args):
        self.contents = []
        for lines in args:
            self.contents.append(lines)
        self.show()

    def show(self):
        self.creationTime = time.time()

    def get(self):
        if (time.time() - self.creationTime) < self.timeout:
            for i, line in enumerate(self.contents):
                self.contents[i] = line[:self.width].ljust(self.width, " ")
            return self.contents
        else:
            return ""

class list(LCDUI_widget):
    pass
