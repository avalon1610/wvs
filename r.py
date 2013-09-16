#!/usr/bin/env python
#-*-coding:utf-8-*-

from Tkinter import *
from ttk import *
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log,signals
from rwvs.spiders.dmoz_spider import DmozSpider
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import tksupport
from rwvs.session import Session
import os,sys

def log():
	pass

class App(Frame):
	plugins = {}
	def __init__(self,master=None):
		Frame.__init__(self,master)
		self._url = StringVar()
		self.pack()
		self.doPaint()

	def Launch(self):
		url = self._url.get()
		
		for mod,var in self.plugins.iteritems():
			if var.get() == 1:
				ss = Session(mod)
				cmd = [sys.executable,'.\\rwvs\\plugins\\%s.py' % mod,url]
				reactor.spawnProcess(ss,cmd[0],cmd)

		# spider = DmozSpider(url=url)
		# crawler = Crawler(Settings())
		# crawler.configure()
		# crawler.crawl(spider)
		# crawler.start()

	def doPaint(self):
		style = Style()
		style.map('x.TButton', foreground=[('pressed','red'),('active','blue')],
					background=[('pressed','!disabled','black'),('active','white')])

		topframe = Frame()
		Label(topframe,text='URL:',width=4).pack(side='left')
		Entry(topframe,textvariable=self._url).pack(side='left',expand=1,fill='x') 
		go = Button(topframe,text="GO",width=10,style='x.TButton')
		go.pack(side='right')
		go['command'] = self.Launch
		topframe.pack(side='top',fill='x')

		nb = Notebook()
		logframe = Frame(nb)
		resultframe = Frame(nb)
		pluginframe = Frame(nb)
		
		Text(logframe).pack(expand=1,fill='both')
		Text(resultframe).pack(expand=1,fill='both')
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
	a.master.title('Raz WVS')
	a.bind('<Destroy>', close)
	tksupport.install(a)
	reactor.run()
