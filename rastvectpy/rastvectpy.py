"""Main module."""


def import_data(raster_path, vector_path):
    from osgeo import gdal, ogr
    # Open the raster file
    raster = gdal.Open(raster_path)
    if raster is None:
        print(f"Could not open {raster_path}")
        return None
    
    # Open the vector file
    vector = ogr.Open(vector_path)
    if vector is None:
        print(f"Could not open {vector_path}")
        return None
    
    # Print some information about the raster and vector data
    print("Raster Information:")
    print(f"Driver: {raster.GetDriver().ShortName}")
    print(f"Size: {raster.RasterXSize} x {raster.RasterYSize}")
    print(f"Projection: {raster.GetProjection()}")
    print(f"Number of Bands: {raster.RasterCount}")
    
    print("\nVector Information:")
    layer = vector.GetLayer()
    print(f"Driver: {vector.GetDriver().ShortName}")
    print(f"Number of Features: {layer.GetFeatureCount()}")
    print(f"Geometry Type: {layer.GetGeomType()}")
    
    # Return the raster and vector data as a tuple
    return (raster, vector)

# raster_path = "/path/to/raster.tif"
# vector_path = "/path/to/vector.shp"
# data = import_data(raster_path, vector_path)


import numpy as np
import matplotlib.pyplot as plt

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