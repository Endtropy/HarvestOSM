# HarvestOSM

HarvestOSM is package design to harvest data from OSM. The idea of the package is to screen the user from necessity to 
know overpassQL statement via simple python interface while providing the possibility to write complex statements.

**Install** 
<br>`$ git clone https://github.com/Endtropy/HarvestOSM.git` </br>
<br>`$ cd HarvestOSM`</br>
<br>`$ python setup.py install`</br>

**Usage**

<br>Interaction with OSM is provided via classes Node and Way that represent OSM elements node a and way 
*(relations are not supported in current version)*.</br>
 <br>`from harvestosm import Node, Way` </br>
<br>Node and Way need to specify the Are of interest. Area of interest can be shapely polygon or an 
object with \_\_geo_interface\_\_. 
 <br>`area = shapely.Polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])`</br>
 <br>`node = Node(area)`</br>
 <br> **or**</b>
 
 optionally followed by OSM tag 
 
 
 
<br>`$ cd harvestosm`</br>
<br>`$ python setup.py install`</br>

	
