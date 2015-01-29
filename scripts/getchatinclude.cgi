#!/usr/bin/python

import os, sys

os.chdir(os.path.dirname(sys.argv[0]))

print "Content-type:text/html\r\n\r\n"

f = open('../mainchatinclude.html','r')
s = f.read()
f.close()

print s
