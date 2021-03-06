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
import re
import theme

left = 0
right = 1
center = 2
scroll = False

class character_register_manager(object):
    """Manages the register of special characters in the LCD. My LCD has 8 slots available for special characters. These
    special characters are defined by a list in the theme.py file. """
    def __init__(self, display, number_of_characters=8):
        self.number_of_slots = number_of_characters
        self.character_names = []
        self.character_codes = []
        self.character_ages = []
        self.escape_codes = {
            0: "\x00",
            1: "\x01",
            2: "\x02",
            3: "\x03",
            4: "\x04",
            5: "\x05",
            6: "\x06",
            7: "\x07"
        }
        self.character_age_counter = 0
        self.display = display

    def add_character(self, character_name, character_code):
        """Add a character to the special character register of the display. This function manages the limited number
        of available slots for special characters by using information on which characters were used last and which
        can be swapped from memory. Optimization of this function probably has a lot of effects on the UI, because
        writing to the LCD memory seems slow."""
        self.character_age_counter += 1
        if character_name in self.character_names:
            self.character_ages[self.character_names.index(character_name)] = self.character_age_counter
        else:
            if len(self.character_names) >= self.number_of_slots:
                new_position = self.character_ages.index(min(self.character_ages))
            else:
                new_position = len(self.character_names)
                self.character_names.append(1)
                self.character_codes.append(1)
                self.character_ages.append(1)
            self.character_names[new_position] = character_name
            self.character_codes[new_position] = character_code
            self.character_ages[new_position] = self.character_age_counter
            self.display.create_char(new_position, self.character_codes[new_position])
        if max(self.character_ages) > self.number_of_slots + 100:
            # Reset the ages so no overflow occurs
            sorted_ages = sorted(self.character_ages)
            for n, i in enumerate(self.character_ages):
                self.character_ages[n] = sorted_ages.index(i)
            self.character_age_counter = self.number_of_slots + 1

    def length(self):
        return len(self.character_names)

    def get_escape_code(self, character):
        return self.escape_codes[self.character_names.index(character)]

    def get_slot(self, character):
        return self.character_names.index(character)

    def get_character(self, slot):
        return self.character_names[slot]

    def get_code(self, character):
        return self.character_codes[self.character_names.index(character)]

    def print_register(self):
        for i, character in enumerate(self.character_names):
            print("Slot %s, character name %s, code %s, age %s" % (i, character, self.character_codes[i], self.character_ages[i]))

