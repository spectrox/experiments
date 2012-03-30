#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import sys

class Statist:
	def add_record(self, widget, data=None):
		None
	def destroy(self, widget, data=None):
#		gtk.main_quit()
		self.window.hide_all()
		return True
	def show(self, widget, data=None):
		self.window.set_visible(True)
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.connect("destroy", self.destroy)
		self.window.set_border_width(10)
		self.button = gtk.Button("Add record")
		self.button.connect("clicked", self.add_record, None)
		self.window.add(self.button)
		self.button.show()
		self.window.show()
		gtk.main()

class TrayIcon:
	def __init__(self):
		self.menu = gtk.Menu()
		quit_item = gtk.MenuItem("Quit")
		quit_item.connect("activate", self.close)
		self.menu.append(quit_item)
		self.menu.show_all()
		icon = gtk.status_icon_new_from_file('icon.png')
		icon.connect("activate", self.show)
		icon.connect("popup-menu", self.icon_clicked)
		Statist()
	def icon_clicked(self, status, button, time):
		self.menu.popup(None, None, None, button, time)
	def show(self, widget):
		Statist()
	def close(self, widget):
		sys.exit(0)

if __name__ == "__main__":
	tray = TrayIcon()
