###
# Drew A. Clinkenbeard
# Error Reporter and Logger
# 29 - April - 2014
# Since I broke this apart into multiple classes
# I needed a more flexible logging system.
###

from time import localtime, strftime

class Logger():

	def __init__(self, fileName="admm.log"):
		"""
			I like using tail -F to have a running log of errors and such.
			rather than just printing to a file and checking it I thought I would create 
			a system to make that possible

			Inputs:	str fileName the name of the file being written

			Output: creates a file named fileName
		"""
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
		"""
			Used to write errors. Errors and logs have a different look than logs
			
			inputs:	Exception e an exception. Only prints if it is present. 
					Default: False

					str msg: The message to print. Won't print if not present
					Default: False

					int line: the line on which the error occurred. Works 
							 well with getframeinfo(currentframe()).lineno
							 Default False

					str fileName: the name of the file where the error occured
							Default False

			output: Writes to the specified log file.


			Example Error Message:

			[*** Error ***]
			[30.Apr.2015 16:59:26] [Line : 212]
			[Message: inventory is exit ]
			[Error Supplied: string indices must be integers, not str]n
			*********************************
		"""
		
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
		

	def _log(self,msg,line=False,level="Low",fileName=False):

		"""
			Used to log actions.

			inputs: str msg: the message to be logged. 
					int line: the line where the log originated works 
							well with getframeinfo(currentframe()).lineno
							Default : False

							str level: the log level. This could be used to determine
									 which log statements are written. Not really
									 implemented here.
									 Default: 'low'

							str fileName: the file where the log statement originated
									Default: False

			output: Writes to the specified log 


			Example Log entry:

			=-=-= Log Level: Low  =-=-=-=
			[25.Apr.2015 15:32:51] 
			 line : 	 355 
			message: 	length of roomY 26, length of roomX 26)
			=-=-=-=-=-=-=-=-=-=-=-=

		"""

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
		"""
			Used to close the log file if necessary. Shouldn't be needed...
		"""
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