class ui(object):
    """Basic ui object. This object contains all drawable widgets and is responsible for the draw action."""
    def __init__(self, display=None, width=20, height=4, rgb=(1.0, 1.0, 1.0)):
        self.display = display
        self.widgets = []
        self.rgb = rgb
        self.intensity = 0
        self.width = width
        self.height = height
        self.loglines = []
        self.displaylines = []
        self.current_displaylines = []
        self.optimize_redraw = False
        self.clear()
        self.number_of_character_memory_slots = 8
        self.theme_stdout = 0
        self.theme_display = 1
        self.register = character_register_manager(self.display, self.number_of_character_memory_slots)

    def clear(self):
        """Clear all content lines from the UI. The UI-object manages clearing the display itself."""
        self.displaylines = []
        for n in range(self.height):
            self.displaylines.append(' ' * self.width)

    def add_widget(self, widget, row, col):
        """Add a widget to the UI. The widgets are drawn in the order in which they are registered.
        Widget objects are first created, and then added to the UI-object."""
        widget.row = row
        widget.col = col
        if (widget.row + widget.height <= self.height) and (widget.col + widget.width <= self.width):
            self.widgets.append(widget)
            return True
        else:
            self.loglines.append("Failed to add widget %s: widget out of bounds" % (widget))
            return False

    def remove_widget(self, widget_name):
        """Remove a widget from the UI widget list. To remove a widget, it needs to have a proper name. You can
        give widgets names during creation by adding name=..., or you can set a name later by calling widget.set_name().
        Note that this doesn't delete the object itself, it just takes it from the UI widget list. You can add it to
        the list again later."""
        reply = False
        for i, widget in enumerate(self.widgets):
            if widget.name == widget_name:
                self.loglines.append("Deleted widget %s (%s)" % (widget.name, widget))
                del self.widgets[i]
                reply = True
        return reply

    def list_widgets(self):
        return self.widgets

    def redraw(self):
        """Redraw all widgets. Add this function to your main loop to update your display."""
        self.clear()
        for widget in self.widgets:
            for i, line in enumerate(widget.get_contents()):
                # The line is cut to the width permitted by the widget, but is also extended to allow for special characters.
                # These characters are represented by several characters, but are just a single character in the output.
                line = line[:widget.width+len(line)-self.length_of_string_with_special_characters(line)]
                if self.display is None:
                    line = self.replace_special_characters_for_stdout(line)
                else:
                    line = self.replace_special_characters_for_display(line)
                if i <= widget.height:
                    #This ensures that no lines are written beyond the capacity of the widget
                    # !! Also, if the line contains special characters, it may be cut short buy this function right now.
                    self.displaylines[widget.row+i] = self.displaylines[widget.row+i][:widget.col] + line + self.displaylines[widget.row+i][widget.col+len(line):]

        if self.display is None:
            # Because there is no lcd defined, the output goes to stdout. This draws a small frame around the output for
            # debugging purposes.
            print("*" + "-" * self.width + "*")
            for line in self.displaylines:
                print("|" + line[:self.width] + "|")
            print("*" + "-" * self.width + "*")
        else:
            if self.optimize_redraw:
                for row, line in enumerate(self.displaylines):
                    for column, character in enumerate(line):
                        if self.displaylines[row][column] != self.current_displaylines[row][column]:
                            try:
                                self.display.set_cursor(column, row)
                                self.display.message(character)
                            except:
                                print("Display error in line '%s'" % line[:self.width])
            else:
                for row, line in enumerate(self.displaylines):
                    try:
                        self.display.set_cursor(0, row)
                        self.display.message(line[:self.width])
                    except:
                        print("Display error in line '%s'" % line[:self.width])

        # Here we make a copy of the information that is currently being displayed. This helps us to compare if there
        # is any new information to be displayed.
        self.current_displaylines = self.displaylines[:]

    def enable_display(self, switch):
        self.display.enable_display(switch)

    def set_backlight(self, intensity):
        self.display.set_backlight(intensity)
        self.intensity = intensity

    def set_color(self, red, green, blue):
        self.rgb = (red, green, blue)
        self.display.set_color(red, green, blue)

    def set_optimize_redraw(self, optimize_redraw = False):
        self.optimize_redraw = optimize_redraw

    def print_widgets(self):
        """Print a list of all widgets to stdout. Mostly useful for debugging your interface."""
        for i, widget in enumerate(self.widgets):
            print("%s. %s, Type: %s; Location: r%s,c%s; Size: %sx%s. Visible=%s" % (i + 1, widget.name, type(widget), widget.row, widget.col, widget.width, widget.height, widget.visible))

    def print_theme(self):
        print("Theme name: %s, version %s" % (theme.name, theme.version))
        print("Created by %s" % theme.creator)

    def print_errors(self):
        """This prints all generated errors for debugging."""
        print(self.loglines)

    def print_all(self):
        print("LCD INFO:")
        print("Object: %s"% self.display)
        print("Size: %dx%d, special character slots: %s" % (self.height, self.width, self.number_of_character_memory_slots))
        print("-" * 40)
        print("THEME INFO:")
        self.print_theme()
        print("-" * 40)
        print("REGISTERED WIDGETS:")
        self.print_widgets()
        print("-" * 40)
        print("ERRORS:")
        self.print_errors()
        print("-" * 40)

    def length_of_string_with_special_characters(self, s):
        """Find the length of a string if it contains special characters. This is necessary so that such strings are
        not cut off. Special characters are represented by ~[...], and should be counted as a single character."""
        length_without_special_characters = len(re.sub("~\[(.*?)\]", "", s))
        number_of_special_characters_found = len(re.findall("~\[(.*?)\]", s))
        return length_without_special_characters + number_of_special_characters_found

    def replace_special_characters_for_display(self, line):
        """Replaces codes for special characters by codes the LCD can interpret. Also registers special characters from
        the theme file to the LCD memory. LCDs can generally display up to 8 special characters. If this limit is
        reached, all further special characters are replaced by question marks."""
        for match in re.findall("~\[(.*?)\]", line):
            self.register.add_character(match, theme.symbol[match][self.theme_display])
            line = line.replace("~[" + match + "]", self.register.get_escape_code(match))
        return line

    def replace_special_characters_for_stdout(self, line):
        """Replaces codes for special characters by characters for writing to stdout. """
        for match in re.findall("~\[(.*?)\]", line):
            line = line.replace("~[" + match + "]", theme.symbol[match][self.theme_stdout])
        return line

