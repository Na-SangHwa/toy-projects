import curses
from curses import wrapper
import time
import random

def game_Start(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Hi! this is WPM test for time killing")
    stdscr.addstr(1, 0, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getkey()

def text_Color(c_num):
    """initial color"""
    if c_num == 1: curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    elif c_num == 2: curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   

    return curses.color_pair(c_num)

def WPM(start_Time, current_Text, target_Text):
    time_Elapse = max(time.time() - start_Time, 1)
    correct_Char = sum(1 for t, c in zip(target_Text, current_Text) if t == c ) #prevent to give wrong wpm 
    gross_Wpm = correct_Char/(time_Elapse / 60)
    net_Wpm = round(gross_Wpm/5)

    if len(current_Text) > 0: accuracy = round((correct_Char/len(target_Text)) * 100)
    else: accuracy = 0

    return net_Wpm, accuracy

def display_Text(stdscr, target_T, current_T, start_T):
    stdscr.addstr(target_T)
    net_Wpm, accuracy = WPM(start_T, current_T, target_T)
    stdscr.addstr(1, 0, f"WPM: {net_Wpm}" )
    stdscr.addstr(2, 0, f"Accuracy: {accuracy}" )
    """set color"""
    for i, char in enumerate(current_T):
        if target_T[i] != char: 
            switch_Color = text_Color(2)
        elif char == " " and target_T[i] != " ": 
            switch_Color = text_Color(2)
        else: 
            switch_Color = text_Color(1)
        """print text"""
        if char == " " and target_T[i] != " ":
            stdscr.addch(0, i, char, switch_Color | curses.A_REVERSE)
        else:
            stdscr.addstr(0, i, char, switch_Color)

def load_Text():
    with open("scripts.txt", "r") as f:
        script = f.readlines()

        return random.choice(script).strip()
    
def exceptions(input):
     if input == "\x00" or input == "\n" or input == "\t": input = ""
     elif input == "SHF_PADENTER": input = "'"
     
     return input

def WPM_test(stdscr):
    target_Text = load_Text()
    current_Text = []
    start_Time = time.time()
    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        display_Text(stdscr, target_Text, current_Text, start_Time)
        stdscr.refresh()
        
        try:
            key = exceptions(stdscr.getkey())

            if ord(key) == 27: 
                stdscr.nodelay(False)
                break
            elif "".join(current_Text) == target_Text:
                stdscr.nodelay(False)
                break

            if key in ("KEY_BACKSPACE", "\b", '\x7f') and len(current_Text) > 0: 
                current_Text.pop()
            elif len(current_Text) < len(target_Text): 
                current_Text.append(key)
        except :
            continue

        

def main(stdscr):
    game_Start(stdscr)

    while True:
        WPM_test(stdscr)
        #stdscr.clear()
        stdscr.addstr(3, 0, "Press any key to continue...")
        #stdscr.refresh()
        key = stdscr.getkey()
        if ord(key) == 27: 
            break

wrapper(main)