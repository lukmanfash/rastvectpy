"""Main module."""

import numpy as np
import matplotlib.pyplot as plt
import ipyleaflet
import os
import ipywidgets as widgets
import requests
import pandas as pd
import geopandas as gpd
from IPython.display import display
import collections
import os
import xyzservices.providers as xyz


class Map(ipyleaflet.Map):
    """The Map class inherits ipyleaflet.Map

    Args:
        ipyleaflet (_type_): ipyleaflet module for visualizing vector data
    """    

    def __init__(self, **kwargs)-> None:
        """ Initialize an ipyleaflet map object.

        Args:
            center (_type_): center of the map
            zoom (_type_): zoom level of the map
        """

        if "center" not in kwargs:
            kwargs["center"] = [20, 0]

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        if "layer_control" not in kwargs:
            kwargs["layer_control"] = True

        if kwargs["layer_control"]:
            self.add_layer_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True
                
        super().__init__(**kwargs)

        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()

        if "height" in kwargs:
            self.layout.height = kwargs["height"]
        else:
            self.layout.height = "500px"
     
    def add_search_control(self, position="topleft", **kwargs):
        """Add a search control to the map.

        Args:
            kwargs: Keyword arguments to pass to the ipyleaflet.SearchControl constructor.
        """  
        if "url" not in kwargs:
            kwargs["url"] = "https://nominatim.openstreetmap.org/search?format=json&q={s}"      
        search_control = ipyleaflet.SearchControl(position=position, **kwargs)
        self.add_control(ipyleaflet.SearchControl(**kwargs))

    def add_draw_control(self, **kwargs):
        """Add a draw control to the map.

        Args:
            kwargs: Keyword arguments to pass to the ipyleaflet.DrawControl constructor.
        """  
        draw_control = ipyleaflet.DrawControl(**kwargs)
      
        draw_control.polyline =  {
            "shapeOptions": {
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1.0
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }
        }
        
        self.add_control(draw_control)

    def add_layer_control(self, position="topright", **kwargs):
        """Add a layer control to the map.

        Args:
            kwargs: Keyword arguments to pass to the ipyleaflet.LayersControl constructor.
        """  
        layer_control = ipyleaflet.LayersControl(position=position, **kwargs)
        self.add_control(layer_control)

    def add_fullscreen_control(self, position="topright", **kwargs):
        """Add a fullscreen control to the map.

        Args:
            kwargs: Keyword arguments to pass to the ipyleaflet.FullScreenControl constructor.
        """  
        fullscreen_control = ipyleaflet.FullScreenControl(position=position, **kwargs)
        self.add_control(fullscreen_control)

    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Add a tile layer to the map.

        Args:
            url (str): The url of the tile layer.
            name (str): The name of the tile layer.
            attribution (str): The attribution of the tile layer.
            kwargs: Keyword arguments to pass to the ipyleaflet.TileLayer constructor.
        """  
        tile_layer = ipyleaflet.TileLayer(url=url, name=name, attribution=attribution, **kwargs)
        self.add_layer(tile_layer)


    def add_basemap(self, basemap, **kwargs):
        import xyzservices.providers as xyz
        """Add a basemap to the map.

        Args:
            basemap (str): The name of the basemap.
            kwargs: Keyword arguments to pass to the ipyleaflet.basemap constructor.
        """  

        if basemap.lower() == "roadmap":
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "satellite":
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'            
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "terrain":
            url = 'http://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "hybrid":
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attriution = attribution)
            except:
                raise ValueError(f"Basemap '{basemap}' is not supported. Please choose one of the following: roadmap, satellite, terrain, hybrid or provide a valid url.")
    

    def add_geojson(self, data, name='GeoJSON', **kwargs):
        """Add a geojson to the map.

        Args:
            data (dict): The geojson data.
            kwargs: Keyword arguments to pass to the ipyleaflet.GeoJSON constructor.
        """  
        if isinstance(data, str):
            import json
            with open(data, "r") as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add_layer(geojson)

    def add_shp(self, data, name='Shapefile', **kwargs):
        """Add a shapefile to the map.

        Args:
            data (str): The url of the shapefile.
            kwargs: Keyword arguments to pass to the ipyleaflet.GeoData constructor.
        """  
        import geopandas as gpd
        gdf = gpd.read_file(data)
        # geojson = gdf.to_json() : this convert to a string but needs to be converted to a dictionary
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)


    def add_shp(self, url, name='Shapefile', **kwargs):
        """Add a shapefile to the map.

        Args:
            data (str): The url of the shapefile.
            kwargs: Keyword arguments to pass to the ipyleaflet.GeoData constructor.
        """  
        import geopandas as gpd
        gdf = gpd.read_file(url)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)


    def read_geojson_from_url(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            gdf = gpd.read_file(response.content)
            return gdf
        except (ValueError, requests.exceptions.RequestException) as e:
            print("Error:", e)
        return None
    

    def add_vector(self, vector_data, name='Vector', **kwargs):
        """Add a vector data to the map.

        Args:
            vector_data (tuple): A tuple of two 1D arrays representing the x and y coordinates of the vector data.
            kwargs: Keyword arguments to pass to the ipyleaflet.GeoData constructor.
        """  
        import geopandas as gpd
        gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(vector_data[0], vector_data[1]))
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)


    def add_raster(self, url, name ='Raster', fit_bounds = True, **kwargs):
        """Add a raster data to the map.

        Args:
            url (str): The url of the raster data.
            name (str): The name of the raster data.
            fit_bounds (bool, optional): Whether to fit the map to the extent of the raster data.
            kwargs: Keyword arguments to pass to the ipyleaflet.ImageOverlay constructor.
        """  
        import httpx
        titiler_endpoint = "https://titiler.xyz"

            # Get bounds(bounding box)
        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }
        ).json()

        bounds = r["bounds"]

            # Get th tile url
        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
                "url": url,
            }
        ).json()

            # Get the tile = the url of the raster data
        tile = r['tiles'][0]

            # Add the tile to the map
        self.add_tile_layer(url=tile, name=name, **kwargs)

            # Decision to fit the map to the bounds
        if fit_bounds:
            bbx = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbx)


    def add_widget(self, content, position="bottomright", **kwargs):
        """Add a widget (e.g., text, HTML, figure) to the map.

        Args:
            content (str | ipywidgets.Widget | object): The widget to add.
            position (str, optional): The position of the widget. Defaults to "bottomright".
            **kwargs: Other keyword arguments for ipywidgets.HTML().
        """

        allowed_positions = ["topleft", "topright", "bottomleft", "bottomright"]

        if position not in allowed_positions:
            raise Exception(f"position must be one of {allowed_positions}")

        if "layout" not in kwargs:
            kwargs["layout"] = widgets.Layout(padding="0px 4px 0px 4px")
        try:
            if isinstance(content, str):
                widget = widgets.HTML(value=content, **kwargs)
                control = ipyleaflet.WidgetControl(widget=widget, position=position)
            else:
                output = widgets.Output(**kwargs)
                with output:
                    display(content)
                control = ipyleaflet.WidgetControl(widget=output, position=position)
            self.add(control)

        except Exception as e:
            raise Exception(f"Error adding widget: {e}")


    def add_image(self, image, position="bottomright", **kwargs):
        """Add an image to the map.

        Args:
            image (str | ipywidgets.Image): The image to add.
            position (str, optional): The position of the image, can be one of "topleft",
                "topright", "bottomleft", "bottomright". Defaults to "bottomright".

        """

        if isinstance(image, str):
            if image.startswith("http"):
                image = widgets.Image(value=requests.get(image).content, **kwargs)
            elif os.path.exists(image):
                with open(image, "rb") as f:
                    image = widgets.Image(value=f.read(), **kwargs)
        elif isinstance(image, widgets.Image):
            pass
        else:
            raise Exception("Invalid image")

        self.add_widget(image, position=position)

    def add_html(self, html, position="bottomright", **kwargs):
        """Add HTML to the map.

        Args:
            html (str): The HTML to add.
            position (str, optional): The position of the HTML, can be one of "topleft",
                "topright", "bottomleft", "bottomright". Defaults to "bottomright".
        """
        self.add_widget(html, position=position, **kwargs)


    def change_basemap(self, change, **kwargs):
        if change['new']:
            self.add(basemap.value)


    def csv_to_shp(self, in_csv, out_shp, x="longitude", y="latitude"):
        """_Convert a CSV file to a shapefile

        Args:
            in_csv (_csv_): _csv_
            out_shp (_shp_): _vector data_
            x (str, optional): _str_. Defaults to "longitude".
            y (str, optional): _str_. Defaults to "latitude".
        """        

        # Read the CSV file using pandas
        df = pd.read_csv(in_csv)
        
        # Create a GeoDataFrame from the DataFrame
        geometry = gpd.points_from_xy(df[x], df[y])
        gdf = gpd.GeoDataFrame(df, geometry=geometry)
        
        # Save the GeoDataFrame as a Shapefile
        gdf.to_file(out_shp, driver='ESRI Shapefile')

    def csv_to_geojson(in_csv, out_geojson, x="longitude", y="latitude"):
        """_Convert a CSV file to a GeoJSON file_

        Args:
            in_csv (_csv_): _csv_
            out_geojson (_GeoJSON_): _vector data_
            x (str, optional): _str_. Defaults to "longitude".
            y (str, optional): _str_. Defaults to "latitude".
        """        

        # Read the CSV file using pandas
        df = pd.read_csv(in_csv)
        
        # Create a GeoDataFrame from the DataFrame
        geometry = gpd.points_from_xy(df[x], df[y])
        gdf = gpd.GeoDataFrame(df, geometry=geometry)
        
        # Save the GeoDataFrame as a GeoJSON file
        gdf.to_file(out_geojson, driver='GeoJSON')


    def add_xy_data(
            self,
            in_csv,
            x="longitude",
            y="latitude",
            label=None,
            layer_name="Marker cluster",
        ):
            """Adds points from a CSV file containing lat/lon information and display data on the map.

            Args:
                in_csv (str): The file path to the input CSV file.
                x (str, optional): The name of the column containing longitude coordinates. Defaults to "longitude".
                y (str, optional): The name of the column containing latitude coordinates. Defaults to "latitude".
                label (str, optional): The name of the column containing label information to used for marker popup. Defaults to None.
                layer_name (str, optional): The layer name to use. Defaults to "Marker cluster".

            Raises:
                FileNotFoundError: The specified input csv does not exist.
                ValueError: The specified x column does not exist.
                ValueError: The specified y column does not exist.
                ValueError: The specified label column does not exist.
            """
            import pandas as pd

            if isinstance(in_csv, pd.DataFrame):
                df = in_csv
            elif not in_csv.startswith("http") and (not os.path.exists(in_csv)):
                raise FileNotFoundError("The specified input csv does not exist.")
            else:
                df = pd.read_csv(in_csv)

            col_names = df.columns.values.tolist()

            if x not in col_names:
                raise ValueError(f"x must be one of the following: {', '.join(col_names)}")

            if y not in col_names:
                raise ValueError(f"y must be one of the following: {', '.join(col_names)}")

            if label is not None and (label not in col_names):
                raise ValueError(
                    f"label must be one of the following: {', '.join(col_names)}"
                )

            self.default_style = {"cursor": "wait"}

            points = list(zip(df[y], df[x]))

            if label is not None:
                labels = df[label]
                markers = [
                    ipyleaflet.Marker(
                        location=point,
                        draggable=False,
                        popup=widgets.HTML(str(labels[index])),
                    )
                    for index, point in enumerate(points)
                ]
            else:
                markers = [
                    ipyleaflet.Marker(location=point, draggable=False) for point in points
                ]

            marker_cluster = ipyleaflet.MarkerCluster(markers=markers, name=layer_name)
            self.add(marker_cluster)

            self.default_style = {"cursor": "default"}

            def add_point_layer(
                self, filename, popup=None, layer_name="Marker Cluster", **kwargs
            ):
                """Adds a point layer to the map with a popup attribute.

                Args:
                    filename (str): str, http url, path object or file-like object. Either the absolute or relative path to the file or URL to be opened, or any object with a read() method (such as an open file or StringIO)
                    popup (str | list, optional): Column name(s) to be used for popup. Defaults to None.
                    layer_name (str, optional): A layer name to use. Defaults to "Marker Cluster".

                Raises:
                    ValueError: If the specified column name does not exist.
                    ValueError: If the specified column names do not exist.
                """
                import warnings

                warnings.filterwarnings("ignore")
                check_package(name="geopandas", URL="https://geopandas.org")
                import geopandas as gpd
                import fiona

                self.default_style = {"cursor": "wait"}

                if isinstance(filename, gpd.GeoDataFrame):
                    gdf = filename
                else:
                    if not filename.startswith("http"):
                        filename = os.path.abspath(filename)
                    ext = os.path.splitext(filename)[1].lower()
                    if ext == ".kml":
                        fiona.drvsupport.supported_drivers["KML"] = "rw"
                        gdf = gpd.read_file(filename, driver="KML", **kwargs)
                    else:
                        gdf = gpd.read_file(filename, **kwargs)
                df = gdf.to_crs(epsg="4326")
                col_names = df.columns.values.tolist()
                if popup is not None:
                    if isinstance(popup, str) and (popup not in col_names):
                        raise ValueError(
                            f"popup must be one of the following: {', '.join(col_names)}"
                        )
                    elif isinstance(popup, list) and (
                        not all(item in col_names for item in popup)
                    ):
                        raise ValueError(
                            f"All popup items must be select from: {', '.join(col_names)}"
                        )

                df["x"] = df.geometry.x
                df["y"] = df.geometry.y

                points = list(zip(df["y"], df["x"]))

                if popup is not None:
                    if isinstance(popup, str):
                        labels = df[popup]
                        markers = [
                            ipyleaflet.Marker(
                                location=point,
                                draggable=False,
                                popup=widgets.HTML(str(labels[index])),
                            )
                            for index, point in enumerate(points)
                        ]
                    elif isinstance(popup, list):
                        labels = []
                        for i in range(len(points)):
                            label = ""
                            for item in popup:
                                label = label + str(item) + ": " + str(df[item][i]) + "<br>"
                            labels.append(label)
                        df["popup"] = labels

                        markers = [
                            ipyleaflet.Marker(
                                location=point,
                                draggable=False,
                                popup=widgets.HTML(labels[index]),
                            )
                            for index, point in enumerate(points)
                        ]

                else:
                    markers = [
                        ipyleaflet.Marker(location=point, draggable=False) for point in points
                    ]

                marker_cluster = ipyleaflet.MarkerCluster(markers=markers, name=layer_name)
                self.add(marker_cluster)

                self.default_style = {"cursor": "default"}



    # def change_basemap(m):
    #     """Widget for changing basemaps.

    #     Args:
    #         m (object): rastvectpy.Map.
    #     """
    #     from box import Box
    #     basemaps = Box(xyz_to_leaflet(), frozen_box=True)
    #     from .rastvectpy import basemaps
    #     from .basemaps import get_xyz_dict

    #     xyz_dict = get_xyz_dict()

    #     layers = list(m.layers)
    #     if len(layers) == 1:
    #         layers = [layers[0]] + [basemaps["OpenStreetMap"]]
    #     elif len(layers) > 1 and (layers[1].name != "OpenStreetMap"):
    #         layers = [layers[0]] + [basemaps["OpenStreetMap"]] + layers[1:]
    #     m.layers = layers

    #     value = "OpenStreetMap"

    #     dropdown = widgets.Dropdown(
    #         options=list(basemaps.keys()),
    #         value=value,
    #         layout=widgets.Layout(width="200px"),
    #     )

    #     close_btn = widgets.Button(
    #         icon="times",
    #         tooltip="Close the basemap widget",
    #         button_style="primary",
    #         layout=widgets.Layout(width="32px"),
    #     )

    #     basemap_widget = widgets.HBox([dropdown, close_btn])


    # def split_basemaps(
    #     m, layers_dict=None, left_name=None, right_name=None, width="120px", **kwargs
    # ):
    #     """Create a split-panel map for visualizing two maps.

    #     Args:
    #         m (ipyleaflet.Map): An ipyleaflet map object.
    #         layers_dict (dict, optional): A dictionary of TileLayers. Defaults to None.
    #         left_name (str, optional): The default value of the left dropdown list. Defaults to None.
    #         right_name (str, optional): The default value of the right dropdown list. Defaults to None.
    #         width (str, optional): The width of the dropdown list. Defaults to "120px".
    #     """
    #     from .rastvectpy import basemaps

    #     controls = m.controls
    #     layers = m.layers
    #     # m.layers = [m.layers[0]]
    #     m.clear_controls()

    #     add_zoom = True
    #     add_fullscreen = True

    #     if layers_dict is None:
    #         layers_dict = {}
    #         keys = dict(basemaps).keys()
    #         for key in keys:
    #             if isinstance(basemaps[key], ipyleaflet.WMSLayer):
    #                 pass
    #             else:
    #                 layers_dict[key] = basemaps[key]

    #     keys = list(layers_dict.keys())
    #     if left_name is None:
    #         left_name = keys[0]
    #     if right_name is None:
    #         right_name = keys[-1]

    #     left_layer = layers_dict[left_name]
    #     right_layer = layers_dict[right_name]

    #     control = ipyleaflet.SplitMapControl(left_layer=left_layer, right_layer=right_layer)
    #     m.add(control)

    #     left_dropdown = widgets.Dropdown(
    #         options=keys, value=left_name, layout=widgets.Layout(width=width)
    #     )

    #     left_control = ipyleaflet.WidgetControl(widget=left_dropdown, position="topleft")
    #     m.add(left_control)

    #     right_dropdown = widgets.Dropdown(
    #         options=keys, value=right_name, layout=widgets.Layout(width=width)
    #     )

    #     right_control = ipyleaflet.WidgetControl(widget=right_dropdown, position="topright")
    #     m.add(right_control)

    #     close_button = widgets.ToggleButton(
    #         value=False,
    #         tooltip="Close the tool",
    #         icon="times",
    #         # button_style="primary",
    #         layout=widgets.Layout(height="28px", width="28px", padding="0px 0px 0px 4px"),
    #     )


    def add_text(
        self,
        text,
        fontsize=20,
        fontcolor="black",
        bold=False,
        padding="5px",
        background=True,
        bg_color="white",
        border_radius="5px",
        position="bottomright",
        **kwargs,
    ):
        """Add text to the map.

        Args:
            text (str): The text to add.
            fontsize (int, optional): The font size. Defaults to 20.
            fontcolor (str, optional): The font color. Defaults to "black".
            bold (bool, optional): Whether to use bold font. Defaults to False.
            padding (str, optional): The padding. Defaults to "5px".
            background (bool, optional): Whether to use background. Defaults to True.
            bg_color (str, optional): The background color. Defaults to "white".
            border_radius (str, optional): The border radius. Defaults to "5px".
            position (str, optional): The position of the widget. Defaults to "bottomright".
        """

        if background:
            text = f"""<div style="font-size: {fontsize}px; color: {fontcolor}; font-weight: {'bold' if bold else 'normal'}; 
            padding: {padding}; background-color: {bg_color}; 
            border-radius: {border_radius};">{text}</div>"""
        else:
            text = f"""<div style="font-size: {fontsize}px; color: {fontcolor}; font-weight: {'bold' if bold else 'normal'}; 
            padding: {padding};">{text}</div>"""

        self.add_html(text, position=position, **kwargs)



