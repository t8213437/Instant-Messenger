#!/usr/bin/python           # This is client.py file
import socket               # Import socket module
import sys
import random
import thread
import getpass

mod = 0

def Threadfun(string, sleeptime, lock):
	while(True):
		msg, addr = s.recvfrom(2048)
		print '\r' + msg,
		if mod == 1:
			print '>',


if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # Create a socket object
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #broadcast
	#host = socket.gethostname() # Get local machine name
	port = random.randint(0,99999)               # Reserve a port for your service.

	print ('Connecting to server')
	try:
		s.bind(('', port))    #we want to send from port 68
	except Exception as e:
		print('port in use...')
		s.close()
		raw_input('press any key to quit...')
		sys.exit(0)

	while mod != 1:
		status = raw_input("Are you a registered user?(y/n)")
		if status == 'y':
			ac = raw_input('account: ')
			pw = getpass.getpass(prompt='password: ')
			msg = '01' + str(len(ac)) + ac + str(len(pw)) + pw + str(port)
			s.sendto(msg, ('<broadcast>', 12345))
			#s.settimeout(5)
			msg, addr = s.recvfrom(2048)
			if msg == '1' :
				mod = 1
			elif msg == '0':
				print 'Account number or password is incorrect!!'
		elif status == 'n':
			ac = raw_input('create account: ')
			pw = getpass.getpass(prompt='create password: ')
			msg = '00' + str(len(ac)) + ac + str(len(pw)) + pw + str(port)
			s.sendto(msg, ('<broadcast>', 12345))
			#s.settimeout(5)
			msg, addr = s.recvfrom(2048)
			if msg == '1' :
				print 'User created!'
				mod = 1
			elif msg == '0':
				print 'Login name already exist!'

	thread.start_new_thread(Threadfun,("Thread-1", 1, 2))
	while (mod == 1):
		op = raw_input('>')
		if op == 'listuser':
			msg = '1' + str(port)
			s.sendto(msg, ('<broadcast>', 12345))
			#msg, addr = s.recvfrom(2048)
			#print (msg)
		elif op.startswith('send'):
			len_ac = len(op)-5
			msg = '2' + str(len_ac) + op[5:len(op)] + 'massage from ' + ac + ': '
			talk = raw_input('')
			msg += talk + '\n'
			s.sendto(msg, ('<broadcast>', 12345))
		elif op.startswith('broadcast'):
			msg = '3' + ac + ' broadcast to everyone: ' + op[10:len(op)] + '\n'
			s.sendto(msg, ('<broadcast>', 12345))
		elif op=='logout':
			msg = '4' + str(len(ac)) + ac
			s.sendto(msg, ('<broadcast>', 12345))
			s.close                     # Close the socket when done
			sys.exit()
		elif op.startswith('talk'):
			mod = 2
			len_ac = len(op)-5
			msg = '5' + str(len_ac) + op[5:len(op)] + str(len(ac)) + ac + 'talk from ' + ac + ': '
			talk = raw_input('')
			msg += talk + '\n'
			s.sendto(msg, ('<broadcast>', 12345))
			while talk != 'end':
				talk = raw_input('')
				if talk == 'end':
					mod = 1
					break
				msg = '2' + str(len_ac) + op[5:len(op)] 
				msg += talk + '\n'
				s.sendto(msg, ('<broadcast>', 12345))
	sys.exit()
	#s.close                     # Close the socket when done
