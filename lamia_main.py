import csv
import math
import json

def main():
    # y0: longitude, x0: latitude
	y0 = 60.1692942
	x0 = 24.9258062
	# Max radius of the included services
	d_in = 0.8
	 
	bikes_filename = 'HSL_bikes.csv'
	terminals_filename = 'HSL_terminals.csv'
	services_filename = 'Konrad_data.csv'
	
	# Returns a tuple (name, distance, x, y)
	closest_bike = file_read_and_print_closest("city bike stop", bikes_filename, x0, y0, 11, 12, 2)
	# Returns a tuple (name, distance, x, y)
	closest_terminal = file_read_and_print_closest("terminal", terminals_filename, x0, y0, 0, 1, 4)
	# Returns a list of tuples [(name, distance, x, y), (..), (..)]
	close_services = file_read_and_print_within("Nearby services", services_filename, x0, y0, 1, 2, 5, d_in)

# This function handles the csv reading, handling and returning. ind denotes index i.e. the column of the attribute in the csv file
def file_read_and_print_closest(subject, filename, x0, y0, x_ind, y_ind, name_ind): 
	#TODO: dynamix allocation
	place_list = [None]*400
	num_stops = 0
	with open(filename, 'r') as csvFile:
		reader = csv.reader(csvFile)
		# Read away header
		headers = next(reader, None)
		i = 0
		for row in reader:
			testtuple = tuple(row)
			place_list[i] = testtuple
			#print(testtuple)
			i = i+1
			num_stops = i
	csvFile.close()
	closest_tuple = find_closest(x0, y0, place_list, num_stops, x_ind, y_ind)
	distance = distance_XY(x0, y0, float(closest_tuple[x_ind]), float(closest_tuple[y_ind]))*100
	result_tuple = (closest_tuple[name_ind], distance, closest_tuple[x_ind], closest_tuple[y_ind])
	print closest_tuple[name_ind] + "," + str(distance) + "," + closest_tuple[x_ind] + "," + closest_tuple[y_ind] + "," + ","
	return result_tuple 

# This function handles the csv reading, handling and returning. ind denotes index i.e. the column of the attribute in the csv file. d_within is the maximum distance (km) of the subjects to be included.
def file_read_and_print_within(subject, filename, x0, y0, x_ind, y_ind, name_ind, d_within): 
	#TODO: dynamic allocation
	place_list = [None]*10000
	within_list = [None]*1000
	num_stops = 0
	with open(filename, 'r') as csvFile:
		reader = csv.reader(csvFile)
		# Read away header
		headers = next(reader, None)
		i = 0
		for row in reader:
			testtuple = tuple(row)
			place_list[i] = testtuple
			#print(testtuple[1], testtuple[2])
			i = i+1
			num_stops = i
	csvFile.close()
	within_list = find_within(x0, y0, place_list, num_stops, x_ind, y_ind, d_within)
	#print(within_list)
	within_list_unique = remove_copies(within_list, name_ind)
	within_list_short = [None]*len(within_list_unique)
	i = 0
	for place_tuple in within_list_unique:
		#print(place_tuple)
		distance = distance_XY(x0, y0, float(place_tuple[x_ind]), float(place_tuple[y_ind]))*100	
		# place_tuple[0] is the type of the service, e.g. culture, health care...
		# IFELSE returns the type of service if we look at services. This is an ugly fix.
		if filename == 'Konrad_data.csv':
			within_list_short[i] = (place_tuple[name_ind], distance, place_tuple[x_ind], place_tuple[y_ind], place_tuple[0])
			print place_tuple[name_ind] + "," +  str(distance) + "," + place_tuple[x_ind] +  "," +  place_tuple[y_ind] + "," + place_tuple[0]
		else:
			within_list_short[i] = (place_tuple[name_ind], distance, place_tuple[x_ind], place_tuple[y_ind])
			print place_tuple[name_ind] + "," +  str(distance) + "," + place_tuple[x_ind] +  "," +  place_tuple[y_ind]
		#print("{0} is located {1} m away.".format(place_tuple[name_ind], distance)) 
		i = i+1
	return within_list_short

# Removes copies by name comparison
def remove_copies(place_list, name_ind):
	new_place_list = [None]*len(place_list)
	num_uniques = 0
	for place_tuple in place_list:
		unique = True
		for k in range(num_uniques):
			unique_tuple = new_place_list[k]
			if place_tuple[name_ind] == unique_tuple[name_ind]:
				unique = False
		if unique:
			new_place_list[num_uniques] = place_tuple
			num_uniques = num_uniques + 1
	return new_place_list[:num_uniques]
		
#Distance between two coordinates. From stackoverflow: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def distance_XY(x0, y0, x1, y1):
	# approximate radius of earth in km
	R = 6373.0

	lat1 = math.radians(y0)
	lon1 = math.radians(x0)
	lat2 = math.radians(y1)
	lon2 = math.radians(x1)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

	distance = R * c
	return distance
	# Test
    # print("Result:", distance)
    # print("Should be:", 278.546, "km")    

# Find the closest bus stop given the source coordinates and the HSL list. Returns a tuple
def find_closest(x0, y0, place_list, num_stops, x_ind, y_ind):
	closest_stop = None
	min_dist = 1000000
	# Loop through the stops
	for i in range(num_stops):
		stop_tuple = place_list[i]
		dist = distance_XY(float(x0), float(y0), float(stop_tuple[x_ind]), float(stop_tuple[y_ind]))
		# Check if its the first element in the loop
		if min_dist == -1:
			min_dist = dist
		# Shortest distance?
		if dist < min_dist:
			#print(dist)
		 	min_dist = dist
			closest_stop = stop_tuple
		#print(x0, y0, corr_coord, dist)
	return closest_stop

# Find all the subjects in the list within d_within distance. For example 0.8 km.
def find_within(x0, y0, place_list, num_stops, x_ind, y_ind, d_within):
	i = 0
	j=0
	within_list = [None]*1000
	for i in range(num_stops):
		stop_tuple = place_list[i]
		#print(stop_tuple)
		dist = distance_XY(float(x0), float(y0), float(stop_tuple[x_ind]), float(stop_tuple[y_ind]))
		# Is it within the given distance limit?
		if dist < d_within:
			within_list[j] = stop_tuple
			j = j+1
		i = i+1
	#print(j)
	return within_list[:j]
	
main()
