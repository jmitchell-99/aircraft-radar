# ---------- IMPORTS ----------- #
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.widgets import Cursor
from scipy import ndimage
from datetime import datetime
# ---------- END OF IMPORTS ---------- #

class AircraftRadar:

    def __init__(self, lonslats):
        """Initialise instance variables, takes bounding box coordinates as an input which by default
        are set to a bounding box around the UK and Ireland."""

        self.lon_min, self.lon_max, self.lat_min, self.lat_max = lonslats[0], lonslats[1], lonslats[2], lonslats[3]

        # Figure for radar
        self.fig = Figure(figsize = (5.25, 4), facecolor='black')
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        # Axes
        self.ax = self.fig.add_subplot(111)

        # Map and scatter plot
        self.m = Basemap(projection='cyl', llcrnrlat=self.lat_min, urcrnrlat=self.lat_max, llcrnrlon=self.lon_min, urcrnrlon=self.lon_max, resolution=None, ax=self.ax)
        self.m.drawlsmask(land_color='green', ocean_color='aqua', grid=1.25)
        self.m = self.ax.scatter([], [])
        
        # Load image for plotting
        self.airplane_icon = plt.imread('aircraft_red.png')
        self.airplane_icon = (self.airplane_icon*255).astype(np.uint8) # this fixes 'Clipping input data...' lines from being printed

        # Cursor
        self.cursor = Cursor(self.ax, useblit=True, linewidth=0)
        self.cid_mouse_click = self.fig.canvas.mpl_connect('button_press_event', self.mouse_click)

        # Start building GUI
        self.root = Tk()

        # Root config
        self.root.title('Aircraft Radar')
        self.root.maxsize(800, 800)
        self.root.config(bg='black')

        # Frames: Layer 1
        left_frame = Frame(self.root, width=250, height=500, bg='black')
        left_frame.grid(row=0, column=0, padx=10, pady=10)
        right_frame = Frame(self.root, width=500, height=500, bg='black')
        right_frame.grid(row=0, column=1, padx=10, pady=10)

        # Frames: Layer 2
        left_frame_1 = Frame(left_frame, bg='black')
        left_frame_1.grid(row=0, column=0, pady=10)
        left_frame_2 = Frame(left_frame, bg='black')
        left_frame_2.grid(row=1, column=0)
        left_frame_3 = Frame(left_frame)
        left_frame_3.grid(row=2, column=0, pady=5)
        left_frame_4 = Frame(left_frame)
        left_frame_4.grid(row=3, column=0)
        left_frame_5 = Frame(left_frame)
        left_frame_5.grid(row=4, column=0)
        left_frame_6 = Frame(left_frame, bg='black')
        left_frame_6.grid(row=5, column=0)
        left_frame_7 = Frame(left_frame, bg='black')
        left_frame_7.grid(row=6, column=0)

        right_frame_1 = Frame(right_frame, width=525, height=400)
        right_frame_1.grid(row=0, column=0)
        right_frame_2 = Frame(right_frame, width=525, height=50, bg='black')
        right_frame_2.grid(row=1, column=0)

        # Frames: Layer 3
        left_frame_2a = Frame(left_frame_2, bg='black')
        left_frame_2a.grid(row=1, column=0, sticky=W)
        left_frame_2b = Frame(left_frame_2, bg='black')
        left_frame_2b.grid(row=1, column=1, sticky=E)

        left_frame_2c = Frame(left_frame_2, bg='black')
        left_frame_2c.grid(row=2, column=0, sticky=W)
        left_frame_2d = Frame(left_frame_2, bg='black')
        left_frame_2d.grid(row=2, column=1, sticky=E)

        left_frame_2e = Frame(left_frame_2, bg='black')
        left_frame_2e.grid(row=3, column=0, sticky=W)
        left_frame_2f = Frame(left_frame_2, bg='black')
        left_frame_2f.grid(row=3, column=1, sticky=E)

        left_frame_2g = Frame(left_frame_2, bg='black')
        left_frame_2g.grid(row=4, column=0, sticky=W)
        left_frame_2h = Frame(left_frame_2, bg='black')
        left_frame_2h.grid(row=4, column=1, sticky=E)

        # Labels
        label_left_frame_1 = Label(master=left_frame_1, bg='black', fg='white', text='MAP COORDINATES:', font='Bahnschrift 18')
        label_left_frame_1.grid(row=0, column=1)

        label_left_frame_2a = Label(master=left_frame_2a, bg='black', fg='white', text='Min. longitude:', font='Bahnschrift 10')
        label_left_frame_2a.grid(row=0, column=0)
        label_left_frame_2c = Label(master=left_frame_2c, bg='black', fg='white', text='Max. longitude:', font='Bahnschrift 10')
        label_left_frame_2c.grid(row=0, column=0)
        label_left_frame_2e = Label(master=left_frame_2e, bg='black', fg='white', text='Minimum latitude:', font='Bahnschrift 10')
        label_left_frame_2e.grid(row=0, column=0)
        label_left_frame_2g = Label(master=left_frame_2g, bg='black', fg='white', text='Maxmimum latitude:', font='Bahnschrift 10')
        label_left_frame_2g.grid(row=0, column=0)

        label_left_frame_4= Label(master=left_frame_4, bg='black', height=4)
        label_left_frame_4.grid(row=0, column=0)

        self.label_left_frame_5 = Label(master=left_frame_5, bg='black', fg='white', justify=LEFT, text='Callsign: \nCountry of origin: \nLongitude: \nLatitude: \nVelocity: \nTrack: \nLast Contact:', font='Bahnschrift 10')
        self.label_left_frame_5.grid(row=0, column=0)

        label_left_frame_6 = Label(master=left_frame_6, bg='black', height=6)
        label_left_frame_6.grid(row=0, column=0)

        self.label_left_frame_7 = Label(master=left_frame_7, bg='black', fg='white', text='TOTAL AIRCRAFT:', font='Bahnschrift 12')
        self.label_left_frame_7.grid(row=0, column=0)

        # Entries
        self.entry_left_frame_2b = Entry(master=left_frame_2b, bg='black', fg='white', bd=5)
        self.entry_left_frame_2b.grid(row=0, column=0)
        self.entry_left_frame_2d = Entry(master=left_frame_2d, bg='black', fg='white', bd=5)
        self.entry_left_frame_2d.grid(row=0, column=0)
        self.entry_left_frame_2f = Entry(master=left_frame_2f, bg='black', fg='white', bd=5)
        self.entry_left_frame_2f.grid(row=0, column=0)
        self.entry_left_frame_2h = Entry(master=left_frame_2h, bg='black', fg='white', bd=5)
        self.entry_left_frame_2h.grid(row=0, column=0)

        # Matplotlib canvas & toolbar
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame_1)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(self.canvas, right_frame_2)
        toolbar.config(bg='black')
        toolbar.set_message = lambda x: ""      # removes coordinates from showing in toolbar
        toolbar._message_label.config(bg='black')
        toolbar.winfo_children()[-2].config(bg='black')
        toolbar.grid(row=0, column=0)
        toolbar.update()

        # Buttons
        self.button_left_frame_2b= Button(master=left_frame_2b, width=2, bg='grey', fg='black', text='->')
        self.button_left_frame_2b.grid(row=0, column=1)
        self.button_left_frame_2d = Button(master=left_frame_2d, width=2, bg='grey', fg='black', text='->')
        self.button_left_frame_2d.grid(row=0, column=1)
        self.button_left_frame_2f = Button(master=left_frame_2f, width=2, bg='grey', fg='black', text='->')
        self.button_left_frame_2f.grid(row=0, column=1)
        self.button_left_frame_2h = Button(master=left_frame_2h, width=2, bg='grey', fg='black', text='->')
        self.button_left_frame_2h.grid(row=0, column=1)
                
        self.button_left_frame_3 = Button(master=left_frame_3, bg='black', fg='white', text='UPDATE MAP COORDINATES', font='Bahnschrift 8', width='25')
        self.button_left_frame_3.grid(row=0, column=0)

        self.button_right_frame_2 = Button(master=right_frame_2, bg='black', fg='white', text='REFRESH RADAR', font='Bahnschrift 8', width='25')
        self.button_right_frame_2.grid(row=1, column=0)

        # Entry buttons' press counters
        [self.buttoncounter1, self.buttoncounter2, self.buttoncounter3, self.buttoncounter4] = [0, 0, 0, 0]

    def buttons(self):
        """Configure buttons to respective functions."""

        # Button: Entry (x4)
        self.button_left_frame_2b.configure(command=instance.entry1_button)
        self.button_left_frame_2d.configure(command=instance.entry2_button)
        self.button_left_frame_2f.configure(command=instance.entry3_button)
        self.button_left_frame_2h.configure(command=instance.entry4_button)

        # Button: Update map
        self.button_left_frame_3.configure(command=instance.update_map)

        # Button: Refresh radar
        self.button_right_frame_2.configure(command=instance.refresh_radar)

        self.root.mainloop()

    def entry1_button(self):
        """Min. longitude button."""
        
        # Changes entry button's appearance upon a mouse click. It then reverts back to original
        # appearance upon another click and switches between the two appearances upon following clicks.
        self.buttoncounter1 +=1

        if self.buttoncounter1 % 2 == 0:
            self.button_left_frame_2b.configure(bg = 'grey', text='->')
            self.entry_left_frame_2b.delete(0,END)
        else:
            self.button_left_frame_2b.configure(bg = 'light grey', text='x')

    def entry2_button(self):
        """Max. longitude button."""
        self.buttoncounter2 +=1

        if self.buttoncounter2 % 2 == 0:
            self.button_left_frame_2d.configure(bg = 'grey', text='->')
            self.entry_left_frame_2d.delete(0,END)
        else:
            self.button_left_frame_2d.configure(bg = 'light grey', text='x')

    def entry3_button(self):
        """Min. latitude button."""
        self.buttoncounter3 +=1

        if self.buttoncounter3 % 2 == 0:
            self.button_left_frame_2f.configure(bg = 'grey', text='->')
            self.entry_left_frame_2f.delete(0,END)
        else:
            self.button_left_frame_2f.configure(bg = 'light grey', text='x')

    def entry4_button(self):
        """Max. latitude button."""
        self.buttoncounter4 +=1
        
        if self.buttoncounter4 % 2 == 0:
            self.button_left_frame_2h.configure(bg = 'grey', text='->')
            self.entry_left_frame_2h.delete(0,END)
        else:
            self.button_left_frame_2h.configure(bg = 'light grey', text='x')

    def update_map(self):
        """Update map coordinates button."""

        # When all 4 buttons are selected, store the 4 user entries
        if self.buttoncounter1 % 2 != 0 and self.buttoncounter2 % 2 != 0 and self.buttoncounter3 % 2 != 0 and self.buttoncounter4 % 2 != 0:

            new_lonmin = float(self.entry_left_frame_2b.get())
            new_lonmax = float(self.entry_left_frame_2d.get())
            new_latmin = float(self.entry_left_frame_2f.get())
            new_latmax = float(self.entry_left_frame_2h.get())

            # Refresh the radar when all entries inputted are numbers
            if type(new_lonmin) == float and type(new_lonmax) == float and type(new_latmin) == float and type(new_latmax) == float:
                
                self.lon_min, self.lon_max, self.lat_min, self.lat_max = new_lonmin, new_lonmax, new_latmin, new_latmax
                
                self.m = Basemap(projection='cyl', llcrnrlat=self.lat_min, urcrnrlat=self.lat_max, llcrnrlon=self.lon_min, urcrnrlon=self.lon_max, resolution=None, ax=self.ax)
                self.m.drawlsmask(land_color='green', ocean_color='aqua', grid=1.25)
                self.m = self.ax.scatter([], [])
                self.canvas.draw()

                #run_tracker.refresh_radar()
                instance.refresh_radar()

    def refresh_radar(self):
        """Update matplotlib figure with refresh radar button."""

        # Data frame column labels (the OpenSky API will return either 17 or 18 columns of data)
        col_labels17 = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source']
        col_labels18 = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source', 'unknown']

        # Store API's response in data frame
        url = 'https://opensky-network.org/api/states/all?' + 'lamin' + str(self.lat_min) + '&lomin=' + str(self.lon_min) + '&lamax=' + str(self.lat_max) + '&lomax=' + str(self.lon_max)
        response = requests.get(url).json()
        df = pd.DataFrame(response)

        # Dictate actions depending on API's response
        try:
            if len(response['states'][0]) == 18:
                df = pd.DataFrame(response['states'], columns=col_labels18)
                print("17 columns")

            elif len(response['states'][0]) == 17:
                df = pd.DataFrame(response['states'], columns=col_labels17)
                print("18 columns")

        except:
            print("No data received from OpenSky API.")
            pass

        # Extract data for plotting
        df_cols = df[['longitude', 'latitude', 'true_track']]
        array = np.array(df_cols)

        self.xdata, self.ydata, self.tdata = [], [], []

        for i in array:
            self.xdata.append(i[0])
            self.ydata.append(i[1])
            self.tdata.append(i[2])

        # Extract data for annotation
        self.df_info = df[['callsign', 'origin_country', 'last_contact', 'velocity', 'true_track']]

        # Plot invisible points
        self.m.remove()
        self.m = self.ax.scatter(self.xdata, self.ydata, c='red', alpha=0)

        # Remove old icons
        while len(self.ax.artists) > 0:
            self.ax.artists[0].remove()

        # Plot icons over invisible points
        x, y, t = np.atleast_1d(self.xdata, self.ydata, self.tdata)

        for x0, y0, t0 in zip(x, y, t):
            icon_rotated = ndimage.rotate(self.airplane_icon, (t0*-1), reshape=False)   # Rotates image dependent on track
            icon_marker = OffsetImage(icon_rotated, zoom=0.1)
            ab = AnnotationBbox(icon_marker, (x0, y0), frameon=False)
            ab.set_zorder(1)
            self.ax.add_artist(ab)

        # Update 'TOTAL AIRCRAFT:' label
        self.label_left_frame_7.config(text='TOTAL AIRCRAFT: ' + str(len(x)))

        # Refresh canvas and GUI
        self.canvas.draw()
        self.root.update()

    def mouse_click(self, event):
        """Update text box upon mouse click event."""

        # Get x,y locations of mouse click
        xclick = event.xdata
        yclick = event.ydata

        # Calculate distances between all plotted points and mouse click
        self.xdist, self.ydist = [], []
        distances = []

        for x in self.xdata:
            self.xdist.append(float(xclick) - float(x))

        for y in self.ydata:
            self.ydist.append(float(yclick) - float(y))

        for i in range(0, len(self.xdist)):
            distances.append(np.sqrt(self.xdist[i]**2 + self.ydist[i]**2))

        # Find index and x,y position of nearest aircraft to mouse click
        min_dist = min(distances)
        min_dist_i = distances.index(min_dist)
        xclick_x = self.xdata[min_dist_i]
        yclick_y = self.ydata[min_dist_i]

        # Store info about selected aircraft
        callsign = self.df_info['callsign'][min_dist_i]
        country = self.df_info['origin_country'][min_dist_i]
        velocity = self.df_info['velocity'][min_dist_i]
        track = self.df_info['true_track'][min_dist_i]
        last_contact_raw = datetime.fromtimestamp(self.df_info['last_contact'][min_dist_i])     # Get 'last_contact' as datetime
        last_contact = (str(last_contact_raw))[11:]                                             # Format as string, exclude date

        # Update the aircraft info label when the mouse click is close enough to a point
        if min_dist <= 0.25:
            self.label_left_frame_5.config(text='Callsign: {:} \nCountry of Origin: {:} \nLongitude: {:.2f} \nLatitude: {:.2f} \nVelocity: {:}m/s \nTrack: {:}° \nLast Contact: {:}'.format(callsign, country, xclick_x, yclick_y, velocity, track, last_contact))
        else:
            self.label_left_frame_5.config(text='Callsign: \nCountry of Origin: \nLongitude: \nLatitude: \nVelocity: \nTrack: \nLast Contact:')     

if __name__ == "__main__":
    lonlats = [-12.551630, 3.356572, 49.245382, 61.380267]
    instance = AircraftRadar(lonlats)
    instance.buttons()
