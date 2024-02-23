def parse_band_ranges(filename, energy_window):
    # List to store (min_energy, max_energy) tuples of each band
    band_ranges = []
    
    with open(filename, 'r') as file:
        for line in file:
            min_energy, max_energy = map(float, line.split())
            
            # Check if the band is within the specified energy window
            if min_energy <= energy_window[1] and max_energy >= energy_window[0]:
                band_ranges.append((min_energy, max_energy))
                
    # Sort the band ranges by their minimum energy
    band_ranges.sort(key=lambda x: x[0])
    
    # Separate the four lowest and four highest bands
    lowest_bands = band_ranges[:4]
    highest_bands = band_ranges[-4:]
    
    # Check if there are enough bands within the window
    if not band_ranges:
        print("No bands found within the specified energy window.")
    else:
        print(f"Number of bands within the energy window: {len(band_ranges)}")
        print(f"Energy window: {energy_window}")
        
        # Report for the lowest bands
        for i, (min_energy, max_energy) in enumerate(lowest_bands, start=1):
            print(f"Lowest band {i}: Min energy = {min_energy:.5f} Hartrees, Max energy = {max_energy:.5f} Hartrees")
        
        # Report for the highest bands
        for i, (min_energy, max_energy) in enumerate(highest_bands, start=1):
            print(f"Highest band {i}: Min energy = {min_energy:.5f} Hartrees, Max energy = {max_energy:.5f} Hartrees")

E_F = 0.726119  # Fermi energy in Hartrees
# Specify the energy window (in Hartrees) you're interested in
energy_window = (0.58681, 0.76670)  # Adjust your energy window as needed

# Path to the wannier.mlwfBandRanges file
filename = 'wannier.mlwfBandRanges'

parse_band_ranges(filename, energy_window)
