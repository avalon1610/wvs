#!/usr/bin/envpython
#-*-coding:utf-8-*-

import pycurl
import StringIO

def curl(url):
	c = pycurl.Curl()
	headerbuffer = StringIO.StringIO()
	bodybuffer = StringIO.StringIO()
	c.setopt(c.URL,url)
	c.setopt(c.HEADERFUNCTION,headerbuffer.write)
	c.setopt(c.WRITEFUNCTION,bodybuffer.write)
	code = 0
	head = ''
	body = ''
	final_url = url
	errcode = 0
	errstr = ''
	try:
		c.perform()

		head_info = headerbuffer.getvalue().split('\r\n')
		code = head_info[0].split(' ')[1]
		if code == '301' or code == '302':
			for h in head_info:
				if h.find('Location') != -1:
					final_url = h.split(' ')[1]
					break
		head = headerbuffer.getvalue()					
		body = bodybuffer.getvalue()
	except pycurl.error,error:
		errcode,errstr = error

	# code
	# head
	# body
	# final_url

	return (int(code),head,body,int(errcode),final_url,errstr)
	 #  CURLE_OK = 0 
	 #  CURLE_COULDNT_CONNECT = 1 
	 #  CURLE_OPERATION_TIMEDOUT = 2 
	 #  CURLE_RECV_ERROR = 3 
	 #  CURLE_SEND_ERROR = 4 
	 #  CURLE_FILESIZE_EXCEEDED = 5 
	 #  CURLE_COULDNT_RESOLVE_HOST = 6 
	 #  CURLE_UNSUPPORTED_PROTOCOL = 7 
	 #  # custome error 
	 #  CURLE_ARG_ERROR = 8 
	 #  CURLE_MIME_ERROR = 9 
	
if __name__=='__main__':
	print curl('http://xiaonei.com/')