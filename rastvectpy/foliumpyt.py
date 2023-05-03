"""Main module: visualize vector data with folium"""

import folium

class Map(folium.Map):
    """Create a folium map object

    Args:
        folium (_type_): _description_
    """
    # def __init__(self, location=None, width='100%', height='100%', **kwargs):
    #     super().__init__(location=location, width=width, height=height, **kwargs)
    def __init__(self, center=[20, 0], zoom = 2, width='100%', height='100%', **kwargs)-> None:
        """Initialize a folium map object

        Args:
            center (list, optional): the map location or center. Defaults to [20, 0].
            zoom (int, optional): the map zoom level. Defaults to 2.
            width (str, optional): the map width. Defaults to '100%'.
            height (str, optional): the map height. Defaults to '100%'.
        """        
        super().__init__(location=center, zoom_start=zoom, width=width, height=height, **kwargs)


    def add_tile_layer(self, url, name, attribution ='', **kwargs):
        """Add a tile layer to the map.

        Args:
            url (str): The tile layer url.
            name (str): The tile layer name.
            attribution (str, optional): The tile layer attribution. Defaults to ''.
            kwargs: Additional keyword arguments to pass to the tile layer constructor.
        """        
        tile_layer = folium.TileLayer(url=url, name=name, attr=attribution, **kwargs)
        self.add_child(tile_layer)
    

    def add_basemap(self, basemap="HYBRID", show=True, **kwargs):
        """Add a basemap to the map.

        Args:
            basemap (str, optional): Name of the basemap. Defaults to "HYBRID".
            show (bool, optional): Whether to show the basemap in the layer control. Defaults to True.
            kwargs: Additional keyword arguments to pass to the basemap constructor.
        """        
        basemap = basemap.upper()
        if basemap == "HYBRID":
            self.add_tile_layer(name="Google Satellite", tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google", show=show, **kwargs)
        elif basemap == "ROADMAP":
            self.add_tile_layer(name="Google Maps", tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", attr="Google", show=show, **kwargs)
        elif basemap == "TERRAIN":
            self.add_tile_layer(name="Google Terrain", tiles="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}", attr="Google", show=show, **kwargs)
        elif basemap == "SATELLITE":
            self.add_tile_layer(name="Google Satellite", tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", attr="Google", show=show, **kwargs)
        elif basemap == "SATELLITE_ONLY":
            self.add_tile_layer(name="Google Satellite", tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google", show=show, **kwargs)
        elif basemap == "ROADMAP_ONLY":
            self.add_tile_layer(name="Google Maps", tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", attr="Google", show=show, **kwargs)
        else:
            raise ValueError("Unknown basemap: {}".format(basemap))


    def add_geojson(self, data, name="GeoJSON", show=True, **kwargs):
        """Add a GeoJSON layer to the map.

        Args:
            data (str, dict): The GeoJSON data or URL to the GeoJSON data.
            name (str, optional): The layer name. Defaults to "Untitled".
            show (bool, optional): Whether to show the layer in the layer control. Defaults to True.
            kwargs: Additional keyword arguments to pass to the GeoJSON constructor.
        """        
        geo_json = folium.GeoJson(data=data, name=name, show=show, **kwargs)
        self.add_child(geo_json)


    def add_shp(self, in_shp, name="Shapefile", show=True, **kwargs):
        """Add a shapefile to the map.

        Args:
            in_shp (str): The input shapefile path.
            name (str, optional): The layer name. Defaults to "Untitled".
            show (bool, optional): Whether to show the layer in the layer control. Defaults to True.
            kwargs: Additional keyword arguments to pass to the GeoJSON constructor.
        """        
        geo_json = folium.GeoJson(data=in_shp, name=name, show=show, **kwargs)
        self.add_child(geo_json)