class LCDUI_widget(object):
    """Base object for all LCDUI widgets. Do not call this directly.
    I should probably make it an abstract base class in the future."""
    def __init__(self, parent, width, height, name="<name not defined>"):
        self.row = 0
        self.col = 0
        self.width = width
        self.height = height
        self.parent = parent
        self.visible = True
        self.contents = []
        self.raw_message = None
        self.timeout = 0
        self.creationTime = time.time()
        self.name = name
        self.rjust = False
        self.center = False

    def set_name(self, name):
        """Sets the name of the widget. Names are not required, but may make managing larger projects easier. The names
        of registered widgets are displayed using the ui.print_widgets function."""
        self.name = name

    def get_name(self):
        """Returns the name of a widget. By default, widgets don't have names. Names are not required, but may make
        managing larger projects easier. The names of registered widgets are displayed using the ui.print_widgets
        function."""
        return self.name

    def start_countdown(self, duration):
        """After the duration (in seconds) has expired, the widget is hidden. At the start of the timeout, widgets are
        always displayed."""
        self.creationTime = time.time()
        self.timeout = duration
        self.show()

    def show(self):
        """Shows (unhides) the widget. This does not guarantee that the widget is visible, as other widgets may be on
        top."""
        self.visible = True

    def hide(self):
        """Hides the widget by not drawing it to the buffer."""
        self.visible = False

    def write(self, message):
        """Writes information to the widget for display on the LCD. The widget manages what to do with the
        information. Text widgets just display text, but progress bars, for example, use this function to update their
        value.
        There are two ways to use this function. If you write one single string, the widget makes sure to wrap the
        lines if necessary. If you write several lines by calling the function with a list, the function writes each
        line to a new line, if the height of the widget permits as many lines."""
        self.contents = []
        if type(message) is str:
            stripped_of_special_characters = re.sub("\[(.*?)\]", "", message)
            message_left_to_process = stripped_of_special_characters
            special_characters = re.findall("\[(.*?)\]", message)
            characters_matched = 0
            for n in range(self.height):
                line_to_write = ""
                snippet = message_left_to_process[0:self.width]
                for c in snippet:
                    if c == "~":
                        if characters_matched >= len(special_characters):
                            break  # This happens if a closing bracket was not found in the message
                        c += "[%s]" % special_characters[characters_matched]
                        characters_matched += 1
                    line_to_write += c
                width_correction = len(line_to_write) - len(snippet)
                if self.rjust:
                    self.contents.append(line_to_write.rjust(self.width + width_correction, " ", ))
                elif self.center:
                    self.contents.append(line_to_write.center(self.width + width_correction, " "))
                else:
                    self.contents.append(line_to_write.ljust(self.width + width_correction, " "))
                message_left_to_process = message_left_to_process[self.width:]
        elif type(message) is int or type(message) is float:
            self.contents=[str(message)]
        else:
            for n in range(min(self.height, len(message))):
                if self.rjust:
                    self.contents.append(str(message[n]).rjust(self.width, " "))
                elif self.center:
                    self.contents.append(str(message[n]).center(self.width, " "))
                else:
                    self.contents.append(str(message[n]).ljust(self.width, " "))
        return self.contents

    def format(self, option):
        """Sets text justification. You can pass libLCDUI.left, .right or .center to justify text."""
        if option == left:
            self.rjust = False
            self.center = False
        elif option == center:
            self.rjust = False
            self.center = True
        elif option == right:
            self.rjust = True
            self.center = False

    def get_contents(self):
        """This function is used by the UI object to obtain the contents of a widget. This function also checks to see
        if the timeout of a widget has expired. Expired functions are then automatically hidden."""
        if not(self.timeout == 0) and (time.time() - self.creationTime) > self.timeout:
            self.hide()
        if self.visible:
            return self.contents
        else:
            return ""

class scrolltext(LCDUI_widget):
    """A scrolltext is a single text widget. If the line written to this widget is wider than the widget width, the text
    will scroll."""
    def __init__(self, width, height, name="<name not defined>"):
        super(scrolltext, self).__init__(self, width, height, name)
        self.contents = ""
        self.scroll_speed = 0.5
        self.pause_before_scroll = 5
        self.scroll_timer = time.time()
        self.pause_timer = time.time()
        self.scroll_position = 0

    def set_scroll_speed(self, scroll_speed):
        """Sets the speed by which the text scrolls by in jumps per second."""
        self.scroll_speed = scroll_speed

    def set_scroll_pause(self, scroll_pause):
        """Sets the time to display the start of the line before the widget starts scrolling."""
        self.pause_before_scroll = scroll_pause

    def write(self, message):
        """Sets the single text line to display inm the widget. The line may be longer than the widget width."""
        if time.time() - self.pause_timer > self.pause_before_scroll:
            if time.time() - self.scroll_timer > self.scroll_speed:
                discarded_part = message[0:self.scroll_position]
                if "~" in discarded_part:
                    self.scroll_position = message.index["]"]
                if self.scroll_position > len(re.sub("\[(.*?)\]", "", message))-(self.width/2):
                    self.scroll_position = 0
                    self.pause_timer = time.time()
                super(scrolltext, self).write(message[self.scroll_position:])
                self.scroll_position += 1
                self.scroll_timer = time.time()
        else:
            super(scrolltext, self).write(message)



