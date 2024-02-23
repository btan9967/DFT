import pandas as pd
import matplotlib.pyplot as plt

def parse_and_plot_aggregated_dos(filename):
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
            aggregated_dos[key] = df[column]
        else:
            aggregated_dos[key] += df[column]
    
    # Plotting
    plt.figure(figsize=(10, 6))
    for key, dos in aggregated_dos.items():
        element, orbital_type = key
        label = f"{element} {orbital_type}-orbital"
        plt.plot(df['Energy'], dos, label=label)
    
    plt.xlabel('Energy (Hartrees)')
    plt.ylabel('Aggregated DOS')
    plt.title('Aggregated Projected Density of States')
    plt.legend()
    plt.grid(True)
    plt.show()

# Specify the path to your pdos.dos file
filename = 'pdos.dos'
parse_and_plot_aggregated_dos(filename)
