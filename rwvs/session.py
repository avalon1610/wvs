from twisted.internet import protocol
from Tkinter import *

DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'

CHECKANDPLUS = 1
CHECKANDMINUS = -1
ONLYCHECK = 0
running = 0
def checkrunning(active):
	global running
	if active == CHECKANDPLUS: 
		running += 1
	elif active == CHECKANDMINUS:
		running -= 1
	elif active == ONLYCHECK:
		pass

	return running

class Session(protocol.ProcessProtocol):
	def __init__(self,mod,app):
		self.mod_name = mod
		self.app = app
		self.ss_done = False

	def log(self,msg,level=INFO):
		l = '[%s][%s]%s\n' % (self.mod_name,level,msg)
		self.app.log.insert(END,l)
		if level == WARNING:
			self.app.result.insert(END,'[%s]%s' % (self.mod_name,msg))

	def connectionMade(self):
		self.log('Session Create')

	def send(self,data):
		self.transport.write(data)
		self.log('Request %s' % data)
		
	def outReceived(self,data):
		self.log('%s' % data,WARNING)

	def errReceived(self,data):
		self.log('%s' % data,ERROR)

	def processEnded(self,reason):
		self.log('Session Closed:%s' % reason.value.exitCode,INFO)
		done = checkrunning(-1)
		self.ss_done = True
		if done == 0:
			self.app.root.title('RazWVS')
			self.app.go['text'] = 'GO'