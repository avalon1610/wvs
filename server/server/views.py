#!/usr/bin/env python
#-*-coding:utf-8-*-
from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render
import datetime


def current_datetime(request):
	now = datetime.datetime.now()
	return render(request,'current_datetime.html',{'current_date':now})

def LoadPlugins():
	import os
	rootDir = '..\\rwvs\\plugins'
	result_list = {}

	for root,dirs,files in os.walk(rootDir):
		number = 0
		py_row = 0
		catalog_number = ''
		catalog_name = ''

		for f in files:
			if f.find('.py') == -1:
				continue
			if f.find('.pyc') != -1:
				continue
			if f.find('__init__') != -1:
				continue

			p_list = []
			for line in open(os.path.join(root,f)):
				if line.split('-')[0].find('catalog') != -1:
					# catalog_number = line.split('-')[1]
					catalog_name = line.split('-')[2]
					result_list[catalog_name] = p_list

				if line.split('-')[0].find('name') != -1:
					mod = f.split('.')[0]
					mod_name = line.split('-')[1]
					p_list.append([mod,mod_name])
					break

	result_list['test'] = [['asdf','aaaaaaaaaaaaaaaaaaa'],['adffff','cccccc']]
	result_list['test1'] = [['asdf','aaaaaaaaaaaaaaaaaaa'],['adffff','cccccc']]
	result_list['test2'] = [['asdf','aaaaaaaaaaaaaaaaaaa'],['adffff','cccccc']]
	result_list['test3'] = [['asdf','aaaaaaaaaaaaaaaaaaa'],['adffff','cccccc']]
	result_list['test4'] = [['asdf','aaaaaaaaaaaaaaaaaaa'],['adffff','cccccc']]
	result_list['test5'] = [['asdf','aaaaaaaaaaaaaaaaaaa'],['adffff','cccccc']]
	result_list['test6'] = [['asdf','aaaaaaaaaaaaaaaaaaa'],['adffff','cccccc']]
	return result_list

def main(request):
	plugins_list = LoadPlugins()
	return render(request,'toolbar.html',{'list':plugins_list})

