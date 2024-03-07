# Part 3 : Road Trip!


The Goal of the problem is to find the best route from given source to destination. We also have to calculate the total number of segments covered, distance travelled in miles and the cost and time incurred to travel the calculated distance. Additional to this we also need to calculate the number of hours that would take to make a delivery drive.

In our given dataset of major highway segments of the United States (and parts of southern Canada and northern Mexico), we have some missing data points too. For these missing points, we are not provided with any latitude or longitude positions for that position. In these cases, we have considered the average latitude and logitude of neighboorhood locations for the given place and placed an approximate latitude and longitude values.

The best route can be found in different ways. Our approach is to find the distance between source and destination using Haversine Formula:
    hav(c)=hav(a-b)+sin(a)sin(b)hav(C)
Using this formula, we calculating the distance between 

As we have to use a heuristic function and A* algorithm to find best orute. To apply the A* algorithm, we need to define a heuristic function and get the next intermidiate distance based on the priprity decided by the heuristic function. Our Heuristic function would calculate the distanc between the source and destination nodes.

Implementation of solution goes as follows,

1. In the get_route(), we push the initial (start point to the fringe) and have list of visited nodes and path, which would prevent us from coming to the same place again and again.

2. Then we find the successor node, the successor node would be one of the neighbooring nodes which ever distance is less to destination when compared to other negihbooring nodes.

3. We also have helper functions for total segment cost, total time cost, total distance cost and one for total delivery distance cost. These functions would return the total cost incurred after reaching th the successor node.

4. In the helper functions mentioned in the above step, we add up the current total cost, current cost and heuristic cost after reaching every location.

5. Here we also have to calculate one more step for delivery drive, if the delivery truck exceeds a speed limit of 50 mph, then the items in the truch would be destroyed. So the cost of this trip would be more for this. In this case, the driver goes back to source node after reaching the destination. We calculate the distance based on the given formula, troad + p · 2(troad + ttrip)

6. By performing all the above steps until we reach the destination, we will have our distance in many routes, out of that we have a function which calculates and returns the minimum distance between given two locations
