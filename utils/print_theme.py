#!/usr/bin/python
# coding: UTF-8

import theme

def draw(character_name):
    character_code = theme.symbol[character_name][1]
    screen_symbols = ["─", "█"]
    for code in character_code:
        for i in (str(bin(code))[2:]).rjust(5, "0"):
            print screen_symbols[int(i)],
        print

i=0
for s in sorted(theme.symbol):
    i += 1
    print("%s. %s" % (i, s))
    draw(s)
    print