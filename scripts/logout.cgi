#!/usr/bin/python

import os,sys

import Cookie
c = Cookie.SimpleCookie()
c['uname'] = ''
c['uname']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

print c

print "Content-type: text/html\n\n"


print """
<html>
<meta http-equiv="refresh" content="0;url=main.cgi" />
<body>
<p> logging out... </p>
</body>
</html>
"""
