#Save the following to PhononDispersion.py:
import numpy as np
from scipy.interpolate import interp1d

#Read the phonon cell map and force matrix:
cellMap = np.loadtxt("totalE.phononCellMap")[:,0:3].astype(int)
forceMatrix = np.fromfile("totalE.phononOmegaSq", dtype=np.float64)
nCells = cellMap.shape[0]
nModes = int(np.sqrt(forceMatrix.shape[0] / nCells))
forceMatrix = np.reshape(forceMatrix, (nCells,nModes,nModes))

#Read the k-point path:
kpointsIn = np.loadtxt('bandstruct.kpoints', skiprows=2, usecols=(1,2,3))
nKin = kpointsIn.shape[0]
#--- Interpolate to a 10x finer k-point path:
nInterp = 10
xIn = np.arange(nKin)
x = (1./nInterp)*np.arange(1+nInterp*(nKin-1)) #same range with 10x density
kpoints = interp1d(xIn, kpointsIn, axis=0)(x)
nK = kpoints.shape[0]

#Calculate dispersion from force matrix:
#--- Fourier transform from real to k space:
forceMatrixTilde = np.tensordot(np.exp((2j*np.pi)*np.dot(kpoints,cellMap.T)), forceMatrix, axes=1)
#--- Diagonalize:
omegaSq, normalModes = np.linalg.eigh(forceMatrixTilde)

#Plot phonon dispersion:
import matplotlib.pyplot as plt
meV = 1e-3/27.2114
plt.plot(np.sqrt(omegaSq)/meV)
plt.xlim([0,nK-1])
plt.ylim([0,None])
plt.ylabel("Phonon energy [meV]")
#--- If available, extract k-point labels from bandstruct.plot:
try:
    import subprocess as sp
    kpathLabels = sp.check_output(['awk', '/set xtics/ {print}', 'bandstruct.plot']).split()
    kpathLabelText = [ label.split('"')[1] for label in kpathLabels[3:-2:2] ]
    kpathLabelPos = [ nInterp*int(pos.split(',')[0]) for pos in kpathLabels[4:-1:2] ]
    plt.xticks(kpathLabelPos, kpathLabelText)
except:
    print ('Warning: could not extract labels from bandstruct.plot')
plt.show()