# Handles the configuration file

import os
import ConfigParser

class DropcopyConfig:
	
	_CONFIG_FILE = "dropcopy.conf"
	
	def save_preferences(self, gnu_cash_file, dropbox_folder):
		preferences = ConfigParser.RawConfigParser()
		preferences.set('DEFAULT', 'gnucashfile',  gnu_cash_file)
		preferences.set('DEFAULT', 'dropboxfolder',  dropbox_folder)
		with open(self._CONFIG_FILE, 'w') as config_file:
			preferences.write(config_file)