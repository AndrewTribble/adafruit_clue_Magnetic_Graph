import board
import displayio
import time
import pulseio
import terminalio
import simpleio
from adafruit_clue import clue 
from adafruit_display_text import label

#get our display on the board
display = board.DISPLAY

# Open the file
with open("/background.bmp", "rb") as background_file:
    # Setup the file as the bitmap data source
    background = displayio.OnDiskBitmap(background_file)
 
    # Create a TileGrid to hold the bitmap for the background
    tile_grid = displayio.TileGrid(background, pixel_shader=displayio.ColorConverter())
 
    # Create a Group to hold all of our Ui elements
    group = displayio.Group()
    
	# Define our color palette to draw the graph with
    palette = displayio.Palette(5)
    palette[0] = 0x000000
    palette[1] = 0xff0000
    palette[2] = 0x00ff00
    palette[3] = 0x0040ff
    palette[4] = 0xffffff

    
	# Create our graph to draw on
    graph = displayio.Bitmap(display.width, display.height-24, 5)
    graph_grid = displayio.TileGrid(graph, pixel_shader=palette)

	# Get the font from terminalio to draw text with
    font = terminalio.FONT
    
	# spin up a label to draw the raw sensor output
    Sensor_Raw = label.Label(font, max_glyphs=50, color=0x000000)

	# position our UI elements how we want them
    Sensor_Raw.x = 5
    Sensor_Raw.y = 234
    graph_grid.y = 12
    
	# Add all of our elements to the DisplayIO group
    group.append(tile_grid)
    group.append(graph_grid)
    group.append(Sensor_Raw)
    
	# Draw the DisplayIO group to the screen
    display.show(group)
     
	# Enter our endless loop where our run-time logic occurs
    while True:
		# Loop over each column of pixels on the screen. This will draw our graph from left to right across the screen one column at a time.
        for column in range(0,display.width):
			# Pull our reading from the mag sensor for this loop. This will serve as the data for this column of pixels.
            SENSOR_VALS = clue.magnetic
			
			# loop over every row on the screen in the Y direction. Here we will do some house-keeping before we draw our datapoints
            for row in range(0, display.height-24):
				# Set every pixel
                graph[column, row] = 0
				# Check if we are not drawing the last two column of pixels to prevent drawing our seek-line outside of the display, causing an IndexError
                if column < display.width-2:
				# Draw a solid white seek-line one column to the right of our current position to make it visually appearant where our current data is drawn
                    graph[column+1, row] = 4
			# Pull the values from the SENSOR_VALS tuple and draw them on the graph one by one. For each value,
			# we get the value from the tuple, and use simpleio to "map_range" the value readout.
			# This allows us to convert the -480 to 480 from the sensor into the y value we need for our graph.
            graph[column, int(simpleio.map_range(SENSOR_VALS[0], -500, 500, 12, display.height-24))] = 1
            graph[column, int(simpleio.map_range(SENSOR_VALS[1], -500, 500, 12, display.height-24))] = 2
            graph[column, int(simpleio.map_range(SENSOR_VALS[2], -500, 500, 12, display.height-24))] = 3
			
			# Draw the sensor readout using string format to round off the decimal and add some padding between values.
            Sensor_Raw.text = "X:{:<10.0F} Y:{:<10.0F} Z:{:<10.0F}".format(*SENSOR_VALS)
