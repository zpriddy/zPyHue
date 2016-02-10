#! /usr/bin/python
#TODO - Make a list off UUIDS lights to light ID - This si for future plans

import argparse
import json
import logging
import requests
from time import sleep


class HueButtonNotPressed(Exception):
	pass

###############################################################################
##												START LIGHT SECTION 															 ##
###############################################################################

class LightObject(object):
	'''
	Hue Light Object

	This is the object that stores all the data of the lights.
	This object should not be used directly becuase it is
	deleted and recreated with each hue update. You should use
	the Light object for any referenced object.
	'''

	def __init__(self, raw_data, bridge, light_id):
		self._light_id = int(light_id)
		self._name = raw_data['name']
		self._uniqueid = raw_data['uniqueid']
		self._manufacturername = raw_data['manufacturername']
		self._swversion = raw_data['swversion']
		self._modelid = raw_data['modelid']
		self._reachable = raw_data['state']['reachable']
		self._on = raw_data['state']['on']
		self._hue = raw_data['state']['hue']
		self._sat = raw_data['state']['sat']
		self._effect = raw_data['state']['effect']
		self._xy = raw_data['state']['xy']
		self._colormode = raw_data['state']['colormode']
		self._alert = raw_data['state']['alert']
		self._bri = raw_data['state']['bri']
		self._reachable = raw_data['state']['reachable']
		self._type = raw_data['type']

		self._bridge = bridge

	def __del__(self):
		pass

	def __repr__(self):
		return '<{0}.{1} Object "{2}" at ID {3}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self._name,
            hex(int(self._light_id)))

	def __str__(self):
		return 'Light ' + self._name + " ID: " + str(self._light_id) +  ' ' + self.str_state()

	def str_state(self):
		return '{on : ' + str(self.on) + ', bri : ' + str(self.bri) + '}'

	@property
	def light_id(self):
		return self._light_id

	@property
	def name(self):
		return self._name

	@property
	def hue(self):
		return self._hue

	@property
	def sat(self):
		return self._sat

	@property
	def bri(self):
		return self._bri

	@property
	def xy(self):
		return self._xy

	@property
	def on(self):
		return self._on

	@on.setter
	def on(self, value):
		self.set_light({'on':value})


	def ON(self):
		self.on = True

	def OFF(self):
		self.on = False

	def set_light(self, value):
		light_id = self._light_id

		logging.info('Setting Light: ' + str(light_id))

		self._bridge.send_request('lights/' + str(light_id) + '/state', data=value, method='PUT')


class Light(object):
	def __init__(self, light):
		self._bridge = light._bridge
		self._light_id = light.light_id

	def __repr__(self):
		return repr(self._bridge.get_light(self._light_id))

	def __str__(self):
		return str(self._bridge.get_light(self._light_id))

	@property
	def on(self):
		light = self._bridge.get_light(self._light_id)
		return light.on

	@on.setter
	def on(self, value):
		light = self._bridge.get_light(self._light_id)
		if value:
			light.ON()
		else:
			light.OFF()

	def update(self):
		self._bridge.update()

	def ON(self):
		light = self._bridge.get_light(self._light_id)
		light.ON()

	def OFF(self):
		light = self._bridge.get_light(self._light_id)
		light.OFF()

###############################################################################
##													END LIGHT SECTION 															 ##
###############################################################################


###############################################################################
##												START GROUP SECTION 															 ##
###############################################################################

class GroupObject(object):
	'''
	Hue Group Object

	This is the object that stores all the data of the lights.
	This object should not be used directly becuase it is
	deleted and recreated with each hue update. You should use
	the Light object for any referenced object.
	'''

	def __init__(self, raw_data, bridge, group_id):
		self._group_id = int(group_id)
		self._name = raw_data['name']
		self._lights = raw_data['lights']
		self._on = raw_data['action']['on']
		self._hue = raw_data['action']['hue']
		self._sat = raw_data['action']['sat']
		self._effect = raw_data['action']['effect']
		self._xy = raw_data['action']['xy']
		self._colormode = raw_data['action']['colormode']
		self._alert = raw_data['action']['alert']
		self._bri = raw_data['action']['bri']
		self._type = raw_data['type']

		self._bridge = bridge

	def __del__(self):
		pass

	def __repr__(self):
		return '<{0}.{1} Object "{2}" at ID {3}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self._name,
            hex(int(self._group_id)))

	def __str__(self):
		return 'Group ' + self._name + " ID: " + str(self._group_id) +  ' ' + self.str_state()

	def str_state(self):
		return '{on : ' + str(self.on) + ', bri : ' + str(self.bri) + '}'

	@property
	def group_id(self):
		return self._group_id

	@property
	def name(self):
		return self._name

	@property
	def hue(self):
		return self._hue

	@property
	def sat(self):
		return self._sat

	@property
	def bri(self):
		return self._bri

	@property
	def xy(self):
		return self._xy

	@property
	def on(self):
		return self._on

	@on.setter
	def on(self, value):
		self.set_group({'on':value})


	def ON(self):
		self.on = True

	def OFF(self):
		self.on = False

	def set_group(self, value):
		group_id = self._group_id

		logging.info('Setting Group: ' + str(group_id))

		self._bridge.send_request('groups/' + str(group_id) + '/action', data=value, method='PUT')



