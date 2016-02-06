#! /usr/bin/python


import argparse
import json
import logging
import requests
from time import sleep


class HueButtonNotPressed(Exception):
	pass

class Light(object):
	'''Hue Light Class'''
	def __init__(self, raw_data, bridge):
		self._name = raw_data['name']
		self._uniqueid = raw_data['uniqueid']
		self._manufacturername = raw_data['manufacturername']
		self._swversion = raw_data['swversion']
		self._modelid = raw_data['modelid']
		self._bridge = bridge



class Bridge(object):
	'''Hue Bridge'''

	def __init__(self, config_file=None):
		self._ip = None
		self._username = None
		self._name = None
		self._rCount = 0
		self._lights = []

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

		if method == 'GET':
			if data:
				r = requests.get(url, data=data)
			else:
				print 
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
			self._lights.append(Light(lights[light], self))





def setup(args):
	'''Basic config setup'''
	if args.debug:
		logging.basicConfig(level=logging.DEBUG)
		logging.info('Debug Enabled')

	return True

def main():
	

	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--debug', required=False, help='Allow Debugging', action='store_true')

	args = parser.parse_args()

	if (setup(args)):
		logging.info('Setup Finished')
		myBridge = Bridge(config_file=True)
		print myBridge.get_lights()

if __name__ == '__main__':
	main()


