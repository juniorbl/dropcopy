import pygtk
import gtk

class DropCopyGTK:
	
	# Main window properties
	WINDOW_HEIGHT = 300
	WINDOW_WIDTH = 100	
	
	# Buttons properties
	BUTTON_HEIGHT = 80
	BUTTON_WIDTH = 30
	
	# Main container
	fixed_container = gtk.Fixed()
	
	def __init__(self):
		self.build_window()
		self.build_file_chooser()
		self.build_save_button()
		self.build_cancel_button()
		self.window.add(self.fixed_container)
		self.window.show_all()
		
	def build_window(self):	
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_resizable(False)
		self.window.set_default_size(self.WINDOW_HEIGHT, self.WINDOW_WIDTH)
		self.window.set_border_width(10)
		self.window.set_title('DropCopy')
		self.window.connect('destroy', self.destroy)
		
	def build_file_chooser(self):
		gnu_cash_file_label = gtk.Label('GnuCash file:')
		self.fixed_container.put(gnu_cash_file_label, 5, 1)
		#build chooser...
		
	def build_save_button(self):
		self.save_button = gtk.Button('Save')
		self.save_button.set_size_request(self.BUTTON_HEIGHT, self.BUTTON_WIDTH)
		self.save_button.connect('clicked', self.save_dirs, 'save_button')
		self.fixed_container.put(self.save_button, 5, 50)
		
	def build_cancel_button(self):
		self.cancel_button = gtk.Button('Cancel')
		self.cancel_button.set_size_request(self.BUTTON_HEIGHT, self.BUTTON_WIDTH)
		self.cancel_button.connect('clicked', self.destroy, 'cancel_button')
		self.fixed_container.put(self.cancel_button, 100, 50)
							
	def save_dirs(self, widget, data=None):
		print 'testing...saved!'
				
	def destroy(self, widget, data=None):
		gtk.main_quit()
		
	def main(self):
		gtk.main()
				
if __name__ == "__main__":
	hello = DropCopyGTK()
	hello.main()

