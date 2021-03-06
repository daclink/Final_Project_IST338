# combatTest.py
import curses
import time
import locale

import enemy
import player
import combat

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

stdscr = curses.initscr()
curses.savetty() #make sure we can put the screen back the way we found it
curses.noecho() #prevent keypresses appearing on screen
curses.cbreak() #interpret input with out return
stdscr.keypad(1) #everyone loves the keypad
stdscr.clearok(1) #allow the screen to be cleared
curses.curs_set(0) #hide the caret
stdscr.border(0)

curses.start_color()

stdscr.clear()
stdscr.refresh()

minX = minX	= 0
#how far to the right we can go.
#Leaving room for messages.
maxX = maxX	= stdscr.getmaxyx()[1] -15

minY = minY	= 0
##how far down we can go
#leaving room for messages
maxY = maxY	= stdscr.getmaxyx()[0] 

startY = int(maxY*.5)
startX = int(maxX*.5)
endY   = int(maxY*.1)
endX   = int(maxX*.1)
window = curses.newwin(startY,startX,endY,endX)

# def __init__(self, name, rpg_id,char_class="generic"):
p1 = player.Player()
e1 = enemy.Enemy()

stdscr.clear()

stdscr.addstr(2,2,"Fight!")

stdscr.refresh()

# time.sleep(3)

# combat.Combat(p1,e1,window)

win2 = curses.newwin(1,1,4,4)

try:
	win2.addstr(1,1,"!")
except Exception as e:
	print e

time.sleep(2)

curses.resetty()
curses.endwin()

















