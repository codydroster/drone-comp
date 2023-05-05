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
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 10)
		self.set_margin_left(5)
		self.set_margin_right(5)
		self.set_margin_top(5)
		self.set_margin_bottom(5)
		
		rollBox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		rollLabel = Gtk.Label("Roll:")
		self.rollValue = Gtk.Label("1500")
		rollLabel.set_xalign(0)
		self.scrollRoll = Gtk.Scrollbar()
		self.scrollRoll.set_size_request(200,0)
		self.scrollRoll.set_range(0,200)
		self.scrollRoll.set_value(100)
		rollBox.add(rollLabel)
		rollBox.add(self.rollValue)

		
		pitchBox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		pitchLabel = Gtk.Label("Pitch:")
		self.pitchValue = Gtk.Label("1500")
		pitchLabel.set_xalign(0)
		self.scrollPitch = Gtk.Scrollbar()
		self.scrollPitch.set_size_request(200,0)
		self.scrollPitch.set_range(0,200)
		self.scrollPitch.set_value(100)
		pitchBox.add(pitchLabel)
		pitchBox.add(self.pitchValue)
		
		
		headingBox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		headingLabel = Gtk.Label("Heading:")
		self.headingValue = Gtk.Label("0")
		headingLabel.set_xalign(0)
		self.scrollHeading = Gtk.Scrollbar()
		self.scrollHeading.set_size_request(200,0)
		self.scrollHeading.set_range(0,200)
		self.scrollHeading.set_value(100)
		headingBox.add(headingLabel)
		headingBox.add(self.headingValue)
		
		
		altitudeBox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		altitudeBox.set_margin_top(5)
		altitudeLabel = Gtk.Label("Altitude:")

		self.altitudeValue = Gtk.Label("240m")
		
		altitudeBox.add(altitudeLabel)
		altitudeBox.add(self.altitudeValue)
		
		
		self.add(rollBox)
		self.add(self.scrollRoll)
		self.add(pitchBox)
		self.add(self.scrollPitch)
		self.add(headingBox)
		self.add(self.scrollHeading)
		self.add(altitudeBox)


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


