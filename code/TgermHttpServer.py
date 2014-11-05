#-*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import BaseHTTPServer
import cgi
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse, parse_qs


class HttpReqHandler(BaseHTTPRequestHandler):
	dic = {}
	def do_GET(self):
		dic = parse_qs(urlparse(self.path).query)
		print(dic)
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("HttpResponse!")
		return

	def do_POST(self):
		dic = cgi.FieldStorage()
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("HttpResponse!")
		return


HandlerClass = HttpReqHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"
Host		 = "192.80.133.221"
Port		 = 8089


server_address = (Host, Port)
 
HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)
 
sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()