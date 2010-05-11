# Handles the copy process

import pyinotify
import shutil
import dropcopy_gtk

class DropcopyCore(pyinotify.ProcessEvent):
	
	_gnucash_file = None
	_dropbox_folder = None
	
	def __init__(self, gnucash_file, dropbox_folder):
		self._gnucash_file = gnucash_file
		self._dropbox_folder = dropbox_folder

	# It seems that GnuCash only saves its file, it doesn't update
	def process_IN_CREATE(self, event):
		if event.name == self._gnucash_file:
			shutil.copy(event.pathname, self._dropbox_folder + event.name)
			self._inform_success()

	def _inform_success(self):
		gtk = dropcopy_gtk.DropcopyGTK()
		gtk.show_notification('GnuCash file was copied to your local dropbox folder')