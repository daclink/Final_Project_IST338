###
# Drew A. Clinkenbeard
# 14 - April - 2014
# e.py
# This is my scratch paper...
#
###

# from __future__ import print_function
# from time import localtime, strftime
import sys
import random
import time
import curses
import curses.textpad
import curses.panel
import locale
import random
import math
import json
from time import localtime, strftime
from inspect import currentframe, getframeinfo

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


# def boolin(cellVisited=False,retVisited=False):
# 	neighbors = {}
# 	# check north and northwest cells
# 	if True and not cellVisited or retVisited:
# 		print "cellVisited : {0} retVisited {1}".format(cellVisited, retVisited)

# boolin(True,True)
# boolin(True,False)
# boolin(False,True)
# boolin(False,False)



# def tester(x):
# 	print "great scott! ", x


# foo = {1:"cake!","fun!":"tester()","def":tester}

# print foo['fun!']


# foo['def']

# import curses 

# screen = curses.initscr()

# try:
#     screen.border(0)

#     box1 = curses.newwin(20, 20, 5, 5)
#     box1.box()    

#     screen.refresh()
#     box1.refresh()

#     screen.getch()

# finally:
#     curses.endwin()

# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.keypad(1)

# win = curses.newwin(5,60,5,10)
# win.box()
# stdscr.clear()
# stdscr.refresh()

# time.sleep(1)
# pan = curses.panel.new_panel(win)
# tb = curses.textpad.Textbox(win)
# text = tb.edit()
# curses.beep()
# win.addstr(4,1,text.encode('utf-8'))

# # Setup Screen
# stdscr = curses.initscr()
# curses.savetty() #make sure we can put the screen back the way we found it
# curses.noecho() #prevent keypresses appearing on screen
# curses.cbreak() #interpret input with out return
# stdscr.keypad(1) #everyone loves the keypad
# stdscr.clearok(1) #allow the screen to be cleared
# # curses.curs_set(0) #hide the caret

# curses.start_color()

# stdscr.clear()
# stdscr.refresh()

# minX	= 0
# #how far to the right we can go.
# #Leaving room for messages.
# maxX = stdscr.getmaxyx()[1] -15

# minY	= 0
# ##how far down we can go
# #leaving room for messages
# maxY	= stdscr.getmaxyx()[0] 


# time.sleep(1)
# ##put it all back
# curses.resetty()
# curses.endwin()


# print u"\U0000270A"
# print u"\U0000270A"
# print u"\U0001F52A"
# print u"\U0001F528"
# print u"\U00002694"
# print u"\U0001F530"
# # print u"\U0001f355"

# def __det_bomb(bomb):
# 	for col in range(bomb['y']-1,bomb['y']+2):
# 		for row in range(bomb['x']-1,bomb['x']+2):
# 			print "col %d row %d BOOM\n" %(col,row)

# for b in range(4):
# 	sbomb[len(sbomb)+1] = {
# 							'counter':3
# 							,'y':random.choice(range(12))
# 							,'x':random.choice(range(12))
# 						}
# print sbomb


# while sbomb[2]['counter'] > 0:
# 	print sbomb[2]['counter']
# 	sbomb[2]['counter'] -=1

# __det_bomb(sbomb[2])

# for b in sbomb:
# 	print "sbomb[%d]['counter'] == %d " %(b,sbomb[b]['counter'])

# remB = []
# for b in sbomb:
# 	if sbomb[b]['counter'] <= 0:
# 		remB += [b]

# print "remB\n\n"		
# print remB
# print "remB\n\n"		

# for x in remB:
# 	del sbomb[x]

# print sbomb

# items= { 	'heart':{'icon':u"\U0001f493",'position':1},
# 						'money':{'icon':u"\U0001f4b0",'position':2},
# 						'food':{'icon':u"\U0001f371",'position':3},
# 						'bomb':{'icon':u"\U0001F4a3",'position':4}
# 				 	}

# for item in items:
# 	print items[item]

# ### Wall testing

# x = 20
# y = 60

# maze = {}
# uv = []

# for wy in range(y):
# 	maze[wy] = {}
# 	for wx in range(x):
# 		# print "wy = %d and wx = %d" %(wy,wx)
# 		if wy%2 or wx%2:
# 			maze[wy][wx] = '#'
# 			uv.append([wy,wx])
# 		else:
# 			maze[wy][wx] = ' '

# for yy in maze:
# 	for ww in maze[yy]:
# 		print maze[yy][ww],
# 	print '\n'


# print len(uv)

# rc = random.choice(range(len(uv)))

# print rc
# print uv[rc]
# print uv.pop(rc)



# print 
# foo = {'a':23,'b':23}

# log =  open("test.log",'a')

# foo = "what now smart guy?\n"

# log.write("cake %d\n" %(21))

# log.write("cake %d\n" %(42))

# log.write("cake %d\n" %(84))

# log.write(foo)




# try:
# 	foo['c']
# except KeyError as e:
# 	report = strftime("[%d.%b.%Y %H:%M:%S] ",localtime())
# 	report += 'KeyError: ['
# 	report += str(e)
# 	report += ']\n'
# 	log.write(report)

# json.dump(foo,log)

# log.close

# def room(x):
# 	if x < 3 : x = 3
# 	l = []
# 	for y in range(1,random.choice(range(2,x))):
# 		l += [y]
# 		print y
# 	return l

# lol = [room(5) for x in range(10)]

# print lol

# # for y in range(1,random.choice(range(2,x))):
# # 		l += [y]roomSize = random.choice([r for r in range(self.maxRoomSize)])


# x = {1:'hat',2:'cat'}

# for y in x:
# 	print y

# z = {}

# for a in z:
# 	print 'a to follow'
# 	print a
# y = 7
# x = 12
# neighbors = {}
# neighbors['N'] = {'y':y-2,'x':x}
# neighbors['E'] = {'y':y,'x':x+2}
# neighbors['W'] = {'y':y,'x':x-2}
# neighbors['S'] = {'y':y+2,'x':x}

# print type(neighbors)

# for rooms in neighbors:
# 	print neighbors[rooms]

# from inspect import currentframe, getframeinfo

# # frameinfo = getframeinfo(currentframe())

# # print frameinfo.filename, frameinfo.lineno

# print getframeinfo(currentframe()).lineno