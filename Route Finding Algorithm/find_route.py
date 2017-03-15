'''
@author: Arnav Garg
@studentID: 1001039593
@class: CSE 4308 - 001
'''
import sys
from Node import Node

'''
@description: This function gets the data from input file provided with the assignment.
@params: 
    file_name: The name of the file from where we have to collect the data
@return: returning a list of lines collected from the input file provided.
'''
def get_data(file_name):

    data = []
    try:
        f = open(file_name, 'r')
    except FileNotFound:
        print '[Error] Cannot open the file.'
    else:
        # getting each line from the file.
        data = [line for line in f]
        f.close()
       
    return data;

'''
@description: This function gets all the adjacent nodes connected to a city node.
@params:
    fringe: This contains all the nodes that are under consideration at the moment for finding the path
    routes: all the routes in the map, this would help us find the nodes in the map.
    explored_city: this is a list that contains all the cities that we have already explored.
    destination_city: the destination city name we have to reach.
@return None
'''
def get_adjacent_nodes(fringe, routes, explored_city, destination_city):
    
    city_node = fringe[0];
    # Getting the city name we have to find the adjacent nodes for.
    city_name = city_node.city_name;
    # getting the total current cost till now.
    current_cost = city_node.total_cost;
    # Adding the city into the explored list.
    explored_city.append(city_name)
    # Now that we have taken that city into account, we can delete it.
    del fringe[0];
    
    # looking at the routes wer are given/
    for route in routes:
        if city_name in route:
            '''
                Within this 'if' branch, I'm checking for all the routes for the city and then adding 
                the ones that the city_name is connected to in the fringe. 
            '''
            # In this case the first city is the city_name so I would create a node for the city the city_name is 
            # connected to. I'm also checking if the city is not already in the explored city list. 
            if route[0] == city_name and not(route[1] in explored_city):
                adjacent_city = Node(route[1], city_node, int(current_cost)+int(route[2]), int(route[2]))
                fringe.append(adjacent_city) 
            elif route[1] == city_name and not(route[0] in explored_city):
                adjacent_city = Node(route[0], city_node, int(current_cost)+int(route[2]), int(route[2]))
                fringe.append(adjacent_city)

'''
@description: This function re-traces the path from the destination node to the origin_city.
@params:
    destination_node: this is the destination node that we have to reach.
@return: None
'''
def retrace_path(destination_node):
    
    print 'distance: %d km' % destination_node.total_cost;

    # trace_city: this will contain all the cities in the path
    # trace_cost: this will contain all the costs b/w the cities in the path. 
    trace_city = []
    trace_cost = []
    
    # Loop for the collecting the data.
    while destination_node:
        trace_city.append(destination_node.city_name)
        trace_cost.append(destination_node.route_cost)
        destination_node = destination_node.parent_node;
    
    # Reversing the lists as I have to show from the start to end.
    trace_city.reverse();
    trace_cost.reverse();
    # deleting the first cost of '0' of going from origin to origin. 
    del trace_cost[0];
    
    # Displaying the output.
    print 'route:'
    for i in range(0, len(trace_city)-1):
        trace_city[i] = trace_city[i][0].upper() + trace_city[i][1:]
        trace_city[i+1] = trace_city[i+1][0].upper() + trace_city[i+1][1:]
        print '%s to %s, %d km' % (trace_city[i], trace_city[i+1], trace_cost[i]);

'''
@description: This is the helper function for performing the uninformed search
@param:
    routes: contains all the routes that we got from the input file.
    origin: the origin node that contains the details of the origin city.
    destination_city: contains the destination city name.
@return None
'''
def uninformed_search_helper(routes, origin, destination_city):
    
    # fringe stores all the cities that are under consideration at the momement.
    fringe = [];
    # List of the the cities that have already been explored.
    explored_city = [];

    # Adding the origin to the fringe and explored city list. 
    fringe.append(origin);
    explored_city.append(origin.city_name)
    
    while True:
        # exit condition.
        if not fringe:
            return None;
        # solution has been found.
        if fringe[0].city_name == destination_city:
            return fringe[0];
        # getting the adjacent nodes for the first node in the fringe.
        get_adjacent_nodes(fringe, routes, explored_city, destination_city);
        # sorting the fringe based in the total cost so far. 
        fringe = sorted(fringe, key=lambda node: node.total_cost)
        
'''
@description: this function performs the uninformed search.
@params:
    routes: contains all the routes that we got from the input file.
    origin: the origin node that contains the details of the origin city.
    destination_city: contains the destination city name.
@returns: None
'''
def uninformed_search(routes, origin, destination):
    
    # getting the result from the uninformed search.
    result = uninformed_search_helper(routes, origin, destination);
    # if not result is returned, giving the generic answer.
    if result == None:
        print 'distance: infinity'
        print 'route:'
        print 'none'
    # else tracing the path from the destination node given back to us from the helper function.
    else:
        retrace_path(result);


def main():    

    # Checking for the arguements. 
    if len(sys.argv) < 4:
        print '[USEAGE] python find_route.py <file_name> <origin_city> <destination_city>';
        print 'Note: Remember to have the input file in the same directory as this file.';
        return;


    file_name = sys.argv[1];
    origin_city = sys.argv[2].lower();
    destination_city = sys.argv[3].lower();

    # Getting the data from the input file name provided.
    data = get_data(file_name)

    # If no data is returned, exit.
    if not data:
        return;

    # Finding the routes from data provided. Basically just formatting the data. 
    routes = [route.lower().split() for route in data]
    # Deleting the useless data like "END OF INPUT" and ""
    del routes[len(routes)-1]
    del routes[len(routes)-1]
    
    # Creating an origin node with the city name, parent: None, Total cost: 0 and route_cost: 0.
    origin = Node(origin_city, None, 0, 0);
    uninformed_search(routes, origin, destination_city);


if __name__ == "__main__":
    main()
