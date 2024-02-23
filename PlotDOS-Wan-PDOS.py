import matplotlib.pyplot as plt
import pandas as pd

def read_and_filter_dos(filename, energy_min, energy_max):
    energies, dos = [], []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) < 2:
                continue  # Skip lines that don't have enough data
            energy, dos_value = float(parts[0]), float(parts[1])
            if energy_min <= energy <= energy_max:
                energies.append(energy)
                dos.append(dos_value)
    return energies, dos

def plot_dos(wannier_file, totalE_file, energy_min, energy_max, inner_lower, inner_upper):
    # Read and filter data
    wannier_energies, wannier_dos = read_and_filter_dos(wannier_file, energy_min, energy_max)
    totalE_energies, totalE_dos = read_and_filter_dos(totalE_file, energy_min, energy_max)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(wannier_energies, wannier_dos, label='Wannier DOS', color='blue')
    plt.plot(totalE_energies, totalE_dos, label='Total Energy DOS', color='red')
    
    # Draw vertical lines for the inner window
    plt.axvline(x=inner_lower, color='green', linestyle='--', label='Inner Lower Window')
    plt.axvline(x=inner_upper, color='purple', linestyle='--', label='Inner Upper Window')
    
    plt.xlabel('Energy (Hartrees)')
    plt.ylabel('Density of States')
    plt.title('DOS Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()


def read_and_aggregate_dos(filename, energy_min, energy_max):
    # Read the data, assuming tab-delimited and skipping the first row as header
    df = pd.read_csv(filename, delim_whitespace=True, skiprows=1, header=None)
    
    # Rename the first column to 'Energy' for clarity
    column_names = ['Energy']
    # Extract column headers from the file
    with open(filename, 'r') as file:
        header_line = file.readline().strip().split('\t')
        column_names.extend(header_line[1:])  # Skip the first entry ("Energy")
    
    # Set the new column names
    df.columns = column_names
    
    # Filter rows by the energy window
    df = df[(df['Energy'] >= energy_min) & (df['Energy'] <= energy_max)]
    
    # Dictionary to hold aggregated DOS data for each element and orbital type
    aggregated_dos = {}
    
    # Process columns to aggregate DOS by element and orbital type
    for column in df.columns[1:]:  # Skip the 'Energy' column
        # Extract element and orbital type
        parts = column.split()
        orbital_type = parts[0][1]  # Extracting the first letter as orbital type
        element = parts[-2]  # The second to last word is the element
        
        key = (element, orbital_type)
        if key not in aggregated_dos:
            aggregated_dos[key] = df[column].tolist()
        else:
            aggregated_dos[key] = [sum(x) for x in zip(aggregated_dos[key], df[column].tolist())]

    return df['Energy'].tolist(), aggregated_dos

# Function to plot DOS data, including aggregated pdos and vertical lines for the inner window
def plot_dos(wannier_file, totalE_file, pdos_file, energy_min, energy_max, inner_lower, inner_upper):
    # Read and filter data from wannier and totalE files
    wannier_energies, wannier_dos = read_and_filter_dos(wannier_file, energy_min, energy_max)
    totalE_energies, totalE_dos = read_and_filter_dos(totalE_file, energy_min, energy_max)
    
    # Read and aggregate pdos data
    pdos_energies, aggregated_dos = read_and_aggregate_dos(pdos_file, energy_min, energy_max)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(wannier_energies, wannier_dos, label='Wannier DOS', color='blue')
    plt.plot(totalE_energies, totalE_dos, label='Total Energy DOS', color='red')
    
    # Plot aggregated pdos
    for key, dos in aggregated_dos.items():
        plt.plot(pdos_energies, dos, label=key)
    
    # Draw vertical lines for the inner window
    plt.axvline(x=inner_lower, color='green', linestyle='--', label='Inner Lower Window')
    plt.axvline(x=inner_upper, color='purple', linestyle='--', label='Inner Upper Window')
    
    plt.xlabel('Energy (Hartrees)')
    plt.ylabel('Density of States')
    plt.title('DOS Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_dos_Ef(wannier_file, totalE_file, pdos_file, energy_min, energy_max, inner_lower, inner_upper, E_F):
    # Reading and filtering data from DOS files
    wannier_energies, wannier_dos = read_and_filter_dos(wannier_file, energy_min, energy_max)
    totalE_energies, totalE_dos = read_and_filter_dos(totalE_file, energy_min, energy_max)
    pdos_energies, aggregated_dos = read_and_aggregate_dos(pdos_file, energy_min, energy_max)
    
    # Plotting, with energies shifted by the Fermi energy
    plt.figure(figsize=(10, 6))
    plt.plot([e - E_F for e in wannier_energies], wannier_dos, label='Wannier DOS', color='blue')
    plt.plot([e - E_F for e in totalE_energies], totalE_dos, label='Total Energy DOS', color='red')
    
    for key, dos in aggregated_dos.items():
        plt.plot([e - E_F for e in pdos_energies], dos, label=f'{key}')

    # Drawing vertical lines for the inner window, adjusted by Fermi energy
    plt.axvline(x=inner_lower - E_F, color='green', linestyle='--', label='Inner Lower Window')
    plt.axvline(x=inner_upper - E_F, color='purple', linestyle='--', label='Inner Upper Window')
    
    plt.xlabel('Energy (Hartrees) relative to E_F')
    plt.ylabel('Density of States')
    plt.title('DOS Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_dos_eV(wannier_file, totalE_file, pdos_file, energy_min, energy_max, inner_lower, inner_upper, E_F):
    # Conversion factor from Hartrees to eV
    ha_to_ev = 27.2114
    
    # Adjusting the energy window and Fermi energy to eV
    energy_min_eV = energy_min * ha_to_ev
    energy_max_eV = energy_max * ha_to_ev
    inner_lower_eV = (inner_lower - E_F) * ha_to_ev
    inner_upper_eV = (inner_upper - E_F) * ha_to_ev
    E_F_eV = E_F * ha_to_ev
    
    # Read and filter data
    wannier_energies, wannier_dos = read_and_filter_dos(wannier_file, energy_min, energy_max)
    totalE_energies, totalE_dos = read_and_filter_dos(totalE_file, energy_min, energy_max)
    pdos_energies, aggregated_dos = read_and_aggregate_dos(pdos_file, energy_min, energy_max)
    
    # Plotting, converting energies to eV
    plt.figure(figsize=(10, 6))
    plt.plot([(e - E_F) * ha_to_ev for e in wannier_energies], wannier_dos, label='Wannier DOS', color='blue')
    plt.plot([(e - E_F) * ha_to_ev for e in totalE_energies], totalE_dos, label='Total Energy DOS', color='red')
    
    for key, dos in aggregated_dos.items():
        plt.plot([(e - E_F) * ha_to_ev for e in pdos_energies], dos, label=f'{key}')

    # Drawing vertical lines for the inner window, adjusted by Fermi energy and converted to eV
    plt.axvline(x=inner_lower_eV, color='green', linestyle='--', label='Inner Lower Window')
    plt.axvline(x=inner_upper_eV, color='purple', linestyle='--', label='Inner Upper Window')
    
    plt.xlabel('Energy (eV) relative to E_F')
    plt.ylabel('Density of States')
    plt.title('DOS Comparison in eV')
    plt.legend()
    plt.grid(True)
    plt.show()

# Specify the energy window, inner window, and Fermi energy (in Hartrees)
energy_min = 0.58079  # Outer window lower bound
energy_max = 0.78175  # Outer window upper bound
inner_lower = 0.58681  # Inner window lower bound
inner_upper = 0.7667  # Inner window upper bound
E_F = 0.725902  # Fermi energy in Hartrees

# Specify the paths to your DOS files
wannier_file = 'wannier.dos'
totalE_file = 'totalE.dos'
pdos_file = 'pdos.dos'  # Path to your pdos.dos file

plot_dos(wannier_file, totalE_file, pdos_file, energy_min, energy_max, inner_lower, inner_upper)
plot_dos_Ef(wannier_file, totalE_file, pdos_file, energy_min, energy_max, inner_lower, inner_upper, E_F)
# Example usage with the same parameters as before, but now expecting the plot to be in eV
plot_dos_eV(wannier_file, totalE_file, pdos_file, energy_min, energy_max, inner_lower, inner_upper, E_F)