import requests
from harvestosm.base import BaseMeta
from harvestosm.utils import BASE_PATH, open_json
import geojson
import geopandas

class Overpass(metaclass=BaseMeta):
    CONFIG = BASE_PATH / 'config.json' # define together with BaseMeta metaclass config properties
    POLY_KEYS = open_json('area_tags.json') # osm keys and values define polygon features.used for parsing overpass
    # response int geojson format. Parser includes simple check if closed way is linear ring
    # or polygon based on (https://wiki.openstreetmap.org/wiki/Overpass_turbo/Polygon_Features). It set

    def __init__(self):
        self._osm_json = None
        self._geojson = None
        self._gpd = None
        self._query = ''

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        if not Overpass.query_check(query) == Overpass.query_check(self._query):
            self._query = query
            self.request_overpass
            self._geojson = Overpass._get_collection(self._osm_json['elements'])

    @staticmethod
    def query_check(query):
        return ''.join(ch for ch in query if not ch.isupper())

    @property
    def request_overpass(self):
        """reqeust overpass with input query and return json object"""
        if self.query is not None:
            payload = {"data": self.query}

            try:
                response = requests.post(
                    self.overpass_endpoint,
                    data=payload,
                    timeout=self.request_timeout,
                    proxies=self.request_proxies,
                    headers=self.request_header,
                )

            except requests.exceptions.Timeout:
                raise TimeoutError(self.request_timeout)

            status = response.status_code

            if status != 200:
                if status == 400:
                    # raise OverpassSyntaxError(query)
                    print('Overpass Syntax Error')
                elif status == 429:
                    # raise MultipleRequestsError()
                    print('Multiple Requests Error')
                elif status == 504:
                    # raise ServerLoadError(self._timeout)
                    print('Server Load Error')
                else:
                    print(f'The request returned status code {status}')
            else:
                response.encoding = "utf-8"
                self._osm_json = response.json()

    @property
    def geojson(self):
        if self._geojson is not None:
            return self._geojson

    # @property
    # def gpd(self):
    #     features = self.geojson
    #
    #     return geopandas.GeoDataFrame.from_features(features, crs={'init':'epsg:3857'})
    #
    @staticmethod
    def _get_collection(elements):
        """Parse overpass json into geojson - multipolygon is not implemented"""
        features = []
        for element in elements:
            if element.get('tags') is not None:
                if element.get('type') == 'node':
                    geom = geojson.Point(coordinates=[element['lon'], element['lat']])
                    features.append(geojson.Feature(element['id'], geom, element['tags']))
                elif element.get('type') == 'way' and (element.get("nodes")[0] == element.get("nodes")[-1]) is False:
                    features.append(Overpass._geojson_feature(element, 'LineString'))
                elif element.get('type') == 'way' and (element.get("nodes")[0] == element.get("nodes")[-1]) is True:
                    if any(Overpass._area_check(key, value) for key, value in element.get('tags').items()) is True:
                        # create polygon feature from closed way after passing the test on polygon tags
                        features.append(Overpass._geojson_feature(element, 'Polygon'))
                    else:
                        features.append(Overpass._geojson_feature(element, 'LineString'))
                else:
                    print(f'problem with {element.get("type")} and id no {element["id"]}')
        return geojson.FeatureCollection(features)

    @staticmethod
    def _get_element_coords(element):
        # extract coords from osm json output
        return [(e.get('lon'), e.get('lat')) for e in element['geometry']]

    @staticmethod
    def _geojson_feature(element, type):
        # create geojson feature based on type
        if type != 'Polygon':
            geom = getattr(geojson, type)(Overpass._get_element_coords(element))
        else:
            geom = getattr(geojson, type)([Overpass._get_element_coords(element)])
        return geojson.Feature(element['id'], geom, element['tags'])

    @staticmethod
    def _area_check(key, value):
        # check if key and value of input element tags are tags of polygon geometry
        try:
            if Overpass.POLY_KEYS[key] == 'all':
                return True
            elif any([value in v for k, v in Overpass.POLY_KEYS[key].items() if k == 'not']) is True:
                return False
            elif any([value in v for k, v in Overpass.POLY_KEYS[key].items() if k == 'is']) is True:
                return True
            else:
                return False
        except KeyError:
            return False
