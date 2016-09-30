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
    def __init__(self, display, dim=(4, 20), rgb=(1.0, 1.0, 1.0), log=False):
        """Initialize the user interface. It requires an Adafruit_charLCD object.
        Most of the functions provided by libLCDUI are just ways to print to this
        object."""

        self.display = display
        self.areas = []
        self.notifys = []
        self.rgb = rgb
        self.dim = dim
        self.log = log
        self.loglines = []

        self.displaylines = []
        for n in range(dim[0]):
            self.displaylines.append('')

    def add_widget(self, widget):
        if type(widget) == text:
            self.areas.append(widget)
        elif type(widget) == notify:
            self.notifys.append(widget)
        else:
            if self.log:
                self.loglines.append("Error: Tried to register an illegal object")

    def print_widgets(self):
        print("Areas:")
        for i, widget in enumerate(self.areas):
            print(i + 1, widget.getProperties())
        print("Notifications:")
        for i, widget in enumerate(self.notifys):
            print(i + 1, widget.getProperties())

    def print_errors(self):
        print(self.loglines)

    def redraw(self):
        for widget in self.areas:
            pass
        for widget in self.notifys:
            pass


class LCDUI_widget(object):
    """Base object for all LCDUI widgets."""
    def __init__(self, parent, name, posRC, sizeWH):
        self.name = name
        self.pos = posRC
        self.size = sizeWH
        self.parent = parent

    def getName(self):
        return self.name

    def getProperties(self):
        return "Type: %s, name: %s" % (type(self), self.name)


class text(LCDUI_widget):
    """Areas are general-purpose displays without a timeout timer."""
    def __init__(self, name, posRC, sizeWH):
        super(text, self).__init__(self, name, posRC, sizeWH)
        self.contents = []

    def write(self, *args):
        for lines in args:
            self.contents.append(lines)

    def get(self):
        return self.contents

class list(LCDUI_widget):
    pass

class notify(LCDUI_widget):
    """Notifies are temporary widgets placed on top of the base areas. Call .display to start the display timer."""
    def __init__(self, name, posRC, sizeWH, timeout=0, type=0):
        super(notify, self).__init__(self, name, posRC, sizeWH)
        self.timeout = timeout
        self.type = type
        self.contents = []
        self.creationTime = time.time()

    def write(self, *args):
        for lines in args:
            self.contents.append(lines)

    def display(self):
        self.creationTime = time.time()

    def get(self):
        if (time.time() - self.creationTime) < self.timeout:
            return self.contents


