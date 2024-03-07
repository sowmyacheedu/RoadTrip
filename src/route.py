#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Sowmya Cheedu (scheedu)
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#


# !/usr/bin/env python3
import math
import sys

def latitude_longitude():
    latlong_points = {}
    with open('city-gps.txt', 'r') as file:
        for line in file:
            latlong_points[line.split()[0]] = (float(line.split()[1]),float(line.split()[2]))
            #print(latlong_points)
    return latlong_points

def latlong_points_notgiven(source_node, loc_segment_data, latlong_points):
    successor_loc = neighbour_nodes(source_node, loc_segment_data)
    avg_x = 0.0
    avg_y = 0.0
    c = 0    #'c' is for count
    for i in successor_loc:
        if (i[1] in latlong_points):
            latitude = latlong_points[i[1]][0]
            longitude = latlong_points[i[1]][1]
            avg_x += latitude
            avg_y += longitude
            c += 1
    if (c == 0): 
        return (0,0)
    avg_x = avg_x/ c
    avg_y = avg_y/c
    return (avg_x, avg_y)

#h_approach 'h' indicates heuristic
def h_approach(start_node,end_node,latlong_points):
    longitude1 = latlong_points[start_node][1] * math.pi / 180.0
    latitude1 = latlong_points[start_node][0] * math.pi / 180.0
    longitude2 = latlong_points[end_node][1] * math.pi / 180.0
    latitude2 = latlong_points[end_node][0] * math.pi / 180.0
    
    dist_long = longitude2 - longitude1
    dist_lat = latitude2 - latitude1
    
    
    x = (pow(math.sin(dist_lat / 2), 2) + pow(math.sin(dist_long / 2), 2) * math.cos(latitude1) * math.cos(latitude2))
    c = 2 * math.asin(math.sqrt(x))
    R = 3956
    dist = R*c
    return dist

def h_latlong_notgiven(start_lat, start_long,target_node,latlong_points):
    longitude1 = start_long * math.pi / 180.0
    latitude1 = start_lat * math.pi / 180.0
    longitude2 = latlong_points[target_node][1] * math.pi / 180.0
    latitude2 = latlong_points[target_node][0] * math.pi / 180.0
    
    dist_long = longitude2 - longitude1
    dist_lat = latitude2 - latitude1
    
    
    a = (pow(math.sin(dist_lat / 2), 2) + pow(math.sin(dist_long / 2), 2) * math.cos(latitude1) * math.cos(latitude2))
    b = 2 * math.asin(math.sqrt(a))
    R = 3963
    d = R*b
    return d

def parse_map(file):
    latlong_points = ''
    with open(file, 'r') as f:
        return [line.split(" ") for line in f.readlines()]
    return latlong_points

def neighbour_nodes(source_node, loc_segment_data):
    successor_loc = []
    for k in loc_segment_data:
        if (str(k[0]) == source_node):
            successor_loc.append(k)
        elif (str(k[1]) == source_node):
            change_successor_loc = []
            change_successor_loc.append(k[1])
            change_successor_loc.append(k[0])
            change_successor_loc.append(k[2])
            change_successor_loc.append(k[3])
            change_successor_loc.append(k[4])
            successor_loc.append(change_successor_loc)
    return successor_loc

def Totalcost_fn(source_node, destination_node, prev_succ, successor_loc, latlong_points, cost):
    if (cost == "segments"):
        #print("entred cost function ")
        return Total_costsegment(source_node, destination_node, prev_succ, successor_loc, latlong_points)
    elif (cost == "distance"):
        return Total_costdist(source_node, destination_node, prev_succ, successor_loc, latlong_points)
    elif (cost == "time"):
        return Total_costtime(source_node, destination_node, prev_succ, successor_loc, latlong_points)


def Total_costdist(source_node, destination_node, prev_succ, successor_loc, latlong_points):
    current_totaldist = prev_succ[6]
    current_dist = successor_loc[2]
    
    if (source_node not in latlong_points):
        loc_segment_data = parse_map("road-segments.txt")
        x,y = latlong_points_notgiven(source_node, loc_segment_data, latlong_points)
        heuristic_cost = h_latlong_notgiven(x,y,destination_node, latlong_points)
    else:
        heuristic_cost = h_approach(source_node, destination_node, latlong_points)

    total_cost = int(current_totaldist) + int(current_dist) + float(heuristic_cost)
    return total_cost

def Total_costtime(source_node, destination_node, prev_succ, successor_loc, latlong_points):
    current_Totaltime = prev_succ[8]
    current_nodetime = float(successor_loc[2]) / float(successor_loc[3])
    if (source_node not in latlong_points):
        
        loc_segment_data = parse_map("road-segments.txt")
        x, y = latlong_points_notgiven(source_node, loc_segment_data, latlong_points)
        heuristic_cost = h_latlong_notgiven(x,y, destination_node, latlong_points)
        
    else:
        heuristic_cost = h_approach(source_node, destination_node, latlong_points)
    
    total_cost = float(current_Totaltime) + float(current_nodetime) + float(heuristic_cost)
    return total_cost

