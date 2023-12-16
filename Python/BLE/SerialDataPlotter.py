import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
file_path = 'serial_data.csv'  # Update this with the correct path
data = pd.read_csv(file_path)

# Plotting
plt.figure(figsize=(10, 6))

# Plot each of the orientation axes
plt.plot(data['Timestamp'], data['Heading'], label='Heading')
plt.plot(data['Timestamp'], data['Pitch'], label='Pitch')
plt.plot(data['Timestamp'], data['Roll'], label='Roll')

# Adding titles and labels
plt.title('Orientation Data Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Degrees')
plt.legend()

# Show grid
plt.grid(True)

# Display the plot
plt.show()
