
# -*- coding: utf-8 -*-
"""
Keszitette: Gal Mate ( E4U2OE ) - Automatizalt Gyartorendszerek Projekt Nulla feladat

Rovid leiras: A GUI Bluetoothon keresztul kepes csatlakozni egy egy eszkozhoz, nev / MAC cim alapjan.
Majd a Canvasban bal klikkel kikuldheto a kurzor koordinatai. 
A projekt soran ez a ket koordinata adat szolgalt a ket PWM jel eloallitasara ( Szervo es Hajtomu motor reszere ) a Vortex Hovercrafthoz.
"""


from Tkinter import * # GUI-hoz 
import os # command line-hoz es system parancsokhoz pl. COM port	
import math # konverzikhoz, GUI-hoz
import time #adatatvitelhez ( delay )
import bluetooth # bt adatatvitel ( PyBluez modul )

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )  # A Bluetooth adatatvitelhez szukseges globalis deklaracio


class Application(Frame):   # Az alkalmazas osztalya, amelyben négy 
	
	#####################################################################################################################

    def mouseDown(self, event):  # a bal egergomb nyomvatartasa eseten keletkezo esemeny 
		self.lastx = event.x	# az objektumhoz köthető esemény ( kattintás ) 
		self.lasty = event.y
	
	#####################################################################################################################
	
    def mouseMove(self, event):	 # a kurzor mozgatasa eseten event.x és event.y megadja a relativ koordinatakat
		self.lastx = event.x		# hozzárendelés az objektummal kapcsolatos esemenyhez
		self.lasty = event.y		
		self.scale.set(255-event.y)		# a scale widgetek beallitasa az objektummal kapcsolatos esemeny szerint
		self.scale2.set(255-event.x)
		

		 ####################################################################################################################
		
		if (0 <= event.x <= 255) and (0 <= event.y <= 255): 	
		# Ellenorizzuk, hogy a cursor a canvason belul van-e, ugyanis ha elhagyja, ervenytelen ( hibas ) a koordinata erteke
		# Az adatkuldott data frame 4 x 8 bites [ START BYTE + X KOORDINATA + Y KOORDINATA + STOP BYTE ]
		
			sock.send("%s" % 'w')				# START BYTE
			time.sleep(0.1)
		
			n1 = str(event.x).rjust(3, '0')		# X KOORDINATA
												# az RJUST fuggveny arra szolgal, hogy pl. 2 -> 002, azaz 3 szamjegyu ertekke konvertalja az egy szamjegyu int erteket
			sock.send("%s" % (n1))				# sock objektum segitsegevel kikuldheto a koordinata stringje ( n1 )
			time.sleep(0.1)						# a szukseges delay, az adatatvitel frame helyessegenek megorzesehez

	#		os.system("echo %s > COM5" % n1)	# COM5-os portra kikuldes ( csak USB-UART atalakitoval hasznalt tesztuzemhez kellett ez a funkcio, a veglegesben nem hasznaljuk )
			
			n2 = str(event.y).rjust(3, '0')		# Y KOORDINATA
			sock.send("%s" % (n2))
			time.sleep(0.1)

	#		os.system("echo %s > COM5" % n2)
			
			sock.send("%s" % 'q')				# STOP BYTE
			time.sleep(0.1)
			
			os.system('cls')
			print "%d %d" % ((event.x),(event.y))	# csak hogy ne vakoskodjak.
			
		else:
			os.system('cls')			# kepernyo torlese ( command line )
			sock.send("%s" % 0)			# hibas koordinata, igy null erteket kuldunk 
			print "Out of range!"		# hatokoron kivul, figyelmeztetes
		
	#####################################################################################################################
	
    def createWidgets(self):	# Maga a GUI - Widgetek létrehozása
		
		def Connect():
	
			os.system('cls')
			print "\n\n    Izombol keresem...\n    Ellenorizd, hogy a Bluetooth eszkozok \n    be vannak-e kapcsolva, es lathatoak-e!"
			
			target_name = search_variable.get()	# Az Entry widget tartalmanak string formaban való atadasa ( param )
			target_address = None	# a Target eszkoz MAC cime elobb NONE, majd a bdaddr ( lookup visszateresi ertek )

			print "    A keresett eszkoz neve: %s" % target_name
			
			# BLUETOOTH ESZKÖZÖK KERESÉSE...
			nearby_devices = bluetooth.discover_devices()

			for bdaddr in nearby_devices:
				if target_name == bluetooth.lookup_name( bdaddr ):
					target_address = bdaddr
					break

			if target_address is not None:
				print "\n    Bluetooth eszkozt talaltam a kovetkezo MAC cimmel:", target_address	# sikeres kereses "target_address" MAC cimmel
			else:
				print "Nem talaltam Bluetooth eszkozt a kozelben."	# sikertelen kereses, ennek tobb oka lehet, pl. kikapcsolt / nem lathato modul
				
			# CSATLAKOZÁSI KÍSÉRLET...
			bd_addr = target_address
			port = 1
			
			sock.connect((bd_addr, port))

			pin = search_variable2.get()
			sock.send(pin) # A tartget eszozunk PIN kodja 1234
		####################################### CONNECT IDENTATION BLOCK VÉGE ###########################################
		
		#	CANVAS
		
		self.draw = Canvas(self, width=255, height=255, bg = 'white', cursor = 'crosshair')
		
		#	CANVAS OBJECTS
		
		coord_x1 = 5
		coord_x2 = 255
		coord_y1 = 0
		coord_y2 = 510
		for i in range(0, 6):
			coord = coord_x1+(i*15), coord_y1+(i*15), coord_x2-(i*15), coord_y2-(i*15)
			arc = self.draw.create_arc(coord, start=0, extent=180)
		i = 6
		coord = coord_x1+(i*15), coord_y1+(i*15), coord_x2-(i*15), coord_y2-(i*15)
		arc = self.draw.create_arc(coord, start=0, extent=180, fill = "red")
		self.draw.pack(anchor = "nw")
		
		
		
		#	LABELS
		
		Label(self, text="Vortex Hovercraft").pack(anchor = S)
		
		Label(self, text="HAJTÓMŰ:").place(x=150, y=320)
		Label(self, text="FÚVÓMŰ:").place(x=150, y=420)
		Label(self, text="SZERVÓ:").place(x=90, y=510)
		
		Frame(relief=SUNKEN, height=2, bg="white").pack()
		
		#	SCALE

		self.scale = Scale(self, from_=255, to=0) 		# HAJTOMU 
		self.scale.pack(anchor=E)
		
		self.scale1 = Scale(self, from_=255, to=0) 		# FUVOMU
		self.scale1.pack(anchor=SE)
		
		self.scale2 = Scale(self, from_=255, to=0, orient = HORIZONTAL) 		# SZERVO
		self.scale2.pack()

		Label(self, text="Eszköz neve:").place(x=20, y=300)
		Label(self, text="Eszköz PIN kodja:").place(x=20, y=400)
		
		# MOUSE CONTROL
		
		Widget.bind(self.draw, "<1>", self.mouseDown)			#self.mouseDown jelentese <1>, balgomb
		Widget.bind(self.draw, "<B1-Motion>", self.mouseMove)	
		
		search_variable = StringVar()
		search_variable2 = StringVar()
		
		self.entry = Entry(self, textvariable = search_variable).place(x=20, y=320)
		self.entry2 = Entry(self, textvariable = search_variable2).place(x=20, y=420)
	#	self.entry.focus_set()
		
		button1 = Button(self, text = "Search & Connect", command = Connect)
		button1.place(x=20, y=350)
		
	#####################################################################################################################
		
    def __init__(self, master=None):   # Az __init__ konstruktorral hozzuk létre a Frame objektumot
		Frame.__init__(self, master)
		Pack.config(self)
		self.createWidgets()
		
	#####################################################################################################################

# A main függvényt, az Application osztályon kívül definiáltuk. 
	
def main():
	root = Tk()
	app = Application(root)
	root.iconbitmap('vh.ico')
	app.mainloop()

main()
