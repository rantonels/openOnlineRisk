#!/usr/bin/python

import chat
import random



print "Content-type:text/html\r\n\r\n"

print "<head></head><body>"

for i in range(1000):
	c = chat.hash2col(str(random.randint(0,0xffffff)))
	print '''<div style="color:%s">Color number %d</div>'''%(c,i)

print "</body>"

