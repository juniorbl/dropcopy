# Handles the configuration file

import os
import ConfigParser

class DropcopyConfig:
	
	# User home directory
	_CONFIG_FILE = os.path.expanduser('~') + "/.dropcopy/dropcopy.conf"
	
	def save_preferences(self, gnu_cash_file, dropbox_folder):
		preferences = ConfigParser.RawConfigParser()
		preferences.set('DEFAULT', 'gnucashfile',  gnu_cash_file)
		preferences.set('DEFAULT', 'dropboxfolder',  dropbox_folder)
		with open(self._CONFIG_FILE, 'w') as config_file:
			preferences.write(config_file)

	def get_preference(self, preference_name):
		preferences = ConfigParser.RawConfigParser()
		preferences.read(self._CONFIG_FILE)
		return preferences.get('DEFAULT', preference_name)
