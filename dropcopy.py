import os
import pyinotify
import shutil

gnucash_full_path = '/directory/gcash.gnc'
dropbox_dir = '/directory/dropcopy/'
gnucash_directory, gnucash_file = os.path.split(gnucash_full_path)

watch_manager = pyinotify.WatchManager()
when_saved = pyinotify.IN_CREATE

class HandleEvents(pyinotify.ProcessEvent):
		# It seems that GnuCash only saves his file.
		def process_IN_CREATE(self, event):
				if event.name == gnucash_file:
						print "Your GnuCash file was saved in", event.pathname
						shutil.copy(event.pathname, dropbox_dir + event.name)
						print "Your GnuCash file was copied to", dropbox_dir
        
drop_copy = HandleEvents()
notifier = pyinotify.Notifier(watch_manager, drop_copy)
watch_manager.add_watch(gnucash_directory, when_saved, rec=True)

notifier.loop()
