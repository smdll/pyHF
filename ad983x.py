import spidev

# All kinds of registers
REG_FREQ = [0x4000, 0x8000]
REG_PHASE = [0xC000, 0xE000]
REG_B28 = 0x2000
REG_HLB = 0x1000
REG_FSEL = 0x0800
REG_PSEL = 0x0400
REG_PINSW = 0x0200
REG_RESET = 0x0100
REG_SLEEP1 = 0x0080
REG_SLEEP12 = 0x0040
REG_OPBITEN = 0x0020
REG_SIGNPIB = 0x0010
REG_DIV2 = 0x0008
REG_MODE = 0x0002
SIGN_OUTPUT_MASK = (REG_OPBITEN | REG_SIGNPIB | REG_DIV2 | REG_MODE)

# Sign mode register bits
SIGN_OUTPUT = {"NONE":0x0000, "MSB":0x0028, "MSB_2":0x0020, "COMPARATOR":0x0038}

# Output mode register bits
OUTPUT_MODE = {"SINE":0x0000, "TRIANGLE":0x0002}

class AD983X:
	def __init__(self, cs_pin):
		self.spi = spidev.SpiDev()
		self.spi.open(0, cs_pin)#MSB FIRST

		self.m_reg = REG_B28

		self.spi.mode = 0b01 #MODE2
		self.writeReg(self.m_reg)

		# Initialize frequency and phase registers to 0
		self.setOutputMode("SINE") # Output sine wave
		self.setSignOutput("NONE") # Disable sign output
		self.setFrequency(0, 0)
		self.setFrequency(1, 0)
		self.setPhase(0, 0)
		self.setPhase(1, 0)

	def writeReg(self, value):
		to_send = [value >> 8, value & 0xFF]
		self.spi.xfer(to_send)

	'''
	Set the output frequency
		channel{0|1}: the output channel
		frequency(MHz): the output frequency
	'''
	def setFrequency(self, channel, frequency):
		self.writeReg(REG_FREQ[channel] | (frequency & 0x3FFF))
		self.writeReg(REG_FREQ[channel] | ((frequency >> 14) & 0x3FFF))

	'''
	Set the output phase
		channel{0|1}: the output channel
		phase: the output phase, 12bit
	'''
	def setPhase(self, channel, phase):
		self.writeReg(REG_PHASE[channel] | (phase & 0x0FFF))

	'''
	Set the mode of sign output
		out{"NONE"|"MSB"|"MSB_2"|"COMPARATOR"}: register bits from above
	'''
	def setSignOutput(self, out):
		self.m_reg = (self.m_reg & ~SIGN_OUTPUT_MASK) | SIGN_OUTPUT[out]
		self.writeReg(self.m_reg)

	'''
	Set the output mode
		out{"SINE"|"TRIANGLE"}: register bits from above
	'''
	def setOutputMode(self, out):
		self.m_reg &= ~REG_MODE
		self.m_reg = (self.m_reg & ~SIGN_OUTPUT_MASK) | OUTPUT_MODE[out]
		self.writeReg(self.m_reg)
