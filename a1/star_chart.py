#
# 20/20 excellent.
# 
# You have more comments than necessary.
#
# Generally good choices for additional functions.
#
"""
Oliver Stappas, 1730124
Tuesday, February 5
R. Vincent, instructor
Assignment 1
"""

#Part 1

# DO NOT CHANGE THESE FUNCTIONS

def draw_line(x0, y0, x1, y1, color):
    '''Draw a line connecting two points, given integer coordinates for the
    start position (x0, y0) and end position (x1, y1). The color is a string, 
    either a color name (e.g. 'red') or an RGB value '#RRGGBB'.'''
    canvas.create_line(x0, y0, x1, y1, width=1, fill=color)

def draw_star(x, y, radius, color):
    '''Draw a star as a filled circle with a given center (in pixel
    coordinates), radius (in pixels), and color (as above).'''
    if radius < 1:
        canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill=color, width=1)
    else:
        canvas.create_oval(x - radius,
                           y - radius,
                           x + radius,
                           y + radius,fill=color, width=0)

# BASIC TKINTER INITIALIZATION

import tkinter as tk
SIZE = 1000
wnd = tk.Tk()
canvas = tk.Canvas(wnd, width=SIZE, height=SIZE, background='black')
canvas.pack()
wnd.title('Star chart')

# YOUR MAIN PROGRAM GOES HERE

#######

import math # import math to use log later to calculate the radius of the star 

def add_names_from_file_lines(line_list, names, draper_nbr):
    '''Adds star names from the lines containing the stars in stars.txt
    to names dictionary after dealing with underscores and spaces'''
    if len(line_list) > 5: # line_list contains all the different values for a give star. 
        name = '' # Gives an initial value to the name of the star that will be the keys of the names dictionary
        if len(line_list) == 7: # If there are seven elements in the list, it means that it's a star with a name divided into two names separated by a comma. 
            name = '{} {}'.format(line_list[5], line_list[6]) # This groups the two names into one for future use.
        elif len(line_list) == 6: # When there are 6 values in the line_list
            possible_names = line_list[5] # Possible names is the name or names of the star on the line (can have two names separated by commas)
            index = possible_names.find(',') # Check if the star has two possible names. If it doesn't, index will equal -1
            if index != -1: # When the star has two separate names 
                name, name2 = possible_names[:index], possible_names[index + 1:] # Makes a first name equal to the value before the comma and a second name equal to the value after the comma
                remove_underscore_add_new_name(name2, names, draper_nbr) # See function descripton below
            else: # When the star doesn't have two separate names
                name = possible_names # Make the star's name equal to the 6th value in the list (one name)
        remove_underscore_add_new_name(name, names, draper_nbr) # See function description below
                        
def remove_underscore_add_new_name(name, names, draper_nbr):
    '''Removes the underscores from the star names and adds the new star
    name seperated by a space to the names dictionary as keys'''
    name = name.replace('_', ' ').upper() # Gets rid of the underscores in the star names and replaces them with a space, then makes the entire star name uppercase
    names[name] = draper_nbr # Adds the name of the star as the key in the names dictionary and makes the value the Draper number associated with that star
    
def coords_to_pixel(star_x, star_y, size):
    '''Given x and y coordinates of a star and the size in pixels of the picture,
    returns the x,y location of the star in terms of pixels in the picture.'''
    pixel_x = (float(star_x) + 1) * size/2 # Calculates the x pixel coordinate of a star based on its x coordinate and the size of the screen
    pixel_y = size - (float(star_y) + 1) * size/2 # Calculates the y pixel coordinate of a star based on its y coordinate and the size of the screen
    return (pixel_x,pixel_y) # Return a tuple of the pixel coordinates of the star

def read_coords(file):
    '''Returns three dictionaries from star catalog text file. First keyed on
    Draper numbers, values are tuples with x, y coordinates of each star.
    Second keyed on Draper numbers, contains magnitudes of stars. Third keyed
    on names of stars, values are Draper numbers.'''
    line = file.readline() # Reads a line of the file
    coords = {} # Initializing first dictionary which will later be keyed on Draper numbers, with values of tuples with x, y coordinates of each star
    magnitudes = {} # Initializing second dictionary which will later be keyed on the stars' Draper numbers, with values corresponding to the magnitudes of stars
    names = {} # Initializing third dictionary which will later be keyed on the names of the stars,  with values corresponding to the stars' Draper numbers
    while line: # While there is still a line to read in the file
        line_list = line.split() # Creates a list with each element corresponding to the values on each line (corresponding to an individual star) of the file
        draper_nbr = line_list[1] # The second element in the list (second value on the line) is the Draper number of that star
        y_coordinate = line_list[2] # The third element in the list (third value on the line) is the y coordinate of that star
        x_coordinate = line_list[3] # The fourth element in the list (fourth value on the line) is the x coordinate of that star
        magnitude = float(line_list[4]) # The fifth element in the list (fifth value on the line) is the magnitude of that star
        add_names_from_file_lines(line_list, names, draper_nbr) # See function description above
        coords[draper_nbr] = (x_coordinate, y_coordinate) # Adds the Draper number of the star as the key in the coords dictionary and makes the value a tuple with the coordinates of that star
        magnitudes[draper_nbr] = magnitude # Adds the Draper number of the star as the key in the magnitudes dictionary and makes the value the magnitude of the star
        line = file.readline() # Continues reading the file
    return (coords, magnitudes, names) # Read function description
      
