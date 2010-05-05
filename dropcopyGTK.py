import pygtk
import gtk
import os

class DropCopyGTK:
	
	# Main window properties
	WINDOW_HEIGHT = 300
	WINDOW_WIDTH = 100	
	
	# Buttons properties
	BUTTON_HEIGHT = 30
	BUTTON_WIDTH = 80
	FILE_CHOOSER_WIDTH = 16
	
	# Main window and container
	main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	fixed_container = gtk.Fixed()
	
	file_chooser = None
	
	def __init__(self):
		self.build_window()
		self.build_file_chooser()
		self.build_save_button()
		self.build_cancel_button()
		self.main_window.add(self.fixed_container)
		self.main_window.show_all()

	def build_window(self):	
		self.main_window.set_resizable(False)
		self.main_window.set_default_size(self.WINDOW_HEIGHT, self.WINDOW_WIDTH)
		self.main_window.set_border_width(10)
		self.main_window.set_title('DropCopy')
		self.main_window.connect('destroy', self.destroy)

	def build_file_chooser(self):
		self.file_chooser = gtk.FileChooserButton('Select the GnuCash file')
		self.file_chooser.set_current_folder(os.getenv('HOME'))
		self.file_chooser.set_width_chars(self.FILE_CHOOSER_WIDTH)
		self.fixed_container.put(self.file_chooser, 5, 1)

	def build_save_button(self):
		save_button = gtk.Button('Save')
		save_button.set_size_request(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
		save_button.connect('clicked', self.save_dirs)
		self.fixed_container.put(save_button, 5, 50)

	def build_cancel_button(self):
		cancel_button = gtk.Button('Cancel')
		cancel_button.set_size_request(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
		cancel_button.connect('clicked', self.destroy)
		self.fixed_container.put(cancel_button, 100, 50)

	def save_dirs(self, widget, data=None):
		gnu_cash_file = self.file_chooser.get_filename()
		if gnu_cash_file != None:
			print 'saving ' + gnu_cash_file
		else:
			self.build_and_show_error_dialog()

	def build_and_show_error_dialog(self):
		error_message = 'You have to choose a GnuCash file'
		must_select_file_dialog = gtk.Dialog(title='Error', parent=self.main_window, flags=gtk.DIALOG_MODAL)
		ok_error_dialog = must_select_file_dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		#ok_error_dialog.connect('clicked', must_select_file_dialog.destroy)
		#must_select_file_dialog.put(error_message, 1, 1)
		must_select_file_dialog.show()

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def main(self):
		gtk.main()

if __name__ == "__main__":
	hello = DropCopyGTK()
	hello.main()
	