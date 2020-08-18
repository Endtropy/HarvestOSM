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
 <br>`area = shapely.geometry.Polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])`</br>
 <br>`node = Node(area)`</br>
 <br> or</b>
 <br>`area = geojson.load(file)`</br>
 <br>`node = Node(area)`</br>
 <br>The `node` variable is equivalent of overpass statement:</br>
 <br>`node(poly: "0.0 0.0 0.0 1.0 1.0 1.0 1.0 0.0 0.0 0.0")->.C; .C out body geom;`</br>
 
 <br>Both classes, Node and Way can contain following tag. Tag can be specify as string:</br>
 <br>`node = Node(area, tag='key')` -> `node.["key"]->.A` </br>
 <br>`node = Node(area, tag='key=value')` -> `node.["key=value"]->.A` </br>
 <br> as list of strings: </br>
 <br>`node = Node(area, tag=['key1','key2')` -> `node.["key1"]["key2"]->.A` </br>
 <br> or as a dictionary: </br>
 <br>`node = Node(area, tag={'key1' :'value1'}` -> `node.["key1"="value1"]->.A` </br>

<br>With single statements can be provided simple operation as union, difference, intersection and recurse via dedicated 
methods.</br>
<br>*Union*</br>
<br>`education = Way(area, tag='building=school').union(Way(area, tag='building=kindergarten'))`</br>
<br>as</br>
<br>`way.area->.B; way.B["building=school"]->.C; way.area->.D; way.D["building=kindergarten"]->.E; (.C;  .E;)->.F;`</br>
<br>*Difference*</br>
<br>`education = Way(area, tag='highway').difference(Way(area, tag='highway=path'))`</br>
<br>as</br>
<br>`way.area->.B; way.B["highway"]->.C; way.area->.D; way.D["highway=path"]->.E; (.C; - .E;)->.F;`</br>
<br>*Intersection*</br>
<br>`education = Way(area, tag='highway').intersection(Way(area, tag='highway=path'), element='node')`</br>
<br>as</br>
<br>`way.area->.B; way.B["highway"]->.C; way.area->.D; way.D["highway=path"]->.E; node.J.L;`</br>
<br>*Recurse*</br>
<br>`education = Way(area, tag='highway').recurse('<')`</br>
<br>as</br>
<br>`way.area->.B; way.B["highway"]->.C; (.C; <;)->.D`</br>

<br>Output of the statement can be harvest as:</br>
* raw json *.to_osm_json()*
* geojson *.to_geojson()*
* geopandas data frame *.to_geopandas()*

*Options*
* lonlat (bool, default = True) specify order of input coordinates. Overpass require order latitude, longitude
while geojson standard is longitude, latitude. If true, order of coordinates is changed
* overpass_timeout (int, default = 360) specify overpass timeout header i.e. [timeout:360]
* overpass_out_format (str, default = 'json') specify overpass output format i.e. [out:json]
* overpass_maxsize (int, default = 1073741824)  specify overpass max output size i.e. [maxsize:1073741824]
* overpass_out (str, default ='out body geom') specify overpass output
* overpass_endpoint "https://overpass-api.de/api/interpreter"



  
  
