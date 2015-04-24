#e.py
# from __future__ import print_function
# from time import localtime, strftime
import json
import random

items= { 	'heart':{'icon':u"\U0001f493",'position':1},
						'money':{'icon':u"\U0001f4b0",'position':2},
						'food':{'icon':u"\U0001f371",'position':3},
						'bomb':{'icon':u"\U0001F4a3",'position':4}
				 	}

for item in items:
	print items[item]

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