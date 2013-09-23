#!/usr/bin/env python
#-*-coding:utf-8-*-
from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render
import datetime

def current_datetime(request):
	now = datetime.datetime.now()
	return render(request,'current_datetime.html',{'current_date':now})

def main(request):
	l = '离离原上草 一岁一枯荣 野火烧不尽 春风吹又生'
	return render(request,'header.html',{'list':l})

