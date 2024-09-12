import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from ipywidgets import interact, FloatSlider

# Function to calculate area, percent diameter, and percent area
def calculate_area(R, dipstick_height, dy):
    # Calculate the total area of the full circular cross-section
    total_area = np.pi * R**2
    
    # Calculate the area of the segment up to the dipstick height using geometry
    h = R - dipstick_height  # Height from the dipstick height to the circle's top edge
    if h > R or h < -R:
        segment_area = 0  # Out of bounds for the dipstick height
    else:
        theta = 2 * np.arccos(h / R)  # Central angle in radians
        segment_area = 0.5 * R**2 * (theta - np.sin(theta))  # Area of the segment
    
    # Percent diameter calculation
    percent_diameter = (dipstick_height / (2 * R)) * 100
    
    # Percent area calculation
    percent_area = (segment_area / total_area) * 100
    
    return segment_area, percent_diameter, percent_area

# Function to plot a horizontal 3D cylinder with a vertical dipstick plane moving from south to north
def plot_cylinder_with_dipstick(dipstick_height, elev, azim, R):
    # Set fixed length for the cylinder
    L = 6  # Updated length to 6 cm
    dy = 0.001  # Step size for area calculation

    # Calculate the area and percent diameter at the current dipstick height
    A, percent_diameter, percent_area = calculate_area(R, dipstick_height, dy)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Cylinder parameters
    theta = np.linspace(0, 2 * np.pi, 50)
    z = np.linspace(0, L, 50)  # Updated to reflect only positive length
    theta_grid, z_grid = np.meshgrid(theta, z)

    # Cylinder coordinates
    X = R * np.cos(theta_grid)
    Y = z_grid
    Z = R * np.sin(theta_grid)

    # Plot the cylinder surface
    ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.6, edgecolor='k')

    # Dipstick plane coordinates
    dipstick_z = np.clip(dipstick_height - R, -R, R)  # Limit to cylinder bounds
    dipstick_x = np.sqrt(R**2 - dipstick_z**2)  # Calculate width of plane inside cylinder

    # Define the vertices of the dipstick plane moving from south to north
    plane_vertices = [
        [-dipstick_x, 0, dipstick_z],
        [dipstick_x, 0, dipstick_z],
        [dipstick_x, L, dipstick_z],
        [-dipstick_x, L, dipstick_z]
    ]

    # Create the dipstick plane
    dipstick_plane = Poly3DCollection([plane_vertices], color='red', alpha=0.5)
    ax.add_collection3d(dipstick_plane)

    # Set plot limits and labels
    ax.set_xlim(-R, R)  # Accurate radius display
    ax.set_ylim(0, L)   # Only positive values for length
    ax.set_zlim(-R, R)  # Accurate height display
    ax.set_xlabel('Cylinder Radius (cm)')
    ax.set_ylabel('Length (cm)')
    ax.set_zlabel('Dipstick Height (cm)')

    # Adjust the perspective using sliders for elevation and azimuth
    ax.view_init(elev=elev, azim=azim)

    # Display the calculated area and percent diameter on the plot
    plt.title(f'Dipstick Height: {dipstick_height:.2f} cm')
    # Display text on the right side of the plot for better visibility
    ax.text2D(0.75, 0.95, f'Area = {A:.2f} cm²\nPercent Diameter = {percent_diameter:.2f}%\nPercent Area = {percent_area:.2f}%', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    plt.show()

# Set up the interactive sliders
dipstick_slider = FloatSlider(value=0.0, min=0.0, max=2 * 5.5, step=0.01, description='Dipstick Height (cm)')
elev_slider = FloatSlider(value=20, min=0, max=90, step=1, description='Elevation')
azim_slider = FloatSlider(value=210, min=0, max=360, step=1, description='Azimuth')
radius_slider = FloatSlider(value=5.5, min=0.1, max=6, step=0.1, description='Radius (cm)')  # Updated default to 5.5 cm

# Use interact to create the sliders and plot the interactive cylinder
interact(plot_cylinder_with_dipstick, dipstick_height=dipstick_slider, elev=elev_slider, azim=azim_slider, R=radius_slider);
