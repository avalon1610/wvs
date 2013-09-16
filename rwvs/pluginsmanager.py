import sys
import imp
import curl

def main():
	if len(sys.argv) < 3:
		return
	mod = sys.argv[1]
	url = sys.argv[2]

	try:
		module = __import__('plugins.%s' % mod,fromlist=['audit'])
	except ImportError:
		print 'plugin %s not found.' % mod
		return

	func = getattr(module,'audit')
	func(url)

if __name__=='__main__':
	main()
	