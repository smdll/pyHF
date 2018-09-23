#coding=utf-8
from ad983x import *
from socket import *
from time import sleep
import ConfigParser

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("127.0.0.1", 4321))
ad983x = AD983X(0) # SPI bus 0(/dev/spidev0.0)
current_frequency = 7.023
dit_time = 0
dah_time = 0
CODE = {
	'A': '.-',     'B': '-...',   'C': '-.-.', 
	'D': '-..',    'E': '.',       'F': '..-.',
	'G': '--.',   'H': '....',    'I': '..',
	'J': '.---',   'K': '-.-',    'L': '.-..',
	'M': '--',    'N': '-.',     'O': '---',
	'P': '.--.',   'Q': '--.-',  'R': '.-.',
     	'S': '...',     'T': '-',      'U': '..-',
	'V': '...-',   'W': '.--',   'X': '-..-',
	'Y': '-.--',   'Z': '--..',

	'0': '-----', '1': '.----', '2': '..---',
	'3': '...--',  '4': '....-',  '5': '.....',
	'6': '-....',   '7': '--...', '8': '---..',
	'9': '----.',

	'.': '.-.-.-', '?': '..--..',  ' ': ' '
}

def sendCW(data):
	for ch in data:
		code = CODE['?']
		try:
			code = CODE[ch]
		except:
			pass
		for elem in code:
			if elem == '.':
				ad983x.setFrequency(0, current_frequency)
				time.sleep(dit_time)
				ad983x.setFrequency(0, 0)
			elif elem == '-':
				ad983x.setFrequency(0, current_frequency)
				time.sleep(dah_time)
				ad983x.setFrequency(0, 0)
			else:
				time.sleep(2 * dit_time)
			time.sleep(dit_time)

def changeWPM(wpm):
	global dit_time
	global dah_time
	dit_time = wpm * 5 / 6 / 1000
	dah_time = dit_time * 3
'''
Data format:
	1. Set frequency: !{Frequency(MHz)}&
	2. Set words per minute(WPM): @{WPM}&
	3. Send preset cw: #{.|-| }&
'''
def main():
	global current_frequency
	changeWPM(15)
	while True:
		data, addr = sock.recvfrom(256)
		if data[0] == '!':
			current_frequency = int(data[1:data.find('&')])
		elif data[0] == '@':
			changeWPM(int(data[1:data.find('&')]))
		elif data[0] == '#':
			sendCW(data[1:data.find('&')])

if __name__ == "__main__":
	main()