# adafruit_clue_Magnetic_Graph

The purpose of this script is to demonstrate the use of the Adafruit Clue Magnetic sensor, as well as demonstrate the use of DisplayIO to draw a minimal interface.  To do this, I developed a small script which will continually read from the magnetic sensor on the Adafruit Clue board, and then push this data to a loop which draws a line graph using displayio.Bitmap() to draw the graph pixel-by-pixel. The process is heavily documented in the comments found within code.py.
