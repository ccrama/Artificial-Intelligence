Name: Arnav Garg
UTA ID: 1001039593

Programming Language Used: Python

----------------------------------------
Code Structure:
----------------------------------------
There are 3 files in total:
	1) Node.py
	2) find_route.py
	3) <input_file_name.ext>

Node.py
--------
This file contains the Node class in which we have the following attributes:
	1) City Name: This holds the city name for the node value. 
	2) Parent Node: This holds the reference to the parent node to this node
	3) Total Cost: This holds the total cost to reach this city from the origin city.
	4) Route Cost: This holds the cost to reach this city from the parent node.

find_route.py
-------------
This contains the following functions:
 1)get_data:
	@description: This function gets the data from input file provided with the assignment.
	@params: 
	    file_name: The name of the file from where we have to collect the data
	@return: returning a list of lines collected from the input file provided.

 2) get_adjacent_nodes:
 	@description: This function gets all the adjacent nodes connected to a city node.
	@params:
	    fringe: This contains all the nodes that are under consideration at the moment for finding the path
	    routes: all the routes in the map, this would help us find the nodes in the map.
	    explored_city: this is a list that contains all the cities that we have already explored.
	    destination_city: the destination city name we have to reach.
	@return None

3)	retrace_path:
	@description: This function re-traces the path from the destination node to the origin_city.
	@params:
	    destination_node: this is the destination node that we have to reach.
	@return: None

4)	uninformed_search_helper:
	@description: This is the helper function for performing the uninformed search
	@param:
	    routes: contains all the routes that we got from the input file.
	    origin: the origin node that contains the details of the origin city.
	    destination_city: contains the destination city name.
	@return None

5)	uninformed_search:
	@description: this function performs the uninformed search.
	@params:
	    routes: contains all the routes that we got from the input file.
	    origin: the origin node that contains the details of the origin city.
	    destination_city: contains the destination city name.
	@returns: None

6) main:
	The main function. Starting point of the code.

----------------------------------------
HOW TO RUN THE CODE
----------------------------------------
The command to run the code is given below:
	python find_route.py <input_filename.ext> <origin> <destination>

example:
	python find_route.py input1.txt bremen frankfurt

NOTE: Make sure the find_route.py , Node.py and the input file are in the same directory.












