import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def read_and_aggregate_dos(filename, energy_min, energy_max):
    # Load the data, with the first row containing headers
    df = pd.read_csv(filename, delim_whitespace=True, comment='#', header=0)
    
    # Filter rows by the energy window
    df_filtered = df[(df['Energy'] >= energy_min) & (df['Energy'] <= energy_max)]
    
    # Initialize a dictionary to hold aggregated DOS data for each specific orbital of each atom
    aggregated_dos = {}
    
    # Process each column (orbital) in the DataFrame
    for column in df_filtered.columns:
        if column == 'Energy':
            continue  # Skip the 'Energy' column
            
        # The key now includes both orbital type and atom number to distinguish between atoms
        key = column  # Use the full column name as the key to keep the distinction
        
        # Aggregate DOS data for each specific orbital of each atom
        aggregated_dos[key] = df_filtered[column].values

    return df_filtered['Energy'].values, aggregated_dos

def plot_pdos_on_separate_figures(energies, aggregated_dos, energy_window):
    for key, dos in aggregated_dos.items():
        plt.figure(figsize=(6, 4))  # Adjust the figure size as needed
        plt.plot(energies, dos, label=key)
        plt.axvline(x=energy_window[0], color='green', linestyle='--', label='Inner Window Start')  # Draw vertical line for the start of the inner window
        plt.axvline(x=energy_window[1], color='red', linestyle='--', label='Inner Window End')  # Draw vertical line for the end of the inner window
        plt.title(key)
        plt.xlabel('Energy (Hartrees)')
        plt.ylabel('Density of States')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

# Specify your energy window and inner window here (in Hartrees)
energy_min = 0.58079  # Outer window lower bound
energy_max = 0.78174  # Outer window upper bound

# Path to your PDOS file
pdos_file = 'pdos.dos'  # Adjust the path to your actual file

# Read and aggregate the PDOS data
energies, aggregated_dos = read_and_aggregate_dos(pdos_file, energy_min, energy_max)

# Define the inner window
energy_window = (0.58681, 0.7667)  # Adjust these values as needed based on your data

# Plot the PDOS with each orbital type separated and distinguished by atom on separate figures
plot_pdos_on_separate_figures(energies, aggregated_dos, energy_window)