def total_deliverytime_cost(source_node, destination_node, prev_succ, successor_loc, latlong_points):
    current_Totaltime = prev_succ[8]
    
    if (source_node not in latlong_points):
       
        loc_segment_data = parse_map("road-segments.txt")
        x,y = latlong_points_notgiven(source_node, loc_segment_data, latlong_points)
        heuristic_cost = h_latlong_notgiven(x,y,destination_node, latlong_points)
    else:
        heuristic_cost = h_approach(source_node, destination_node, latlong_points)
    if (int(successor_loc[3]) >= 50 ):       
        t_road = float(successor_loc[2]) / float(successor_loc[3])
        t_trip = float(prev_succ[8])
        current_nodetime = t_road + 2*math.tanh(float(successor_loc[2]) / 1000) *(t_road + t_trip)
    else:
        current_nodetime = float(successor_loc[2]) / float(successor_loc[3])
    total_cost = float(current_Totaltime) + float(current_nodetime)  + float(heuristic_cost)
    return total_cost

def Total_costsegment(source_node, destination_node, prev_succ, successor, latlong_points):
    current_Totalsegments = prev_succ[7]
    
    if (source_node not in latlong_points):
        
        loc_segment_data = parse_map("road-segments.txt")
        x,y = latlong_points_notgiven(source_node, loc_segment_data, latlong_points)
        heuristic_cost = h_latlong_notgiven(x,y,destination_node, latlong_points)
    else:
        heuristic_cost = h_approach(source_node, destination_node, latlong_points)
    Total_cost = int(current_Totalsegments) + 1 + float(heuristic_cost)
    return Total_cost


def travelled_path(visited_nodes, final_path):
    visited_nodes_len = len(visited_nodes)
    prev_succ = final_path[0]
    taken_path = []
    taken_path.append(final_path)
    for i in range (visited_nodes_len-2, -1, -1):
        if (visited_nodes[i][1] == prev_succ):
            prev_succ = visited_nodes[i][0]
            taken_path.append(visited_nodes[i])
        if (visited_nodes[i][1] == "starting point"):
            taken_path.append(visited_nodes[i])
            return taken_path
    return list(reversed(taken_path))

def result_of_path_taken(taken_path):
    final_result = []
    total_miles = 0.0
    Total_time = 0.0
    for i in taken_path:
        if (i[0] != "starting point"):
            next_node = i[1]
            st = i[4].replace("\n", "") + " for " + i[2] +" miles"
            s = (next_node, st)
            total_miles += float(i[2])
            time = float(i[2]) / float(i[3])
            Total_time += time
            final_result.append(s)
    return (final_result, total_miles, Total_time)

def deliverytime_of_path_taken(taken_path):
    delivery_time = 0.0
    for i in taken_path:
        if (i[0] != "starting point") :
            if float(i[3]) >= 50 :
                t_road = float(i[2]) / float(i[3])
                t_trip = delivery_time
                curr_Totaltime = t_road + 2*math.tanh(float(i[2]) / 1000) *(t_road + t_trip)
                delivery_time += curr_Totaltime
            else:
                Total_time = float(i[2]) / float(i[3])
                delivery_time += Total_time
    return delivery_time

def minimum_cost(successors):
    minimum = successors[0][5]
    result = successors[0]
    ind = 0
    ind_count = 0
    for i in successors:
        if (i[5] < minimum):
            minimum = i[5]
            result = i
            ind = ind_count
        ind_count += 1
    
    return (result, ind)

def get_route(start, end, cost):

    loc_segment_data = parse_map("road-segments.txt")
    latlong_points = latitude_longitude()
    visited_nodes = []
    visited_path = []
    Initial_node = ["starting point", start,0,0,0,0,0,0,0]
    fringe = [(Initial_node)]
    while fringe:
        mincost_of_succnode, ind = minimum_cost(fringe)
        fringe.pop(ind)
        visited_nodes.append(mincost_of_succnode[1])
        visited_path.append(mincost_of_succnode)
        if mincost_of_succnode[1] == end :
            taken_path = travelled_path(visited_path, mincost_of_succnode)
            final_result, miles, time = result_of_path_taken(taken_path)
            return {"total-segments" : len(final_result), 
            "total-miles" : miles, 
            "total-hours" : time, 
            "total-delivery-hours" : deliverytime_of_path_taken(taken_path), 
            "route-taken" : final_result}
        successor_loc = neighbour_nodes(mincost_of_succnode[1], loc_segment_data)
        for successor in successor_loc:
            if (successor[1] not in visited_nodes):
                if (cost == "delivery"):
                    heuristic_value = total_deliverytime_cost(successor[1], end, mincost_of_succnode, successor, latlong_points)
                    if (int(successor[3]) >= 50 ):
                        probability_speed_count = 1
                        t_road = float(successor[2]) / float(successor[3])
                        t_trip = float(mincost_of_succnode[8])
                        current_nodetime = t_road + 2*math.tanh(float(successor[2]) / 1000) *(t_road + t_trip)
                
                    else:
                        current_nodetime = float(successor[2]) / float(successor[3])
                else:
                    heuristic_value = Totalcost_fn(successor[1],end,mincost_of_succnode, successor, latlong_points, cost)
                    current_nodetime = float(successor[2])/float(successor[3])
                     
                s_list = []
                s_list.append(successor[0])
                s_list.append(successor[1])
                s_list.append(successor[2])
                s_list.append(successor[3])
                s_list.append(successor[4])
                s_list.append(heuristic_value)
                s_list.append(mincost_of_succnode[6] + int(successor[2]))
                s_list.append(int(mincost_of_succnode[7]) + 1)
                s_list.append(float(mincost_of_succnode[8]) + current_nodetime)
                fringe.append(s_list)
            



# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


