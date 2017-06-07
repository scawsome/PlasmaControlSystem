
import numpy as np
import logging

from ..hardware import device

class PlasmaHandler:

	"""PlasmaHandler class
		- Stores plasma state variables
		- Receives calls from the GUI for data and plasma state as well as commands for control
		- Sends commands to hardware controlling software and querys hardware control software 
		
		Attributes:
			heater_current,heater_voltage etc. = float vars storing most recent data from measurements
			interlock_water,interlock_vacuum, etc. = boolians for storing interlock state variables
			devices = dictionary of hardware objects for interfacing with
			state = dictonary of state reporting from devices
	
	"""
	
	def __init__(self):
		"""Initialization:
			create hardware objects
			create self storage for attributes
			send initialization data to GUI
			
		"""
		tdk = device.TDKPowerSupply('discharge_pwr','TCPIP0::169.254.223.84::inst0::INSTR') 
		tdk.unlock()
		self.power_supplies = {'discharge':tdk}
		#self.power_supplies = {'heater':None,'discharge':tdk,
		#	'solenoid':None,'vacuum':None}
		#self.interlock_devices = {'water':None}
	
	
	def update_monitor_panel(self,monitor_panel_object):
		"""Handle updating the monitor panel values for display
			send the panel a dict with the same shape but replace the var name with dict {var_name:value}	
		"""
		self.monitor_panel_data = {}
		for device_ID,device_obj in self.power_supplies.items():
			if device_obj.status == device.ACTIVE:
				device_obj.focus()
				self.monitor_panel_data[device_ID] = {}
				self.monitor_panel_data[device_ID]['current'] = device_obj.get('current')
				self.monitor_panel_data[device_ID]['voltage'] = device_obj.get('voltage')
			
		monitor_panel_object.update(self.monitor_panel_data)
	
	
	def update_diagram_panel(self,diagram_panel_object):
		self.diagram_panel_data = {}
		for device_ID,device in self.power_supplies.items():
			self.diagram_panel_data[device_ID] = {}
			self.diagram_panel_data[device_ID]['current'] = device.get('current')
			self.diagram_panel_data[device_ID]['voltage'] = device.get('voltage')
			self.diagram_panel_data[device_ID]['pressure'] = device.get('pressure')
		diagram_panel_object.update(self.diagram_panel_data)
	
	
	def update_interlock_panel(self,interlock_panel_object):
		self.interlock_panel_data = {}
		for device_ID,device in self.interlock_devices.items():
			self.interlock_panel_data[device_ID]['status'] = device.query('STATUS')
			
	
	def get_interlock_status(self):
		"""check if the plasma source is interlocked"""
		no_comm_devices = []
		locked_devices = []
		for name,device in self.interlock_devices.items():
			if device.device_status == device.NO_COMM:
				no_comm_devices.append(name)
			elif device.device_status == device.LOCKED:
				locked_devices.append(name)
			else:
				pass
		return {'locked':locked_devices,'no_comm':no_comm_devices}
	
	
	def close(self):
		for name,item in self.power_supplies.items():
			item.clean()
