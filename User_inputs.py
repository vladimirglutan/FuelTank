#USE THIS!
#user inputs
import numpy as np
from numpy import sqrt

# Function to calculate the height at which a target percentage of the area is reached
def find_height_for_target_percentage(R, dy, target_percent):
    # Initialize variables
    y = -R  # Starting point at the bottom of the cylinder
    A = 0  # This will be the aggregate area from -R upwards
    A_total = np.pi * (R ** 2)  # Total area of the circle (cross-section of the cylinder)

    # Calculate the target area based on the target percentage
    target_area = (target_percent / 100) * A_total

    # Iterate until the target percentage of the total area is reached
    while A < target_area:
        A += 2 * sqrt(R ** 2 - y ** 2) * dy  # Add the area of each small strip
        y += dy  # Move to the next height increment

    pdiam = (y + R)/(2*R)

    # Print the results
    print('Aggregate Area =', A)
    print('Target Percentage of Total Area =', (A / A_total) * 100, '%')
    print('Height at', target_percent, '% of the total area =', y)
    print('Percent of Diameter at', target_percent, '% of the total area =', pdiam * 100)

# Input values
R = float(input("Enter the radius (R): "))
dy = float(input("Enter the step size (dy): "))
target_percent = float(input("Enter the target percentage full: "))

# Call the function with the input values
find_height_for_target_percentage(R, dy, target_percent)
