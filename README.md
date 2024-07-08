# University Postal Service Delivery System

### Language: Python

### WGU - C950

#### Scenerio:
The purpose of this project is to create a data structure and algorithm for the Western Governors University Parcel Service (WGUPS) to determine the best route and delivery distribution for their Salt Lake City Daily Local Deliveries. 
Packages are currently not being delivered by their promised deadline and a more efficient and accurate solution is necessary. The Salt Lake City route is covered by three trucks, two drivers, and has a daily average of approximately 40 packages.

#### Algorithm Overview:
The core WGUPS Package Routing system utilizes a Nearest Neighbor Algorithm to solve the routing problem.
First, it has a list of the initial points of locations, you choose a starting point, measure the distance for each location inside the list of points you initialize, and then compare each location measuring the distances, then it will select the point that is closest as your "nearest neighbor." 
Once it has its new location, it loops through the distances of each point thereafter and continues the cycle, until all locations have been visited. 

#### Data Structure Overview:
The core data structure WGUPS Package Routing system will utilizes is a Hash Table to solve the routing problem.
Hash tables use key-value pairs to make insertion, deletion, and data retrieval very fast and efficient, O(1) to be specific. The hash table uses a hash function from the key, to find the index where the data is stored inside an array. 
While each key-value pair is stored in an element also referred to as a “bucket”, each bucket typically can contain multiple pairs, in use for collision handling. 


Main function outputs a user friendly and interactive console interface, containing delivery information for all packages or individual packages depending on user input. To see the specific requirements for this project, go to ProjectReq.md.
