# Initial point. Loads preferences and run the application

import dropcopy_core
import dropcopy_config
import pyinotify
import os
	
# Preference names
GNUCASH_PREFERENCE = 'gnucashfile'
DROPBOX_FOLDER_PREFERENCE = 'dropboxfolder'

config = dropcopy_config.DropcopyConfig()
gnucash_full_path = config.get_preference(GNUCASH_PREFERENCE)
dropbox_folder = config.get_preference(DROPBOX_FOLDER_PREFERENCE)
gnucash_folder, gnucash_file = os.path.split(gnucash_full_path)
watch_manager = pyinotify.WatchManager()

def main():
	dropcopy = dropcopy_core.DropcopyCore(gnucash_file, dropbox_folder)
	notifier = pyinotify.Notifier(watch_manager, dropcopy)
	when_saved = pyinotify.IN_CREATE
	watch_manager.add_watch(gnucash_folder, when_saved, rec=True)
	notifier.loop()
		
if __name__ == "__main__":
	main()