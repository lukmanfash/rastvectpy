"""Main module."""

import numpy as np
import matplotlib.pyplot as plt
import ipyleaflet

class Map(ipyleaflet.Map):

    def __init__(self, center, zoom, **kwargs):

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True
        # print(kwargs)
        super().__init__(center = center, zoom = zoom, **kwargs)

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