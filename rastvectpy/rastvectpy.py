"""Main module."""

import numpy as np
import matplotlib.pyplot as plt
import ipyleaflet

class Map(ipyleaflet.Map):

    def __init__(self, center, zoom, **kwargs)-> None:

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True
        # print(kwargs)
        super().__init__(center = center, zoom = zoom, **kwargs)

        if "layer_control" not in kwargs:
            kwargs["layer_control"] = True

        if kwargs["layer_control"]:
            self.add_layer_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True

        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()
     
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

    def add_tile_layer(self, url, name, attribution, **kwargs):
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


# More to come