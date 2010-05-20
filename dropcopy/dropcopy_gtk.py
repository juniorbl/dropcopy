# User Interface using GTK+

import dropcopy_config
import gtk
import pynotify
import os

class DropcopyGTK:
	
	# Main window properties
	_WINDOW_HEIGHT = 300
	_WINDOW_WIDTH = 100	
	
	# Buttons properties
	_BUTTON_HEIGHT = 30
	_BUTTON_WIDTH = 80
	_FILE_CHOOSER_WIDTH = 16
	
	# Icons
	_WINDOW_ICON = 'icons/16x16/dropcopy-logo.png'
	_TRAY_ICON = 'icons/32x32/dropcopy-logo.png'
	_NOTIFICATION_ICON = 'icons/48x48/dropcopy-logo.png'
	
	# Main window and container
	_main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	_fixed_container = gtk.Fixed()
	_main_window.add(_fixed_container)
	
	_gnucash_file_chooser = None
	_dropbox_file_chooser = None
	
	def __init__(self):
		self._build_system_tray()
		self._build_window()
		self._build_gnucash_file_chooser()
		self._build_dropbox_file_chooser()
		self._build_save_button()
		self._build_cancel_button()

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
		save_button.connect('clicked', self._save_dirs)
		self._fixed_container.put(save_button, 50, 80)

	def _build_cancel_button(self):
		cancel_button = gtk.Button('Cancel')
		cancel_button.set_size_request(self._BUTTON_WIDTH, self._BUTTON_HEIGHT)
		cancel_button.connect('clicked', self._hide_preferences)
		self._fixed_container.put(cancel_button, 150, 80)

	def _save_dirs(self, widget, data=None):
		gnu_cash_file = self._gnucash_file_chooser.get_filename()
		dropbox_folder = self._dropbox_file_chooser.get_filename() + os.sep
		if gnu_cash_file != None:
			config = dropcopy_config.DropcopyConfig()
			config.save_preferences(gnu_cash_file, dropbox_folder)
			self._show_dialog('Preferences saved.', gtk.MESSAGE_INFO)
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

	def show_notification(self, message):
		pynotify.init('Dropcopy')
		notification = pynotify.Notification('Dropcopy', message)
		notification.set_icon_from_pixbuf(gtk.gdk.pixbuf_new_from_file(self._NOTIFICATION_ICON))
		notification.set_timeout(3000)
		notification.show()

	def main(self):
		gtk.main()

