#!/usr/bin/env python
from Tkinter import *
from ttk import *
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log,signals
from rwvs.spiders.dmoz_spider import DmozSpider
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import tksupport

class App(Frame):
	def __init__(self,master=None):
		Frame.__init__(self,master)
		self._url = StringVar()
		self.pack()
		self.doPaint()

	def Launch(self):
		url = self._url.get()
		
		spider = DmozSpider(url=url)
		crawler = Crawler(Settings())
		crawler.configure()
		crawler.crawl(spider)
		crawler.start()
		log.start()

	def doPaint(self):
		style = Style()
		style.map('x.TButton', foreground=[('pressed','red'),('active','blue')],
					background=[('pressed','!disabled','black'),('active','white')])

		topframe = Frame()
		Label(topframe,text='URL:',width=4).pack(side='left')
		Entry(topframe,width=80,textvariable=self._url).pack(side='left') 
		go = Button(topframe,text="GO",width=10,style='x.TButton')
		go.pack(side='left')
		go['command'] = self.Launch
		topframe.pack(side='top')

		nb = Notebook()
		logframe = Frame(nb)
		resultframe = Frame(nb)

		Text(logframe).pack(fill='both')
		Text(resultframe).pack(fill='both')
		nb.add(logframe,text='LOG')
		nb.add(resultframe,text='RESULT')
		nb.pack(fill='both')

def close(e):
	reactor.stop()

if __name__ == "__main__":
	a = App()
	a.master.title('Raz WVS')
	a.bind('<Destroy>', close)
	tksupport.install(a)
	reactor.run()
