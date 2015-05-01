###
# Drew A. Clinkenbeard
# Error Reporter and Logger
# 30 - April - 2014
# Since I broke this appart into multiple classes
# I needed a more flexible logging system.
###
from time import localtime, strftime

class Logger():

	def __init__(self, fileName="admm.log"):
		self.fileName = fileName
		try :
			f = open(fileName,'a')
		except :
			print "Error: Couldn't Open File {0}".format(fileName)
		finally :
			f.close()

	def __repr__(self):

		return "Writing to file: {0}".format(self.fileName)


	def _err(self,e=False,msg=False,line=False,fileName=False):
		
		f = open(self.fileName,'a')
		
		report = "\n[*** Error ***]\n"
		report += strftime("[%d.%b.%Y %H:%M:%S] ",localtime())
		if fileName:
			report == "[File : {0}] \n".format(fileName)
		if line:
			report += "[Line : {0}]\n".format(line)
		if msg:
			report += "[Message: {0} ]\n".format(msg)
		if e:
			report += "[Error Supplied: {0}]n".format(e)
		report += "\n*********************************\n"
		f.write(report)
		f.close()
		

	def _log(self,msg,line="none",level="Low",fileName=False):
		f = open(self.fileName,'a')
		
		report = "\n[Log {0}]\n".format(level)
		report += strftime("[%d.%b.%Y %H:%M:%S]\n ",localtime())
		if fileName:
			report == "[File : {0}] \n".format(fileName)
		if line:
			report += "[Line : {0}]\n".format(line)
		if msg:
			report += "[Message: {0} ]\n".format(msg)
		report += "\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"
		f.write(report)

	def closeFile(self):
		try :
			self.f.close()
			return true
		except:
			print "Error Closing file {0}".format(self.fileName)
			return False

# class admm_logger(logger):

# 	def __err__(self,e=False,values=False,line=False):

# 		stats  = "minY %d maxY %d\n" %(self.minY, self.maxY)
# 		stats += "minX %d maxX %d\n" %(self.minX, self.maxX)
# 		stats += "len(self.maze) %d len(self.maze[self.minY]) %d" %(len(self.maze) , len(self.maze[self.minY]))

# 		report = strftime("[%d.%b.%Y %H:%M:%S] ",localtime())
# 		report += 'KeyError: ['
# 		report += str(e)
# 		report += ']\n'
# 		log.write(report)
# 		log.write("\n**stats**\n")
# 		log.write(stats)
# 		log.write("\n**stats**\n")
# 		log.write("\n ** report **\n")
# 		json.dump(values,log)
# 		log.write("\n ** report **\n")

# 	def __logger__(self,msg,line="none",level="Low"):
# 		log.write("=-=-= Log Level: %s  =-=-=-=\n" %(level))
# 		log.write(strftime("[%d.%b.%Y %H:%M:%S] \n ",localtime()))
# 		log.write("line : \t %s \n" %(str(line)))
# 		log.write("message: \t")
# 		log.write(msg)
# 		log.write("\n=-=-=-=-=-=-=-=-=-=-=-=\n")
