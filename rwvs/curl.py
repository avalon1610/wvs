#!/usr/bin/envpython
#-*-coding:utf-8-*-

import threading
import pycurl
import StringIO

def curl(url):
	c = pycurl.Curl()
	if url.find('-d') != -1:
		post_data = url.split(' ')[1]
		url = url.split(' ')[2]
		c.setopt(c.POSTFIELDS,post_data)
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


class UrlOpen(threading.Thread):
	def __init__(self):
		super(UrlOpen,self).__init__()
		self.opener = pycurl.CurlMulti()
		self.handle_list = []

	def add(self,url,recall,writer=StringIO.StringIO()):
		c = pycurl.Curl()
		c.url = url
		c.content = writer
		c.recall = recall
		c.setopt(c.URL,url)
		c.setopt(c.WRITEFUNCTION,c.content.write)

		self.handle_list.append(c)
		self.opener.add_handle(c)

	def _remove(self,c):
		c.close()
		self.opener.remove_handle(c)
		self.handle_list.remove(c)

	def run(self):
		num_handle = len(self.handle_list)
		while num_handle:
			ret = self.opener.select(5.0)
			if ret == -1:
				continue
			while 1:
				num_handle_pre = num_handle
				ret,num_handle = self.opener.perform()
				if num_handle != num_handle_pre:
					result = self.opener.info_read()
					for i in result[1]:
						i.http_code = i.getinfo(i.HTTP_CODE)
						i.recall(i)
						self._remove(i)
					for i in result[2]:
						# fail
						print i
						self._remove(i)

				if ret != pycurl.E_CALL_MULTI_PERFORM:
					break

_opener = None

def curlm(urllist,callback):
	global _opener
	_opener = UrlOpen()
	for url in urllist:
		_opener.add(url,callback)
	_opener.start()
	_opener.join()

if __name__=='__main__':
	print curl('http://xiaonei.com/')