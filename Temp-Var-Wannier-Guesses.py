import numpy as np
import sys

# Set a fixed seed for reproducibility
np.random.seed(42)

relDecision = input('Is this spin orbit? [y/n]: ')
if relDecision not in ['y', 'Y', 'n', 'N']:
    print("Invalid command. Please try again")
    sys.exit(0)

nCenters = int(input('How many centers: '))
innerWindowLow = float(input('Lower inner window: '))
innerWindowHigh = float(input('Higher inner window: '))
outerWindowLow = float(input('Lower outer window: '))
outerWindowHigh = float(input('Higher outer window: '))
nIterations = int(input('How many iterations: '))
startTemp = int(input('Start temperature (K): '))
endTemp = int(input('End temperature (K): '))
tempIncrement = int(input('Temperature increment (K): '))

# Generate the same set of random centers for all temperatures
centers = (np.random.rand(nCenters, 3) - 0.5) / 1  # Assuming x = 1 for simplicity

for temp in range(startTemp, endTemp + 1, tempIncrement):
    filename = f'wannier-{temp}.in'
    with open(filename, 'w') as wan:
        # Reference the corresponding totalE-${temp}K.in file
        wan.write(f"include totalE-{temp}K.in \n\n")
        wan.write("wannier \ \n")
        wan.write(f"\t innerWindow {innerWindowLow} {innerWindowHigh}\n")
        wan.write(f"\t outerWindow {outerWindowLow} {outerWindowHigh}\n")
        wan.write("\t saveMomenta yes \n\n")
        wan.write(f"#input file generated from script for {temp}K \n")
        wan.write(f"# {nCenters} centers included \n\n")

        if relDecision in ['y', 'Y']:
            unrelCenters = nCenters // 2
            for i in range(unrelCenters):
                for spin in ["sUp", "sDn"]:
                    wan.write("wannier-center Gaussian")
                    wan.write(f" {centers[i][0]:.9f} {centers[i][1]:.9f} {centers[i][2]:.9f} 1 {spin}\n")
        elif relDecision in ['n', 'N']:
            for i in range(nCenters):
                wan.write("wannier-center Gaussian")
                wan.write(f" {centers[i][0]:.9f} {centers[i][1]:.9f} {centers[i][2]:.9f}\n")

        wan.write("\n\nwannier-initial-state ../totalE/totalE.$VAR\n")
        wan.write(f"wannier-dump-name ../wannier/wannier-{temp}K.$VAR\n")  # Ensure unique dump names
        wan.write(f"wannier-minimize nIterations {nIterations}\n")

    print(f"Generated file: {filename}")
