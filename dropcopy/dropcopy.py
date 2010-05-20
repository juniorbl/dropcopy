# Initial point. Loads preferences and run the application

import dropcopy_config
import dropcopy_gtk
import pyinotify
import shutil
import gtk
import os
	
# Preference names
GNUCASH_PREFERENCE = 'gnucashfile'
DROPBOX_FOLDER_PREFERENCE = 'dropboxfolder'

dpGTK = dropcopy_gtk.DropcopyGTK()
config = dropcopy_config.DropcopyConfig()
gnucash_full_path = config.get_preference(GNUCASH_PREFERENCE)
dropbox_folder = config.get_preference(DROPBOX_FOLDER_PREFERENCE)
gnucash_folder, gnucash_file = os.path.split(gnucash_full_path)
watch_manager = pyinotify.WatchManager()

class Dropcopy(pyinotify.ProcessEvent):
	
	# It seems that GnuCash only saves its file, it doesn't update
	def process_IN_CREATE(self, event):
		if event.name == gnucash_file:
			shutil.copy(event.pathname, dropbox_folder + event.name)
			self._inform_success()

	def _inform_success(self):
		dpGTK.show_notification('GnuCash file was copied to your local dropbox folder')

def main():
	dropcopy = Dropcopy()
	dpGTK.main()
	notifier = pyinotify.Notifier(watch_manager, dropcopy)
	when_saved = pyinotify.IN_CREATE
	watch_manager.add_watch(gnucash_folder, when_saved, rec=True)
	notifier.loop()
		
if __name__ == "__main__":
	main()
