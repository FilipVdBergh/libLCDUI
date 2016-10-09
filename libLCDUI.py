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
import symbols



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
        """This clears the content lines."""
        self.displaylines = []
        for n in range(self.height):
            self.displaylines.append(' ' * self.width)

    def add_widget(self, widget):
        """This adds a widget to the UI. The widgets are drawn in the order in which they are registered.
        All widgets must be added, or they won't be drawn at all."""
        if (widget.row + widget.height <= self.height) and (widget.col + widget.width <= self.width):
            self.areas.append(widget)
            return True
        else:
            self.loglines.append("Failed to add widget %s: widget out of bounds" % (widget))
            return False

    def print_widgets(self):
        """This prints a list of all widgets to stdout. Mostly useful for debugging your interface."""
        print("All registered objects in ui:")
        for i, widget in enumerate(self.areas):
            print("%s. Type: %s; Location: r%s,c%s; Size: %sx%s." % (i + 1, type(widget), widget.row, widget.col, widget.width, widget.height))

    def print_errors(self):
        """This prints all generated errors for debugging."""
        print(self.loglines)

    def redraw(self):
        """Add  to your main loop to draw the UI"""
        self.clear()
        for widget in self.areas:
            for i, line in enumerate(widget.get_contents()):
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

    def create_character(self, position, character):
        """This function registers new characters in the memory of the LCD. The argument is a listobject from symbols.py."""
        if not(self.display is None):
            self.display.create_char(position, character)
            return True
        else:
            return False

class LCDUI_widget(object):
    """Base object for all LCDUI widgets. Do not call this directly.
    I should probably make it an abstract base class in the future."""
    def __init__(self, parent, row, col, width, height):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.parent = parent
        self.visible = True
        self.contents = []
        self.timeout = 0
        self.creationTime = time.time()

    def start_countdown(self, duration):
        self.creationTime = time.time()
        self.timeout = duration

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def write(self, *args, timeout=0):
        self.contents = []
        for i, lines in enumerate(args):
            if i >= self.height:
                break
            self.contents.append(str(lines)[0:self.width])
        self.start_countdown(timeout)

    def get_contents(self):
        if not(self.timeout == 0) and (time.time() - self.creationTime) > self.timeout:
            self.hide()
        if self.visible:
            return self.contents
        else:
            return ""

class text(LCDUI_widget):
    """Text areas are general-purpose text widgets."""
    def __init__(self, row, col, width, height):
        super(text, self).__init__(self, row, col, width, height)
        self.contents = []

class notify(LCDUI_widget):
    """Notifies are temporary widgets. Call .show to start the display timer.
    The display timer is also started on write. The timeout is in seconds."""
    def __init__(self, row, col, width, height, timeout=3):
        super(notify, self).__init__(self, row, col, width, height)
        self.timeout = timeout
        self.creationTime = time.time()

class list(LCDUI_widget):
    """Users can select options from lists. The list may be longer than the number of showable lines.
    You can write all options at once, clearing the list first. Or you can appende new options with the add_item function.
    Call move_up and move_down to move the list indicator, to make the widget respond to input. The function get_selected
    returns the currently selected item, either by name or by number."""

    def __init__(self, row, col, width, height):
        super(list, self).__init__(self, row, col, width, height)
        self.contents = []
        self.items = []
        self.listindex = 0
        self.top_item = 0

    def write(self, *args, timeout=0):
        """Adds several items at once, first clearing the list."""
        self.items = []
        for lines in args:
            self.items.append(str(lines)[0:self.width])
        self.start_countdown(timeout)
        self.make_contents()

    def add_item(self, *args):
        """Append an item to the bottom of the list."""
        for line in args:
            self.items.append(line)
        self.make_contents()

    def make_contents(self):
        """This creates the contents based on the currentl;y viewable part of the list. For internal use in this class."""
        self.contents = []
        for i in range(self.height):
            self.contents.append(self.items[self.top_item + i])
        for i, line in enumerate(self.contents):
            if i == self.listindex - self.top_item:
                self.contents[i] = "> " + line
            else:
                self.contents[i] = "  " + line

    def move_down(self, steps=1):
        """Move the indicator down one or more steps."""
        self.listindex += steps
        if self.listindex >= len(self.items):
            self.listindex = 0
            self.top_item = 0
        if self.listindex - self.top_item >= self.height:
            self.top_item += steps
        self.make_contents()

    def move_up(self, steps=1):
        """Move the indicator up one or more steps."""
        self.listindex -= steps
        if self.listindex < 0:
            self.listindex = len(self.items) - 1
            self.top_item = len(self.items) - self.height
        if self.listindex - self.top_item < 0:
            self.top_item -= steps
        self.make_contents()

    def get_selected(self, by_name = False):
        """This returns the currently selected item from the list, either by number (default) or by name."""
        if not(by_name):
            return self.listindex
        else:
            return self.items[self.listindex]

    def get_items(self):
        """Returns the items in the list widget."""
        return self.items

    def get_number_of_items(self):
        """Returns the number of items in the list widget."""
        return len(self.items)

    def get_contents(self):
        """For internal use. This overrides the standard get_contents because not all oitems are viewable in list objects."""
        if not(self.timeout == 0) and (time.time() - self.creationTime) > self.timeout:
            self.hide()
        if self.visible:
            for i, line in enumerate(self.contents):
                self.contents[i] = line[:self.width].ljust(self.width, " ")
                if i >= self.height:
                    break
            return self.contents
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
        #This code needs to be replaced to make prettier LCD-graphics based on symbols.py.
        if position_only:
            if self.horizontal_orientation:
                self.char_before_marker = "-"
            else:
                self.char_before_marker = "|"
        else:
            self.char_before_marker = "*"
        if self.horizontal_orientation:
            self.char_after_marker = "-"
        else:
            self.char_after_marker = "|"
        self.marker_char = "*"

    def write(self, current_value):
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
    """A vertical progress bar that fills up."""
    def __init__(self, row, col, width, height, current_value, max_value, reverse_direction=False):
        super(vertical_progress_bar, self).__init__(row, col, width, height, current_value, max_value, horizontal_orientation=False, reverse_direction=reverse_direction, position_only=False)

class horizontal_progress_bar(generic_progress_bar):
    """A horizontal progress bar that fills up."""
    def __init__(self, row, col, width, height, current_value, max_value, reverse_direction=False):
        super(horizontal_progress_bar, self).__init__(row, col, width, height, current_value, max_value, horizontal_orientation=True, reverse_direction=reverse_direction, position_only=False)

class vertical_position_bar(generic_progress_bar):
    """A vertical position bar draws and indicator on an interval."""
    def __init__(self, row, col, width, height, current_value, max_value, reverse_direction=False):
        super(vertical_position_bar, self).__init__(row, col, width, height, current_value, max_value,
                                                    horizontal_orientation=False, reverse_direction=reverse_direction,
                                                    position_only=True)

class horizontal_position_bar(generic_progress_bar):
    """A horizontal position bar draws and indicator on an interval."""
    def __init__(self, row, col, width, height, current_value, max_value, reverse_direction=False):
        super(horizontal_position_bar, self).__init__(row, col, width, height, current_value, max_value,
                                                      horizontal_orientation=True, reverse_direction=reverse_direction,
                                                      position_only=True)