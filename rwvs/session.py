from twisted.internet import protocol

DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'

def log(msg,level=INFO,mod=None):
	print '[%s][%s]%s' % (mod,level,msg)

class Session(protocol.ProcessProtocol):
	def __init__(self,mod):
		self.mod_name = mod
		
	def log(self,msg,level=INFO):
		log(msg,level,self.mod_name)

	def connectionMade(self):
		self.log('Session Create')

	def send(self,data):
		self.transport.write(data)
		self.log('%s' % data)
		
	def outReceived(self,data):
		self.log('%s' % data)

	def errReceived(self,data):
		self.log('%s' % data,ERROR)

	def processEnded(self,reason):
		self.log('Process END:%s' % reason.value.exitCode,ERROR)