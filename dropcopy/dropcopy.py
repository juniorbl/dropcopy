# Initial point. Loads preferences and run the application

import dropcopy_config
import dropcopy_gtk
import pyinotify
import shutil
import gobject
import gtk
import os

gobject.threads_init()

class Dropcopy(pyinotify.ProcessEvent):
	
	# Preference names
	GNUCASH_PREFERENCE = 'gnucashfile'
	DROPBOX_FOLDER_PREFERENCE = 'dropboxfolder'

	dpGTK = dropcopy_gtk.DropcopyGTK()
	config = dropcopy_config.DropcopyConfig()
	gnucash_full_path = config.get_preference(GNUCASH_PREFERENCE)
	dropbox_folder = config.get_preference(DROPBOX_FOLDER_PREFERENCE)
	gnucash_folder, gnucash_file = os.path.split(gnucash_full_path)
	watch_manager = pyinotify.WatchManager()
	
	def __init__(self):
		pyinotify.ProcessEvent.__init__(self)
		self.notifier = pyinotify.ThreadedNotifier(self.watch_manager, self)
		when_saved = pyinotify.IN_CREATE
		self.watch_manager.add_watch(self.gnucash_folder, when_saved, rec=True)
		self.notifier.start()
		self.dpGTK.main()

	# It seems that GnuCash only saves its file, it doesn't update
	def process_IN_CREATE(self, event):
		if event.name == self.gnucash_file:
			shutil.copy(event.pathname, self.dropbox_folder + event.name)
			self._inform_success()

	def _inform_success(self):
		gobject.idle_add(self.dpGTK.show_notification, 'GnuCash file was copied to your local dropbox folder')

if __name__ == "__main__":
	Dropcopy()
