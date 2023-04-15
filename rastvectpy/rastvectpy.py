"""Main module."""

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