class text(LCDUI_widget):
    """Text areas are general-purpose text widgets."""

    def __init__(self, width, height, name="<name not defined>"):
        super(text, self).__init__(self, width, height, name)
        self.contents = []


class notify(LCDUI_widget):
    """Notifies are temporary text widgets. Call .show to start the display timer.
    The display timer is also started on write. The timeout is in seconds. All widgets can have a timeout. This just
    class allows setting the timeout from init."""

    def __init__(self, width, height, timeout=3, name="<name not defined>"):
        super(notify, self).__init__(self, width, height, name)
        self.timeout = timeout
        self.creationTime = time.time()

class list(LCDUI_widget):
    """Users can select options from lists. The list may be longer than the number of showable lines.
    You can write all options at once, clearing the list first. Or you can appende new options with the add_item function.
    Call move_up and move_down to move the list indicator, to make the widget respond to input. The function get_selected
    returns the currently selected item, either by name or by number."""

    def __init__(self, width, height, name="<name not defined>"):
        super(list, self).__init__(self, width, height, name)
        self.contents = []
        self.items = []
        self.listindex = 0
        self.top_item = 0
        self.selected = "~[RIGHT]"
        self.not_selected = " "

    def set_indicator(self, selected, not_selected =" "):
        self.selected = selected
        self.not_selected = not_selected

    def clear(self):
        """Clears the options list."""
        self.contents = []
        self.items = []
        self.listindex = 0
        self.top_item = 0

    def write(self, *args):
        """Adds a list of several items at once, first clearing the list."""
        self.items = []
        for lines in args:
            self.items.append(str(lines)[0:self.width])
        #self.start_countdown(timeout)
        self.make_contents()

    def add_item(self, *args):
        """Append an item to the bottom of the list."""
        for line in args:
            self.items.append(line)
        self.make_contents()

    def make_contents(self):
        """This creates the contents based on the currently viewable part of the list. For internal use in this
        class."""
        self.contents = []
        for i in range(min(len(self.items), self.height)):
            self.contents.append(self.items[self.top_item + i])
        for i, line in enumerate(self.contents):
            if i == self.listindex - self.top_item:
                self.contents[i] = self.selected + line
            else:
                self.contents[i] = self.not_selected + line

    def move_down(self, steps=1):
        """Move the indicator down one or more steps. Usually, this function is called in response to a button press."""
        self.listindex += steps
        if self.listindex >= len(self.items):
            self.listindex = len(self.items)-1
            #self.listindex = 0
            #self.top_item = 0
        if self.listindex - self.top_item >= self.height:
            self.top_item += steps
        self.make_contents()

    def move_up(self, steps=1):
        """Move the indicator up one or more steps. Usually, this function is called in response to a button press."""
        self.listindex -= steps
        if self.listindex < 0:
            self.listindex = 0
            #self.listindex = len(self.items) - 1
            #self.top_item = len(self.items) - self.height
        if self.listindex - self.top_item < 0:
            self.top_item -= steps
        self.make_contents()

    def set_listindex(self, index):
        if not self.listindex == -1:
            if index > self.listindex:
                #print "index %s, listindex %s" % (index, self.listindex)
                self.move_down()
                self.set_listindex(index)
            elif index < self.listindex:
                #print "index %s, listindex %s" % (index, self.listindex)
                self.move_up()
                self.set_listindex(index)

    def get_selected(self, by_name = False):
        """This returns the currently selected item from the list, either by number (default) or by name.
        Usually, this function is called in response to a button press."""
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
        """This function is used by the UI object to obtain the contents of a widget. This overrides the standard
        get_contents of the parent object because not all items are viewable in list objects."""
        if not(self.timeout == 0) and (time.time() - self.creationTime) > self.timeout:
            self.hide()
        if self.visible:
            for i, line in enumerate(self.contents):
                self.contents[i] = line #[:self.width].ljust(self.width, " ")
                if i >= self.height:
                    break
            return self.contents
        else:
            return ""

