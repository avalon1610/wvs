#!/usr/bin/env python
#-*-coding:utf-8-*-

from Tkinter import *
from ttk import *
import tkMessageBox
from twisted.internet import reactor
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import tksupport
from rwvs.session import Session,checkrunning
import os,sys
from urlparse import urlparse

class App(Frame):
	plugins = {}
	sessionlist = []
	def __init__(self,master=None):
		self.root = Tk()
		# 几号写轮眼，随你喜欢
		self.root.wm_iconbitmap('.\\rwvs\\resource\\sharieye_04.ico')
		Frame.__init__(self,master)
		self._url = StringVar()
		self.pack()
		self.doPaint()

	def Launch(self):
		if checkrunning(0) > 0 and len(self.sessionlist) > 0:
			# stop it 
			for ss in self.sessionlist:
				if not ss.ss_done:
					ss.send('Abort')
			return

		url = self._url.get()
		if not url:
			return
		
		del self.sessionlist[:]
		scheme,netloc,path,params,query,fragment = urlparse(url)
		if len(scheme) == 0 and len(netloc) == 0:
			url = 'http://' + url
			scheme,netloc,path,params,query,fragment = urlparse(url)
		if len(scheme) == 0:
			scheme = 'http'
		url = scheme + '://' + netloc + '/'

		self.log.delete(1.0,END)
		self.result.delete(1.0,END)
		for mod,var in self.plugins.iteritems():
			if var.get() == 1:
				ss = Session(mod,self)
				self.sessionlist.append(ss)
				cmd = [sys.executable,'.\\rwvs\\pluginsmanager.py',mod,url]
				reactor.spawnProcess(ss,cmd[0],cmd)
				checkrunning(1)

		self.root.title('RazWVS - Running...')
		self.go['text'] = 'STOP'

	def doPaint(self):
		style = Style()
		style.map('x.TButton', foreground=[('pressed','red'),('active','blue')],
					background=[('pressed','!disabled','black'),('active','white')])

		topframe = Frame()
		Label(topframe,text='URL:',width=4).pack(side='left')
		Entry(topframe,textvariable=self._url).pack(side='left',expand=1,fill='x') 
		self.go = Button(topframe,text="GO",width=10,style='x.TButton')
		self.go.pack(side='right')
		self.go['command'] = self.Launch
		self.root.bind('<Return>',lambda e:self.go.invoke())
		topframe.pack(side='top',fill='x')

		nb = Notebook()
		logframe = Frame(nb)
		resultframe = Frame(nb)
		pluginframe = Frame(nb)
		
		self.log = Text(logframe)
		self.log.pack(expand=1,fill='both')
		self.result = Text(resultframe)
		self.result.pack(expand=1,fill='both')
		nb.add(pluginframe,text='PLUGIN')
		nb.add(logframe,text='LOG')
		nb.add(resultframe,text='RESULT')
		nb.pack(expand=1,fill='both')
		nb.enable_traversal()

		self.LoadPlugins(pluginframe)

	def LoadPlugins(self,pluginframe):
		rootDir = '.\\rwvs\\plugins'
		var = locals()
		plugins_nb = Notebook(pluginframe)
		style = Style()
		style.configure('disable.TCheckbutton',foreground='red')
		for root,dirs,files in os.walk(rootDir):
			number = 0
			py_row = 0
			for f in files:
				if f.find('.py') == -1:
					continue
				if f.find('.pyc') != -1:
					continue
				if f.find('__init__') != -1:
					continue
				mod_name = ''
				mod_description = ''
				check_var = IntVar()
				for line in open(os.path.join(root,f)):
					if line.split('-')[0].find('catalog') != -1:
						number = line.split('-')[1]
						if var.has_key(number):
							pass
						else:
							var[number] = Frame(plugins_nb)
							plugins_nb.add(var[number],text=line.split('-')[2])

					if line.split('-')[0].find('name') != -1:
						mod = f.split('.')[0]
						mod_name = line.split('-')[1]

						# find a undefined catalog plugins
						if number == 0 and not var.has_key(number):
							var[number] = Frame(plugins_nb)
							plugins_nb.add(var[number],text='未归类')
						var[mod] = Checkbutton(var[number],text=mod_name,variable=check_var)
						var[mod].grid(row=py_row,column=0,sticky=W)
						var[mod].invoke()
						var[mod].invoke()
						self.plugins[mod] = check_var
						py_row += 1
						break

				if mod_name != '':
					continue
				if (var.has_key(number)):
					mod_name = 'load plugin failed:%s' % f
					Checkbutton(var[number],style='disable.TCheckbutton',text=mod_name).grid(row=py_row,column=0,sticky=W)
					py_row += 1

		plugins_nb.pack(expand=1,fill='both')
		plugins_nb.enable_traversal()

def close(e):
	reactor.stop()

if __name__ == "__main__":
	a = App()
	a.master.title('RazWVS')
	a.bind('<Destroy>', close)
	tksupport.install(a)
	reactor.run()
