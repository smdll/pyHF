#coding=utf-8
from ad983x import *
from socket import *
from time import sleep
import ConfigParser

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("127.0.0.1", 4321))
ad9983x = AD983X(0) # SPI bus 0(/dev/spidev0.0)
ad983x.setOutputMode(OUTPUT_MODE_SINE) # Output sine wave
ad983x.setSignOutput(SIGN_OUTPUT_NONE) # Channel 0
wpm = 15
dit_time = wpm * 5 / 6 / 1000#######
dah_time = dit_time * 3#######

def sendCW(data):
	for word in data:
		if word == '.':
			setSignOutput(SIGN_OUTPUT_MSB)
			time.sleep(dit_time)
			
		elif word == '-':
			pass
		elif word == ' ':
			pass
		else:
			raise Exception("Character Error")

'''
Data format:
	1. Set frequency: !{Frequency(MHz)}&
	2. Set words per minute(WPM): @{WPM}&
	3. Send preset cw: #{.|-| }&
'''
while True:
	data, addr = sock.recvfrom(256)
	if data[0] == '!':
		ad983x.setFrequency(int(data[1:data.find('&')]))
	elif data[0] == '@':
		
	elif data[0] == '#':
		sendCW(data[1:data.find('&')])