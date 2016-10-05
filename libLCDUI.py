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
                if i >= self.height :
                    #This ensures that no lines are written beyond the capacity of the defined lcd
                    break
                else:
                    self.displaylines[widget.row+i] = self.displaylines[widget.row+i][:widget.col] + line + self.displaylines[widget.row+i][widget.col+len(line):]
        if self.display is None:
            print("Output to stdout:")
            for line in self.displaylines:
                print("|", line[:self.width], "|")
        else:
            for i, line in enumerate(self.displaylines):
                self.display.set_cursor(0,i)
                self.display.message(line[:self.width])

    def input_event(self, event):
        pass

    def char(self, name):
        code = [0,14,17,1,6,4,0,4]
        if name == "vert_0":
            code = [17,17,17,17,17,17,17,17]
        elif name == "vert_25":
            code = [17,17,17,17,17,17,31,31]
        elif name == "vert_50":
            code = [17,17,17,17,31,31,31,31]
        elif name == "vert_75":
            code = [17,17,31,31,31,31,31,31]
        elif name == "vert_100":
            code = [31,31,31,31,31,31,31,31]
        elif name == "note":
            code = [2,3,2,14,30,12,0,31]
        elif name == "RE_2":
            code = [14,2,8,14,0,31,8,31]
        elif name == "RE_3":
            code = [14,6,2,14,0,31,2,31]
        elif name == "RE_4":
            code = [2,10,14,2,0,31,1,31]
        elif name == "sync":
            code = [12,18,22,13,9,6,0,31]
        elif name == "heart":
            code = [0,10,31,31,14,4,0,31]
        elif name == "left":
            code = [0,2,6,14,30,14,6,2]
        elif name == "right":
            code = [0,8,12,14,15,14,12,8]
        elif name == "up":
            code = [0,4,4,14,14,31,31,0]
        elif name == "down":
            code = [0,31,31,14,14,4,4,0]
        elif name == "empty":
            code = [0,0,0,0,0,0,0,0]
        elif name == "folder":
            code = [0,28,19,17,17,31,0,31]
        elif name == "clock":
            code = [0,14,21,23,17,14,0,31]
        elif name == "undefined":
            code = [10,21,0,21,21,0,10,21]
        else:
            code = [10,21,0,21,21,0,10,21]
        return code

    def create_character(self, position, character):
        if not(self.display is None):
            self.display.create_char(position, self.char(character))
            return True
        else:
            return False

class LCDUI_widget(object):
    """Base object for all LCDUI widgets."""
    def __init__(self, parent, row, col, width, height):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.parent = parent
        self.visible = True
        self.contents = []
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
                if i > self.height:
                    break
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
                if i > self.height:
                    break
            return self.contents
        else:
            return ""

class list(LCDUI_widget):
    """Users can select options from lists. The list may be longer than the number of showable lines."""

    def __init__(self, row, col, width, height):
        super(list, self).__init__(self, row, col, width, height)
        self.contents = []
        self.listindex = 0
        self.top_item = 0

    def write(self, *args):
        self.contents = []
        for line in args:
            self.contents.append(line)

    def add_item(self, *args):
        for line in args:
            self.contents.append(line)

    def set_listindex(self, listindex):
        self.listindex = listindex
        if self.listindex < 0:
            self.listindex = 0
        if self.listindex > len(self.contents):
            self.listindex = len(self.contents)

    def move_down(self, steps = 1):
        self.listindex = max(len(self.contents), self.listindex+1)

    def move_up(self, steps = 1):
        self.listindex = min(0, self.listindex-1)

    def select(self, by_name = False):
        if not(by_name):
            return self.listindex
        else:
            return self.contents[self.listindex]

    def get(self):
        if self.visible:
            pass
        else:
            return ""

class generic_progress_bar(LCDUI_widget):
    """A progressbar converts a value relative to a maximum value into a number of similar characters.
    The function does not support half-full characters yet."""
    def __init__(self, row, col, width, height, current_value, max_value, horizontal_orientation=True, reverse_direction=False, position_only = True):
        super(generic_progress_bar, self).__init__(self, row, col, width, height)
        self.current_value = current_value
        self.max_value = max_value
        self.horizontal_orientation = horizontal_orientation
        self.reverse_direction = reverse_direction
        self.fill = 0
        if position_only:
            self.char_before_marker = "-"
        else:
            self.char_before_marker = "*"
        self.char_after_marker = "-"
        self.marker_char = "*"

    def set_value(self, current_value):
        self.current_value = current_value
        self.contents = []
        if self.horizontal_orientation:
            self.fill = int((min(self.current_value, self.max_value) / self.max_value) * self.width)
            for _ in range(self.height):
                if not(self.reverse_direction):
                    self.contents.append((self.char_before_marker * self.fill) + self.marker_char + (self.char_after_marker * (self.width - self.fill - 1)))
                else:
                    self.contents.append((self.char_after_marker * (self.width - self.fill - 1)) + self.marker_char + (self.char_before_marker * self.fill))
        else:
            self.fill = int((min(self.current_value, self.max_value) / self.max_value) * self.height)
            if not(self.reverse_direction):
                for _ in range(self.fill):
                    self.contents.append(self.char_before_marker * self.width)
                self.contents.append(self.marker_char * self.width)
                for _ in range(self.height - self.fill - 1):
                    self.contents.append(self.char_after_marker * self.width)
            else:
                for _ in range(self.height - self.fill - 1):
                    self.contents.append(self.char_after_marker * self.width)
                self.contents.append(self.marker_char * self.width)
                for _ in range(self.fill):
                    self.contents.append(self.char_before_marker * self.width)

class vertical_progress_bar(generic_progress_bar):
    def __init__(self, row, col, width, height, current_value, max_value, reverse_direction=False):
        super(vertical_progress_bar, self).__init__(row, col, width, height, current_value, max_value, horizontal_orientation=False, reverse_direction=reverse_direction, position_only=False)

class horizontal_progress_bar(generic_progress_bar):
    def __init__(self, row, col, width, height, current_value, max_value, reverse_direction=False):
        super(horizontal_progress_bar, self).__init__(row, col, width, height, current_value, max_value, horizontal_orientation=True, reverse_direction=reverse_direction, position_only=False)

class vertical_position_bar(generic_progress_bar):
    def __init__(self, row, col, width, height, current_value, max_value, reverse_direction=False):
        super(vertical_position_bar, self).__init__(row, col, width, height, current_value, max_value,
                                                    horizontal_orientation=False, reverse_direction=reverse_direction,
                                                    position_only=True)

class horizontal_position_bar(generic_progress_bar):
    def __init__(self, row, col, width, height, current_value, max_value, reverse_direction=False):
        super(horizontal_position_bar, self).__init__(row, col, width, height, current_value, max_value,
                                                      horizontal_orientation=True, reverse_direction=reverse_direction,
                                                      position_only=True)