class Group(object):
	def __init__(self, group):
		self._bridge = group._bridge
		self._group_id = group.group_id

	def __repr__(self):
		return repr(self._bridge.get_group(self._group_id))

	def __str__(self):
		return str(self._bridge.get_group(self._group_id))

	@property
	def on(self):
		group = self._bridge.get_group(self._group_id)
		return group.on

	@on.setter
	def on(self, value):
		group = self._bridge.get_group(self._group_id)
		if value:
			group.ON()
		else:
			group.OFF()


	def update(self):
		self._bridge.update()

	def ON(self):
		group = self._bridge.get_group(self._group_id)
		group.ON()

	def OFF(self):
		group = self._bridge.get_group(self._group_id)
		group.OFF()

###############################################################################
##													END GROUP SECTION 															 ##
###############################################################################


###############################################################################
##												START BRIDGE SECTION 															 ##
###############################################################################

class Bridge(object):
	'''
	Hue Bridge

	This is the core of zPyHue. There should only need to be one
	bridge object. The bridge object manages all the other objects
	and is able to look them up as needed. It also loads the config
	file and settigns.
	'''

	def __init__(self, config_file=None):
		self._ip = None
		self._username = None
		self._name = None
		self._rCount = 0
		self._lights = []
		self._groups = []

		if config_file:
			self._ip = '10.10.202.104'
			self._username = '15946c956413d2e011d7763a649433cf'
			#pass #TODO: Add config file parser
		if not self._ip:
			self.get_ip()
		if not self._username:
			self.register()



	def send_request(self, path, data=None, method='GET', return_json=True, no_username=False):
		if data:
			data = json.dumps(data)

			logging.info('Data: ' + data)

		url = ''
		if (no_username or not self._username):
			url = 'http://' + str(self._ip) + '/' + path
		else:
			url = 'http://' + str(self._ip) + '/api/' + self._username + '/' + path

		logging.info('Request URL: ' + url + ' Method: ' + method)

		if method == 'POST':
			r = requests.post(url, data=data)
			if return_json:
				return r.json()
			return r

		if method == 'PUT':
			r = requests.put(url, data=data)
			if return_json:
				return r.json()
			return r

		if method == 'GET':
			if data:
				r = requests.get(url, data=data)
			else: 
				r = requests.get(url)
			if return_json:
				return r.json()
			return r


	def get_ip(self):
		data = requests.get('http://www.meethue.com/api/nupnp')
		try:
			self._ip = data.json()[0]['internalipaddress']
		except:
			logging.error('Problem parsing IP Address of Bridge')
			exit()
		if not self._ip:
			logging.error('Problem parsing IP Address of Bridge')
			exit()

		logging.info('IP address: ' + str(self._ip))

	def register(self):
		request_data = {'devicetype':'zPyHue'}
		response = self.send_request('api', request_data, method='POST', no_username=True)[0]
		
		logging.info('Response: ' + str(response))

		if 'error' in response:
			if response['error']['type'] == 101:
				logging.info('Please press the hue button.')
				sleep(3)
				if (self._rCount < 30): 
					self.register()
				else:
					raise HueButtonNotPressed("Hue button was not pressed in the last 60 seconds")

		if 'success' in response:
			self._username = response['success']['username']
			logging.info('Success! username: ' + str(self._username))

	def get_all(self):
		'''Returns all from /api/username'''
		return self.send_request('api/' + str(self._username), no_username=True)

	def get_lights(self):
		'''Get all lights'''
		lights = self.send_request('lights')
		self._lights = []
		for light in lights:
			self._lights.append(LightObject(lights[light], self, light))

	def get_light(self, light_id):
		#self.get_lights()
		if isinstance(light_id, int):
			for light in self._lights:
				if light.light_id == light_id:
					return light

		for light in self._lights:
			if light.name == light_id:
				return light

	def get_light_control(self, light_id):
		return Light(self.get_light(light_id))

	def get_all_light_controls(self):
		#self.get_lights()
		all_lights = {}
		for light in self._lights:
			all_lights[light._name] = self.get_light_control(light._name)
		return all_lights




	def get_groups(self):
		'''Get all groups'''
		groups = self.send_request('groups')
		self._groups = []
		for group in groups:
			self._groups.append(GroupObject(groups[group], self, group))

	def get_group(self, group_id):
		#self.get_groups()
		if isinstance(group_id, int):
			for group in self._groups:
				if group.group_id == group_id:
					return group

		for group in self._groups:
			if group.name == group_id:
				return group

	def get_group_control(self, group_id):
		return Group(self.get_group(group_id))

	def get_all_group_controls(self):
		self.get_lights()
		all_groups = {}
		for group in self._groups:
			all_groups[group._name] = self.get_group_control(group._name)
		return all_groups



	def update(self):
		self.get_lights()
		self.get_groups()


###############################################################################
##													END BRIDGE SECTION 															 ##
###############################################################################
	





def setup(args):
	'''Basic config setup'''
	if args.debug:
		logging.basicConfig(level=logging.DEBUG)
		logging.info('Debug Enabled')

	return True

def main():
	

	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--debug', required=False, help='Allow Debugging', action='store_true')
	parser.add_argument('-c', '--config', required=False, help='Mock Config File', action='store_true')

	args = parser.parse_args()

	if (setup(args)):
		logging.info('Setup Finished')
	myBridge = Bridge(config_file=args.config)
	myBridge.update()
	all_lights = myBridge.get_all_light_controls()
	all_groups = myBridge.get_all_group_controls()

	all_groups['c.All Hue'].on = not all_groups['c.All Hue'].on



	stairs =  all_lights['Stairs']
	stairs.update()

	stairs.on = not stairs.on

	print stairs

if __name__ == '__main__':
	main()


