import threading
import time
import serial
import pygame
import sys
import warnings
warnings.filterwarnings(action="ignore")
from multiprocessing import Process, Manager
from gi.repository import Gtk, Gdk, GLib, GObject




class attitudeBox(Gtk.Box):
	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 5)
		self.rollBox = Gtk.Box(orientation = 'vertical', spacing = 5)
		
		self.rollValue = Gtk.Label("Roll:")
		self.scrollRoll = Gtk.Scrollbar()
		self.scrollRoll.set_size_request(200,0)
		self.scrollRoll.set_range(0,200)
		self.rollBox.add(self.rollValue)
		self.rollBox.add(self.scrollRoll)
		
		self.pitchBox = Gtk.Box(orientation = 'vertical', spacing = 5)

		self.pitchValue = Gtk.Label("Pitch:")
		self.scrollPitch = Gtk.Scrollbar()
		self.scrollPitch.set_size_request(200,0)
		self.pitchBox.add(self.pitchValue)
		self.pitchBox.add(self.scrollPitch)
		
		self.add(self.rollBox)
		self.add(self.pitchBox)

def app_main():

	mainwin = Gtk.Window()
#	mainwin.set_default_size(800, 600)
	mainwin.connect("destroy", Gtk.main_quit)
	attitude = attitudeBox()
	mainwin.add(attitude)

	mainwin.show_all()
	
	
	pygame.display.init()



#	GLib.idle_add(update_gui)
#	GLib.idle_add(background)

#	GLib.timeout_add(15, serialbg)

	Gtk.main()
	
	
app_main()