# def to_streamlit(self, width=None, height=600, scrolling=False, **kwargs):
#     """Renders map figure in a Streamlit app.

#     Args:
#         width (int, optional): Width of the map. Defaults to None.
#         height (int, optional): Height of the map. Defaults to 600.
#         responsive (bool, optional): Whether to make the map responsive. Defaults to True.
#         scrolling (bool, optional): If True, show a scrollbar when the content is larger than the iframe. Otherwise, do not show a scrollbar. Defaults to False.

#     Returns:
#         streamlit.components: components.html object.
#     """

#     try:
#         import streamlit.components.v1 as components

#         # if responsive:
#         #     make_map_responsive = """
#         #     <style>
#         #     [title~="st.iframe"] { width: 100%}
#         #     </style>
#         #     """
#         #     st.markdown(make_map_responsive, unsafe_allow_html=True)
#         return components.html(
#             self.to_html(), width=width, height=height, scrolling=scrolling
#         )

#     except Exception as e:
#         raise Exception(e)
    
    
    def visualize_raster(raster_data):    
        """
        Visualize a raster data using matplotlib.

        Parameters:
        raster_data (numpy.ndarray): A 2D array of raster data.

        Returns:
        None
        """
        # Create a figure and axis object
        fig, ax = plt.subplots()
        # Set the aspect ratio
        ax.set_aspect('equal')
        # Show the raster data as an image
        ax.imshow(raster_data, cmap='gray')
        # Set the x and y axis labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        # Show the plot
        plt.show()


    def visualize_vector(vector_data):
        """
        Visualize a vector data using matplotlib.

        Parameters:
        vector_data (tuple): A tuple of two 1D arrays representing the x and y coordinates of the vector data.

        Returns:
        None
        """
        # Create a figure and axis object
        fig, ax = plt.subplots()
        # Plot the vector data
        ax.quiver(vector_data[0], vector_data[1], color='blue', scale=1, units='xy', width=0.005, headwidth=5, headlength=7)
        # Set the x and y axis limits
        ax.set_xlim([min(vector_data[0])-1, max(vector_data[0])+1])
        ax.set_ylim([min(vector_data[1])-1, max(vector_data[1])+1])
        # Set the x and y axis labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        # Show plot
        plt.show()