class generic_progress_bar(LCDUI_widget):
    """A progressbar converts a value relative to a maximum value into a number of similar characters.
    The function does not support half-full characters yet."""
    def __init__(self, width, height, current_value, max_value,
                 horizontal_orientation=True, position_only = True,
                 name="<name not defined>"):
        super(generic_progress_bar, self).__init__(self, width, height, name)
        self.current_value = current_value
        self.max_value = max_value
        self.horizontal_orientation = horizontal_orientation
        self.position_only = position_only
        if self.position_only and self.horizontal_orientation:
            self.char_before_marker = "~[PB_HORI_NONE]"
            self.char_after_marker = "~[PB_HORI_NONE]"
            self.marker_char = {0: "~[PB_HORI_0]",
                                1: "~[PB_HORI_25]",
                                2: "~[PB_HORI_50]",
                                3: "~[PB_HORI_75]",
                                4: "~[PB_HORI_100]"}
        if self.position_only and not(self.horizontal_orientation):
            self.char_before_marker = "~[PB_VERT_NONE]"
            self.char_after_marker = "~[PB_VERT_NONE]"
            self.marker_char = {0: "~[PB_VERT_0]",
                                1: "~[PB_VERT_25]",
                                2: "~[PB_VERT_50]",
                                3: "~[PB_VERT_75]",
                                4: "~[PB_VERT_100]"}
        if not(self.position_only) and self.horizontal_orientation:
            self.char_before_marker = "~[SB_HORI_100]"
            self.char_after_marker = "~[SB_HORI_NONE]"
            self.marker_char = {0: "~[SB_HORI_0]",
                                1: "~[SB_HORI_25]",
                                2: "~[SB_HORI_50]",
                                3: "~[SB_HORI_75]",
                                4: "~[SB_HORI_100]"}
        if not(self.position_only) and not(self.horizontal_orientation):
            self.char_before_marker = "~[SB_VERT_100]"
            self.char_after_marker = "~[SB_VERT_NONE]"
            self.marker_char = {0: "~[SB_VERT_0]",
                                1: "~[SB_VERT_25]",
                                2: "~[SB_VERT_50]",
                                3: "~[SB_VERT_75]",
                                4: "~[SB_VERT_100]"}

    def set_maximum_value(self, maximum_value):
        self.max_value = maximum_value
        if self.current_value > self.max_value:
            self.current_value = self.max_value

    def write(self, current_value):
        self.current_value = current_value
        self.contents = []
        if self.horizontal_orientation:
            size = self.width
        else:
            size = self.height
        fraction = min(self.current_value, self.max_value) / float(self.max_value)
        fill = int(fraction * size)
        part = int((fraction * size % 1) * len(self.marker_char))
        if self.horizontal_orientation:
            for n in range(self.height):
                self.contents.append((self.char_before_marker * fill) + self.marker_char[part] +
                                     (self.char_after_marker * (self.width - fill - 1)))
        else:  # Vertical orientation
            for n in range(self.height):
                if n == (self.height - fill - 1):
                    self.contents.append(self.marker_char[part] * self.width)
                elif n < (self.height - fill - 1):
                    self.contents.append(self.char_after_marker * self.width)
                elif n > (self.height - fill - 1):
                    self.contents.append(self.char_before_marker * self.width)

class vertical_progress_bar(generic_progress_bar):
    """A vertical progress bar that fills up."""
    def __init__(self, width, height, current_value, max_value, name="<name not defined>"):
        super(vertical_progress_bar, self).__init__(width, height, current_value, max_value,
                                                    horizontal_orientation=False,
                                                    position_only=False,
                                                    name=name)

class horizontal_progress_bar(generic_progress_bar):
    """A horizontal progress bar that fills up."""
    def __init__(self, width, height, current_value, max_value, name="<name not defined>"):
        super(horizontal_progress_bar, self).__init__(width, height, current_value, max_value,
                                                      horizontal_orientation=True,
                                                      position_only=False,
                                                      name=name)

class vertical_position_bar(generic_progress_bar):
    """A vertical position bar draws and indicator on an interval."""
    def __init__(self, width, height, current_value, max_value, name="<name not defined>"):
        super(vertical_position_bar, self).__init__(width, height, current_value, max_value,
                                                    horizontal_orientation=False,
                                                    position_only=True,
                                                    name=name)

class horizontal_position_bar(generic_progress_bar):
    """A horizontal position bar draws and indicator on an interval."""
    def __init__(self, width, height, current_value, max_value, name="<name not defined>"):
        super(horizontal_position_bar, self).__init__(width, height, current_value, max_value,
                                                      horizontal_orientation=True,
                                                      position_only=True,
                                                      name=name)