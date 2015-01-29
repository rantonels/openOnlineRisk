#!/usr/bin/python

import chat
import os,sys
import hashlib
import cgi, cgitb

#print "Content-type:text/html\r\n\r\n"




#change directory to script directory
os.chdir(os.path.dirname(sys.argv[0]))



#error redirect

sys.stderr = open('../error.log', 'a+')


#check login

import Cookie

if 'HTTP_COOKIE' in os.environ:
	cookie_string = os.environ.get('HTTP_COOKIE')
	c = Cookie.SimpleCookie()
	c.load(cookie_string)
	
	try:
		un = c['uname'].value
		ps = c['hash'].value
		
		import cPickle as pickle
		
		db = pickle.load(open("../database.dat",'r'))
		if un in db:
			if (db[un]["hpass"] == ps):
				logged_in = True
				identity = un
			else:
				logged_in = False
	
	except KeyError:
		logged_in = False
	
else:
	logged_in = False
	
	

#CHAT
cht = chat.Chat("../mainchat.dat")

#post message
form = cgi.FieldStorage()
mess = form.getvalue('chat-message')
if mess != None:
	mess=mess.strip()

if ((mess!="") and (mess!=None)):
	if logged_in:
		nmnm = identity
		col = chat.hash2col(ps)
	else:
		nmnm = "Guest"
		col = ""
	cht.pushm(nmnm,col,mess,"")

	#generate chat
	f = open('../mainchatinclude.html','w') 
	f.write(cht.getFormat())
	f.close()

chatcode = '''

<div id="chatinc" style="padding: 30px">Loading chat...</div>
'''


#LOBBY
	
#generate lobby
lobbycode = ""
#if mess != None:
	#lobbycode = "there was a message."
#else:
	#lobbycode = "there was no message."
	
#lobbycode += "<br>"
#for it in form.list:
	#lobbycode += it.name
	


#USERBAR

#generate userbar
if logged_in:
	color = chat.hash2col(ps)
	userbar = '''<h1 style="color:%s">%s</h1>
		<p>You are logged in as %s. <a href="logout.cgi">Log out</a>.</p>
	
	'''%(color,identity,identity)
else:
	userbar = '''<h1>Guest</h1>
		<p>You are not logged in. <a href="../login.html">Log in</a>.</p>
	'''

	
print "Content-type:text/html\r\n\r\n"
print '''
	<!DOCTYPE html>
	<html lang="en">
	<head>
	<meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

	<script>
		function autoScrollDown() {
				var scrollDiv = $('#chatmain');
				scrollDiv.scrollTop(scrollDiv[0].scrollHeight);
		};

		function reLoad() {
				$("#chatinc").load("getchatinclude.cgi");
				};




	    $(document).ready(
	            function() {
			reLoad();
			autoScrollDown();
       	         	setInterval(reLoad, 3000);
			setTimeout(autoScrollDown,50);
	            });
	</script>


	<title>openOnlineRisk - Lobby</title>
	
	<link href="/css/bootstrap.min.css" rel="stylesheet">
	
	</head>
	<body> 
	
	<div class="container fill-height" style="min-height:100%%; height:100%%; overflow-y:hidden">
	
		<div class="row">
		
			<div class="col-md-4">
		
				%s		

			</div>
			<div class="col-md-8"></div>
		</div>

		<div class="col-md-6">
			%s
		</div>

		<div class="col-md-6">
			<div class="row" id="chatmain" style="outline: 1px solid; height: 500px; padding:10px; overflow-y: scroll">
				%s
				<div id="bottomscroll"></div>
			</div>
			
			<div class="row" style="margin:10px"><div class="col-md-12">
				<form role="form" action="main.cgi" method="POST">
					<div class="form-group">
					<div class="input-group">
						<input name="chat-message" type="text" class="form-control" placeholder="Write a message..." autofocus>
						<span class="input-group-btn " id="send-addon">
							<button class="btn btn-default glyphicon glyphicon-send" type="submit" value="Submit"></button>
						</span>
					</div>
					</div>
				</form>
			</div></div>
			
		</div>
		



	</div> 
	</body> 
	</html> '''%(userbar,lobbycode,chatcode)
