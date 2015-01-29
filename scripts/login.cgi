#!/usr/bin/python
 
import cgi, cgitb
import cPickle as pickle
import os,sys
import hashlib

#error redirect

sys.stderr = sys.stdout 


#change directory to script directory
os.chdir(os.path.dirname(sys.argv[0]))


form = cgi.FieldStorage()

nick = form.getvalue('username').strip()
passw = form.getvalue('password')

try:
	database = pickle.load(open("../database.dat",'r'))
except IOError:
	database = {}

#encrypting password
if passw != None:
	m = hashlib.md5()
	m.update(passw)
	epassw = m.hexdigest()


if (nick == None):
	OUT = 0
elif (not (nick.isalnum())):
	OUT = 1
elif (not (nick in database)):
	OUT = 2
else:
	if (database[nick]["hpass"] == epassw):
		#set cookie
		import Cookie
		c = Cookie.SimpleCookie()
		c['uname'] = nick
		c['hash'] = epassw
		print c

		OUT=3
	else:
		OUT=4


print "Content-type:text/html\r\n\r\n"

print '''<!DOCTYPE html>
<html lang="en">


<head>
	<meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    '''
    
if (OUT == 3):
	print '''
	<meta http-equiv="refresh" content="1;url=main.cgi" />
	'''
    
    
print '''
    <title>openOnlineRisk - Login</title>

	<link href="/css/bootstrap.min.css" rel="stylesheet">
	
	<style>
		.spacer {
			margin-top: 10px; /* define margin as you see fit */
			margin-bottom: 10px;
			}
	</style>

</head>



<body>

<div class="container">
'''



if (OUT==0):
	print '''
			<div class="alert alert-danger" role="alert">Error: you didn't input any username.
			<a href="javascript:history.back()" class="alert-link">Go back</a> and fix it.
			</div>
			
			'''
elif (OUT==1):
	print '''
			<div class="alert alert-danger" role="alert">Error: username must be purely alphanumeric.
			<a href="javascript:history.back()" class="alert-link">Go back</a> and fix it.
			</div>
			
			'''
	
elif (OUT==2):
	print '''
			<div class="alert alert-danger" role="alert">Error: account %s does not exist.
			<a href="javascript:history.back()" class="alert-link">Go back</a> and fix it.
			</div>
			
			'''% nick
			
elif (OUT==3):
		
		
		print '''
			<div class="alert alert-success" role="alert">Welcome back, %s!
			</div>
			<p>We'll redirect you in a few seconds...</p>
			
			'''% nick
		
elif (OUT==4):
		print '''
			<div class="alert alert-danger" role="alert">Error: password incorrect for username %s
			<a href="javascript:history.back()" class="alert-link">Go back</a> and fix it.
			</div>
			
			'''% nick
		
else:
		print "<p>This is embarrassing...</a>"


print '''</div>


</body>
</html>'''
