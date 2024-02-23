# Define temperatures from 20 K to 300 K, incremented by 20 K
temperatures_K = list(range(20, 301, 20))  # Generates [20, 40, 60, ..., 300]

# Simplified conversion to smearing factors in Hartrees (for demonstration)
# Replace this with your precise conversion if necessary
smearing_factors_Ha = [temp / 315774.64 for temp in temperatures_K]

template = """include common.in
kpoint-folding 8 8 8
elec-n-bands 100
elec-smearing Fermi {smearing}
converge-empty-states yes
electronic-scf
dump-name totalE/totalE-{temp}K.$VAR
dump End State BandEigs ElecDensity Symmetries Kpoints
density-of-states Total
dump End EigStats
"""

for temp, smearing in zip(temperatures_K, smearing_factors_Ha):
    filename = f"totalE-{temp}K.in"
    with open(filename, 'w') as file:
        # Format smearing factor and temperature with precision
        file_content = template.format(smearing=f'{smearing:.8f}', temp=temp)
        file.write(file_content)
    print(f"Generated file: {filename}")
