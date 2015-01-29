#!/usr/bin/python

PRIVATE_NAMES = ["Guest"]
 
import cgi, cgitb
import cPickle as pickle
import os,sys
import hashlib

#error redirect

sys.stderr = sys.stdout 


#change directory to script directory
os.chdir(os.path.dirname(sys.argv[0]))


form = cgi.FieldStorage()

nick = form.getvalue('username')
passw = form.getvalue('password')
cpassw = form.getvalue('confirm_password')

try:
	database = pickle.load(open("../database.dat",'r'))
except IOError:
	database = {}

#encrypting password
if passw != None:
	m = hashlib.md5()
	m.update(passw)
	epassw = m.hexdigest()

print "Content-type:text/html\r\n\r\n"

print '''<!DOCTYPE html>
<html lang="en">


<head>
	<meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
 
 
	<title>openOnlineRisk - Register account</title>
	</head>
	<body>

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

if (nick == None):
	print '''<div class="alert alert-danger" role="alert">Error: you did not enter any username, <b>or</b> you reached this page by non-conventional means. Either way, <a href="javascript:history.back()" class="alert-link">go back</a> and enter one.</div>'''
elif (nick in PRIVATE_NAMES):
	print '''<div class="alert alert-danger" role="alert">Error: the username you entered (%s) is a reserved word. <a href="javascript:history.back()" class="alert-link">Go back</a> and choose another one.</div>'''%nick
elif (not (nick.isalnum())):
	print '''<div class="alert alert-danger" role="alert">Error: username must be purely alphanumeric. <a href="javascript:history.back()" class="alert-link">Go back</a> and choose another one.</div>'''
elif ( nick in database):
	print '''<div class="alert alert-danger" role="alert">Error: username already exists! If you forgot your password, you're pretty much f***ed. <a href="javascript:history.back()" class="alert-link">Go back</a><div>'''
elif (passw != cpassw):
	print '''<div class="alert alert-danger" role="alert">Error: passwords don't match! <a href="javascript:history.back()" class="alert-link">Go back</a> and retype them carefully.</div>'''
elif (passw == None):
	print '''<div class="alert alert-danger" role="alert">Error: you did not enter any password. <a href="javascript:history.back()" class="alert-link">Go back</a> and enter one.</div>'''
else:
	account = {"hpass":epassw}
	database[nick] = account
	pickle.dump(database,open("../database.dat",'w'))

	print '''<div class="alert alert-success" role="alert">New account created! <a href="javascript:history.back()" class="alert-link">Go back</a> and log in.</div>'''

print '''
</div>
</body>



</html>'''
