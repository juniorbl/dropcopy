import pygtk
import gtk

class DropCopyGTK:
		def __init__(self):
				self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
				self.window.set_title('DropCopy')
				self.window.connect('destroy', self.destroy)
				self.window.set_border_width(10)
				
				self.box_buttons = gtk.HBox(False, 0)
				self.window.add(self.box_buttons)
				
				self.btn_save = gtk.Button('Save')
				self.btn_save.connect('clicked', self.save_dirs, 'btn_save')
				self.box_buttons.pack_start(self.btn_save, True, True, 0)
				self.btn_save.show()
				
				self.btn_cancel = gtk.Button('Cancel')
				self.btn_cancel.connect('clicked', self.destroy, 'btn_cancel')
				self.box_buttons.pack_start(self.btn_cancel, True, True, 0)
				self.btn_cancel.show()
				
				self.box_buttons.show()
				self.window.show()
				
		def save_dirs(self, widget, data=None):
				print 'saved!'
				
		def destroy(self, widget, data=None):
				gtk.main_quit()
		
		def main(self):
				gtk.main()
				
if __name__ == "__main__":
	hello = DropCopyGTK()
	hello.main()

