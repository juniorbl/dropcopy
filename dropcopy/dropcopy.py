import dropcopy_config
import pyinotify
import pynotify
import shutil
import gobject
import gtk
import os

class Dropcopy(pyinotify.ProcessEvent):
	
	# Main window properties
	_WINDOW_HEIGHT = 300
	_WINDOW_WIDTH = 100	
	
	# Buttons properties
	_BUTTON_HEIGHT = 30
	_BUTTON_WIDTH = 80
	_FILE_CHOOSER_WIDTH = 16
	
	# Icons
	_WINDOW_ICON = 'icons/16x16/dropcopy-logo.png'
	_TRAY_ICON = 'icons/22x22/dropcopy-logo.png'
	_NOTIFICATION_ICON = 'icons/48x48/dropcopy-logo.png'
	
	# Main window and container
	_main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	_fixed_container = gtk.Fixed()
	_main_window.add(_fixed_container)
	
	# Preference names
	GNUCASH_PREFERENCE = 'gnucashfile'
	DROPBOX_FOLDER_PREFERENCE = 'dropboxfolder'
	
	_gnucash_file_chooser = None
	_dropbox_file_chooser = None
	
	_dropbox_folder = None
	_gnucash_folder = None
	_gnucash_file = None

	def __init__(self):
		self._build_system_tray()
		self._build_window()
		self._build_gnucash_file_chooser()
		self._build_dropbox_file_chooser()
		self._build_save_button()
		self._build_cancel_button()
		self._start_monitor()
		gtk.main()
		self.notifier.stop()
	
	def _start_monitor(self):
		self._load_configuration()
		watch_manager = pyinotify.WatchManager()
		self.notifier = pyinotify.ThreadedNotifier(watch_manager, self)
		when_saved = pyinotify.IN_CREATE
		watch_manager.add_watch(self._gnucash_folder, when_saved, rec=True)
		self.notifier.start()

	def _restart_monitor(self):
		self.notifier.stop()
		self._start_monitor()

	def _load_configuration(self):
		config = dropcopy_config.DropcopyConfig()
		gnucash_full_path = config.get_preference(self.GNUCASH_PREFERENCE)
		self._dropbox_folder = config.get_preference(self.DROPBOX_FOLDER_PREFERENCE)
		self._gnucash_folder, self._gnucash_file = os.path.split(gnucash_full_path)

	# It seems that GnuCash only saves its file, it doesn't update
	def process_IN_CREATE(self, event):
		if event.name == self._gnucash_file:
			shutil.copy(event.pathname, self._dropbox_folder + event.name)
			self._show_notification('GnuCash file was copied to your local dropbox folder')

	def _build_window(self):	
		self._main_window.set_resizable(False)
		self._main_window.set_default_size(self._WINDOW_HEIGHT, self._WINDOW_WIDTH)
		self._main_window.set_border_width(10)
		self._main_window.set_title('DropCopy')
		self._main_window.connect('destroy', self._destroy)
		self._main_window.set_icon_from_file(self._WINDOW_ICON)

	def _build_gnucash_file_chooser(self):
		gnucash_label = gtk.Label('GnuCash file:')
		self._fixed_container.put(gnucash_label, 5, 10)
		self._gnucash_file_chooser = gtk.FileChooserButton('Select the GnuCash file')
		self._gnucash_file_chooser.set_current_folder(os.getenv('HOME'))
		self._gnucash_file_chooser.set_width_chars(self._FILE_CHOOSER_WIDTH)
		self._fixed_container.put(self._gnucash_file_chooser, 115, 1)

	def _build_dropbox_file_chooser(self):
		dropbox_label = gtk.Label('Dropbox folder:')
		self._fixed_container.put(dropbox_label, 5, 50)
		self._dropbox_file_chooser = gtk.FileChooserButton('Select the dropbox folder') 
		self._dropbox_file_chooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		self._dropbox_file_chooser.set_current_folder(os.getenv('HOME'))
		self._dropbox_file_chooser.set_width_chars(self._FILE_CHOOSER_WIDTH)
		self._fixed_container.put(self._dropbox_file_chooser, 115, 40)

	def _build_save_button(self):
		save_button = gtk.Button('Save')
		save_button.set_size_request(self._BUTTON_WIDTH, self._BUTTON_HEIGHT)
		save_button.connect('clicked', self._save_preferences)
		self._fixed_container.put(save_button, 50, 80)

	def _build_cancel_button(self):
		cancel_button = gtk.Button('Cancel')
		cancel_button.set_size_request(self._BUTTON_WIDTH, self._BUTTON_HEIGHT)
		cancel_button.connect('clicked', self._hide_preferences)
		self._fixed_container.put(cancel_button, 150, 80)

	def _save_preferences(self, widget, data=None):
		gnu_cash_file = self._gnucash_file_chooser.get_filename()
		dropbox_folder = self._dropbox_file_chooser.get_filename() + os.sep
		if gnu_cash_file != None:
			config = dropcopy_config.DropcopyConfig()
			config.save_preferences(gnu_cash_file, dropbox_folder)
			self._show_dialog('Preferences saved.', gtk.MESSAGE_INFO)
			self._restart_monitor()
			self._hide_preferences()
		else:
			self._show_dialog('You have to choose a GnuCash file.', gtk.MESSAGE_ERROR)

	def _show_dialog(self, error_message, message_type):
		error_dialog = gtk.MessageDialog(self._main_window, gtk.DIALOG_DESTROY_WITH_PARENT, message_type, gtk.BUTTONS_CLOSE, error_message)
		error_dialog.run()
		error_dialog.destroy()

	def _destroy(self, widget):
		gtk.main_quit()
		
	def _build_system_tray(self):
		self.tray = gtk.StatusIcon()
		self.tray.set_from_icon_name(gtk.STOCK_NETWORK)
		self.tray.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(self._TRAY_ICON))
		self.tray.connect('popup-menu', self._show_menu)
		self.tray.set_visible(True)

	def _show_menu(self, data, event_button, event_time):
		menu = gtk.Menu()
		preferences_item = gtk.MenuItem('Preferences')
		exit_item = gtk.MenuItem('Exit')
		menu.append(preferences_item)
		menu.append(exit_item)
		preferences_item.connect_object('activate', self._show_preferences, 'Preferences')
		preferences_item.show()
		exit_item.connect_object('activate', self._destroy, 'Exit')
		exit_item.show()
		menu.popup(None, None, None, event_button, event_time)

	def _show_preferences(self, data=None):
		self._main_window.show_all()

	def _hide_preferences(self, data=None):
		self._main_window.hide()

	def _show_notification(self, message):
		pynotify.init('Dropcopy')
		notification = pynotify.Notification('Dropcopy', message)
		notification.set_icon_from_pixbuf(gtk.gdk.pixbuf_new_from_file(self._NOTIFICATION_ICON))
		notification.set_timeout(3000)
		notification.show()