def plot_by_magnitude(size, coords, magnitudes):
    '''Plots all the stars in the dictionaries'''
    for draper_nbr in coords: # For every key in the coords dictionary
        star_x, star_y = coords[draper_nbr] # The x and y coordinates of stars are the first and second values of the values (tuples) in the coords dictionary respectively
        pixel_x, pixel_y = coords_to_pixel(star_x, star_y, size) # Use the coords_to_pixel function (see description above) to transform the coordinates of the stars into pixel coordinates
        radius = math.log(8 - magnitudes[draper_nbr]) # The radius of the stars can be derived from this equation which uses the magnitude of the stars
        color = '#FFFFFF' # Set the color of the stars to white
        draw_star(pixel_x, pixel_y, radius, color) #Plots the stars using the draw_star function (see description above)

def read_constellation_lines(file):
    '''Opens text file, reads constellation data, returns a dictionary keyed
    by source, star name or number, with a value consisting of a list of star
    names or numbers. For each key, the associated list contains all of the stars
    connected by a line form the key star.'''
    lines = {} # An empty dictionary that will later be keyed by star name or number, with a value corresponding to a list of star names or numbers
    line = file.readline() # Read the constellation file
    while line: # While there are still lines to read
        star1, star2 = line.split(',') # Makes one star equal to the first star on each line (before comma) and a second one equal to the second star on that line (after)
        star2 = star2.strip() # Gets rid of the space before the second star
        if star1 not in lines: # Creates an empty list for the values in the lines dictionary
            lines[star1] = []
        lines[star1].append(star2) # Appends the second star on each line to the list that corresponds to the value of the lines dictionary
        line = fp.readline() # Continues reading the file
    return lines # Returns the dictionary in description

def star_to_pixel_coordinates(star, coords, names, size):
    '''Returns the pixel coordinates of a star identified by its Draper
    number or name'''
    if not star.isdigit(): # If a star is represented by a name and not numbers
        star = names[star] # Makes the star input equal to the value (Draper number) associated with that star in the names dictionary
    star_x, star_y = coords[star] # Makes the star coordinates equal to the value (coordinates tuple) associated with that star in the coords dictionary
    return coords_to_pixel(star_x, star_y, size) # See function description above
            
def plot_constellation(coords, lines, names, color, size):
    '''Draws the lines for a given constellation'''
    for star1 in lines: # For every key in the lines dictionary
        x0, y0 = star_to_pixel_coordinates(star1, coords, names, size) # The first star's pixel coordinates are determined from the star_to_pixel_coordinates function (see above)
        for star2 in lines[star1]: # For every value in the lines dictionary
            x1, y1 = star_to_pixel_coordinates(star2, coords, names, size) # The second star's pixel coordinates are determined from the star_to_pixel_coordinates function (see above)
            draw_line(x0, y0, x1, y1, color) # Use the draw_line function to draw the lines for a given constellation (see above)

########
            
fp = open('stars.txt')
coords, magnitudes, names = read_coords(fp)
fp.close()
plot_by_magnitude(SIZE, coords, magnitudes)
constellation_files = [('Auriga_lines.txt',     '#00FFEC'), # Makes a list of tuples containing a file name associated with a constellation and the hexadecimal color desired for that constellation
                       ('BigDipper_lines.txt',  '#FF00EC'),
                       ('Bootes_lines.txt',     '#F7FF00'),
                       ('Cas_lines.txt',        '#1FFF00'),
                       ('Cepheus_lines.txt',    '#FFFFFF'),
                       ('Cyg_lines.txt',        '#FF7562'),
                       ('Draco_lines.txt',      '#FF8B00'),
                       ('UrsaMinor_lines.txt',  '#FF5B8F')]
for fname, color in constellation_files:
    fp = open(fname)
    lines = read_constellation_lines(fp)
    fp.close()
    plot_constellation(coords, lines, names, color, SIZE)

# DO NOT DELETE THIS LINE!
wnd.mainloop()


