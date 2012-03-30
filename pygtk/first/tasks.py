#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import pango
import sys

class MainWindowRow(gtk.VBox):
	def __init__(self):
		super(self.__class__, self).__init__()

	def assign(self, item_id, date, content):
		self.item_id = item_id
		self.date = date
		self.content = content
		self.__init_row()

	def __get_date(self):
		label = gtk.Label(self.date)
		label.set_alignment(0, 0)
		label.set_padding(15, 5)
		fontdesc  = pango.FontDescription('Purisa 9')
		label.modify_font(fontdesc)
		return label

	def __get_content(self):
#		buffer = gtk.TextBuffer()
#		buffer.set_text(self.content)
#		text = gtk.TextView(buffer)
#		text.set_editable(False)
#		text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))
#		text.set_cursor_visible(False)
		text = gtk.Label(self.content)
		text.set_alignment(0, 0)
		text.set_padding(15, 0)
		return text

	def __init_row(self):
#		self.set_border_width(10)
		self.add(self.__get_date())
		self.add(self.__get_content())

class MainWindowContent(gtk.VBox):
	def __init__(self):
		super(MainWindowContent, self).__init__()

		rows = [('1', '12.12.2011', 'Hello world'),
			('2', '14.12.2011', 'No!!! Not this world again!!!')]

		for item_id, date, content in rows*10:
			self.add_item(item_id, date, content)

#		self.pack_start(box, False)

	def add_item(self, *params):
		row = MainWindowRow()
		row.assign(*params)
		event_box = gtk.EventBox()
		event_box.add(row)
#		event_box.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65535, 65535, 65535))
		self.pack_start(event_box, False, True, 5)

class MainWindow(gtk.Window):
	def __init__(self):
		super(MainWindow, self).__init__()
		
		self.set_title('Tasks')
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_default_size(640, 600)
		self.set_geometry_hints(min_width=640, min_height=600)
		self.set_icon_from_file('tray_icon.png')
		self.connect('delete-event', self.hide)

		scrolled_window = gtk.ScrolledWindow()
		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrolled_window.add_with_viewport(MainWindowContent())
		self.add(scrolled_window)
		
		self.show_all()

	def hide(self, widget, event=None):
		super(self.__class__, self).hide()
		return True

class TasksMainMenu(gtk.Menu):
	def __init__(self, main_window):
		super(TasksMainMenu, self).__init__()
		self.main_window = main_window
		self.__init_menu()
		self.show_all()

	def __init_menu(self):
		self.__new_item('Show Tasks', self.on_tray_activate)
		self.__new_item('Quit', self.quit)

	def __new_item(self, title, callback):
		menu_item = gtk.MenuItem(title)
		menu_item.connect('activate', callback)
		self.append(menu_item)
		return menu_item

	def on_tray_activate(self, widget, event=None):
		self.main_window.present()

	def on_tray_popup(self, status, button, time):
		self.popup(None, None, None, button, time)

	def quit(self, widget, event=None):
		gtk.main_quit()
		return False

class Tasks():
	def init_tray(self, icon_path):
		self.tray = gtk.status_icon_new_from_file(icon_path)
		self.tray_menu = TasksMainMenu(self.window)
		self.tray.connect('activate', self.tray_menu.on_tray_activate)
		self.tray.connect('popup-menu', self.tray_menu.on_tray_popup)
		self.tray.set_visible(True)

	def __init__(self):
		self.window = MainWindow()
		self.init_tray('tray_icon.png')
		gtk.main()

if __name__ == "__main__":
	Tasks()
