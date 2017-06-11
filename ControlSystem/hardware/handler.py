import visa
import logging
import time

class VISAHandler:
	"""
		VISAHandler(address,RS485_enabled=False)
		Attributes:
			- rm = resource manager object
			- inst = visa instrument object
			- current_RS485_address = current RS485 address if RS485_enabled = True
		
		Methods:
			connect() - attempt to connect to device, if it fails it returns False
			list_resources() - utility function showing avalible resources
			write(cmd) - write cmd to device and return True if it succeeds, False if it does not
			query(cmd) - write cmd to device and read afterwards return read if it succeeds, False if it does not
			select_RS485_device(RS485_address) - change to device with RS485_address as the address
			close() - close resource
	"""
	
	def __init__(self,address='',RS485_enabled=False):
		self.rm = visa.ResourceManager()
		self.address = address
		self.connection_status = False
		
		if RS485_enabled:
			self.RS485_enabled = True
			self.current_RS485_address = ''
		
		self.connection_status = self.connect()
		
	def connect(self):
		if not self.address == '':
			try:
				self.inst = self.rm.open_resource(self.address)
				return True
			except visa.VisaIOError as e:
				logging.error(e.args[0])
				return False
		else:
			logging.error('No address specified')
			return False
	
	def list_resources(self):
		logging.info(self.rm.list_resources())
		
	def write(self,cmd):
		try:
			self.inst.write(cmd)
			return True
		except AttributeError:
			logging.error('Resource was not connected')
			return False
		except visa.VisaIOError as e:
			logging.error(e.args[0])
			return False	
	
	def query(self,cmd):
		try:
			return self.inst.query(cmd)
		except AttributeError:
			logging.error('Resource was not connected')
			return False
		except visa.VisaIOError as e:
			logging.error(e.args[0])
			return False
	
	def select_RS485_device(self,RS485_address):			
		if self.RS485_enabled:
			if not RS485_address == self.current_RS485_address:
				try:
					self.write('INST:SEL {}'.format(RS485_address))
					self.current_RS485_address = RS485_address
					return True
				except visa.VisaIOError as e:
					logging.error(e.args[0])
					return False
			else:
				True
		else:
			logging.warning('RS485 not enabled')
			False
	def close(self):
		try:
			self.instrument.close()
			return True
		except AttributeError:
			logging.error('Resource was not connected')
			return False
		except visa.VisaIOError as e:
			logging.error(e.args[0])
			return False
