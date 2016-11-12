# This is a theme file for libLCDUI. It contains a symbol list. Each symbol is defined by a name and by two definitions.
# The first is a list that is used to create special characters for the lcd. The second is a symbol used if the output
# is redirected to stdout.
# You can create your own special characters using the Excel spreadsheet "char designer.xlsm".

name = "Erres project"
version = "2016-01"
creator = "Filip van den Bergh"

# To use a special character in a widget, write the name between ~[ and ]. It is then automatically replaced before
# writing to the display. These characters also have an ASCII-representation only used when writing to stdout.

symbol = {
    "SB_VERT_NONE" :  (" ", [17, 17, 17, 17, 17, 17, 17, 17]),
    "SB_VERT_0" :  (" ", [17,17,17,17,17,17,17,17]),
    "SB_VERT_25":  (".", [17,17,17,17,17,17,31,31]),
    "SB_VERT_50":  (".", [17,17,17,17,31,31,31,31]),
    "SB_VERT_75":  ("|", [17,17,31,31,31,31,31,31]),
    "SB_VERT_100": ("|", [31,31,31,31,31,31,31,31]),
    "SB_HORI_NONE": (" ", [0,0,0,0,0,0,0,0]),
    "SB_HORI_0":   (" ", [0,16,16,16,16,16,16,0]),
    "SB_HORI_25":  (".", [0,24,24,24,24,24,24,0]),
    "SB_HORI_50":  (".", [0,28,28,28,28,28,28,0]),
    "SB_HORI_75":  ("-", [0,30,30,30,30,30,30,0]),
    "SB_HORI_100": ("-", [0,31,31,31,31,31,31,0]),
    "PB_VERT_NONE": (" ", [18,18,18,18,18,18,18,18]),
    "PB_VERT_0":   (" ", [18,18,18,18,18,18,18,30]),
    "PB_VERT_25":  (".", [18,18,18,18,18,18,30,18]),
    "PB_VERT_50":  (".", [18,18,18,18,30,18,18,18]),
    "PB_VERT_75":  ("|", [18,18,30,18,18,18,18,18]),
    "PB_VERT_100": ("|", [30,18,18,18,18,18,18,18]),
    "PB_HORI_NONE": (" ", [0,0,31,0,0,0,31,0]),
    "PB_HORI_0":   (" ", [0,0,31,16,16,16,31,0]),
    "PB_HORI_25":  (".", [0,0,31,8,8,8,31,0]),
    "PB_HORI_50":  (".", [0,0,31,4,4,4,31,0]),
    "PB_HORI_75":  ("-", [0,0,31,2,2,2,31,0]),
    "PB_HORI_100": ("-", [0,0,31,1,1,1,31,0]),
    "NOTE":        ("#", [2, 3, 2, 14, 30, 12, 0, 31]),
    "KNOB1":       ("1", [14, 2, 8, 14, 0, 31, 8, 31]),
    "KNOB2":       ("2", [14, 2, 8, 14, 0, 31, 8, 31]),
    "KNOB3":       ("3", [14, 6, 2, 14, 0, 31, 2, 31]),
    "KNOB4":       ("4", [2, 10, 14, 2, 0, 31, 1, 31]),
    "SYNC":        ("=", [12, 18, 22, 13, 9, 6, 0, 31]),
    "HEART":       ("&", [0, 10, 31, 31, 14, 4, 0, 31]),
    "LEFT":        ("<", [0, 2, 6, 14, 30, 14, 6, 2]),
    "RIGHT":       (">", [0, 8, 12, 14, 15, 14, 12, 8]),
    "UP":          ("^", [0, 4, 4, 14, 14, 31, 31, 0]),
    "DOWN":        ("v", [0, 31, 31, 14, 14, 4, 4, 0]),
    "FOLDER":      ("+", [0, 28, 19, 17, 17, 31, 0, 31]),
    "CLOCK":       ("o", [0, 14, 21, 23, 17, 14, 0, 31]),
    "UNDEFINED":   ("?", [10, 21, 0, 21, 21, 0, 10, 21]),
    "HLINE":       ("-", [0,0,0,0,31,0,0,0]),
    "VLINE":       ("|", [4,4,4,4,4,4,4,4]),
    "INDICATOR":   ("*", [0,0,4,10,21,10,4,0])
    }