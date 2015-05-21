#!/usr/bin/python           # This is server.py file
import socket               # Import socket module
import re
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# Create a socket object
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
#host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
user = {}
online = []
on_user = {}
off_msg = {}

user['marry'] = '123456'
user['john'] = 'qwerty'
user['jean'] = 'asdfgh'
user['jack'] = 'zxcvbn'
off_msg['marry'] = ''
off_msg['john'] = ''
off_msg['jean'] = ''
off_msg['jack'] = ''

print 'Server started!'
try:
	s.bind(('', port))
except Exception as e:
	print('port in use...')
	s.close()
	raw_input('press any key to quit...')
	sys.exit(0)

while True:
	print 'Waiting for clients...'
	msg, addr = s.recvfrom(2048)
	print msg
	if msg[0:1] == '0':
		len_ac = int(msg[2:3],10)
		ac = msg[3:(len_ac+3)]
		len_pw = len_ac + int(msg[len_ac+3:len_ac+4],10)
		pw = msg[len_ac+4:4+len_pw]
		user_port = int(msg[4+len_pw:len(msg)],10)
		print ac
		print pw
		print user_port
		if msg[1:2] == '1':
			if user[ac] == pw: 
				s.sendto('1', ('<broadcast>', user_port))
				online.append(ac)
				on_user[ac] = user_port
				if off_msg[ac] != '':
					s.sendto(off_msg[ac], ('<broadcast>', user_port))
					off_msg[ac] = ''
			else:
				s.sendto('0', ('<broadcast>', user_port))
		elif msg[1:2] == '0':
			if ac in user:
				s.sendto('0', ('<broadcast>', user_port))
			else:
				user[ac] = pw
				s.sendto('1', ('<broadcast>', user_port))
				online.append(ac)
				on_user[ac] = user_port
				off_msg[ac] = ''
	elif msg[0:1] == '1':
			print online
			user_port = int(msg[1:len(msg)])
			msg = ''
			for x in online:
				msg += x + '\n'
			s.sendto(msg, ('<broadcast>', user_port))
	elif msg[0:1] == '2':
		len_ac = int(msg[1:2],0)
		if msg[2:(len_ac+2)] in online:
			user_port = on_user[msg[2:(len_ac+2)]]
			s.sendto(msg[(len_ac+2):len(msg)], ('<broadcast>', user_port))
		else :
			off_msg[msg[2:(len_ac+2)]] +=  msg[(len_ac+2):len(msg)]
	elif msg[0:1] == '3':
		for x in online:
			user_port = on_user[x]
			s.sendto(msg[1:len(msg)], ('<broadcast>', user_port))
	elif msg[0:1] == '4':
		len_ac = int(msg[1:2],0)
		ac = msg[2:(len_ac+2)]
		online.remove(ac)
	print 'end'

c.close()                # Close the connection
