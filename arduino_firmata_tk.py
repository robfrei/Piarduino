import pyfirmata
from Tkinter import *

# create a new board object - specify serial port
board = pyfirmata.Arduino('/dev/ttyACM0')

# start an iterator thread so serial buffer doesn't overflow
iter8 = pyfirmata.util.Iterator(board)
iter8.start()

# set up pins
# A0 input (LM35)
pin0 = board.get_pin('a:0:i')
# D3 PWM output (LED)
pin3 = board.get_pin('d:3:p')

# IMPORTANT! discard the first reads until A0 gets something valid
while pin0.read() is None:
	pass

def get_temp():
	# LM35 reading in deg C to label
	label_text = "Temp: %6.1f C" % (pin0.read() * 5 *100)
	label.config(text = label_text)
	# reschedule after half second
	root.after(500, get_temp)

def set_brightness(x):
	# set LED
	# scale widget returns 0 .. 100
	# pyfirmata expects 0 .. 1.0
	pin3.write(float(x) / 100.0)

def cleanup():
	# clean up on exit and turn LED off
	pin3.write(0)
	board.exit()

# set up the GUI
root = Tk()

# ensure cleanup() is called on exit
root.wm_protocol("WM_DELETE_WINDOW", cleanup)

# draw a big slider for LED brightness
scale = Scale(root,
		command = set_brightness,
		orient = HORIZONTAL,
		length = 400,
		label = 'Brightness')
scale.pack(anchor = CENTER)

# place label up against scale widget
label = Label(root)
label.pack(anchor = 'nw')

# start temperature read loop
root.after(500, get_temp)

# run Tk event loop
root.mainloop()
