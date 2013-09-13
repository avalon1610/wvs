from twisted.internet import protocol

class Session(protocol.ProcessProtocol):
	def connectionMade(self):
		print 'Session Create'

	def send(self,data):
		self.transport.write(data)
		print 'Sent:%r' % data
		
	def outReceived(self,data):
		print '[torrent]:',data

	def errReceived(self,data):
		print '[torrent error]:',data

	def processEnded(self,reason):
		print 'Process end status',reason.value.exitCode
