#Save the following to WannierDOS.py:
import numpy as np

#Read the MLWF cell map, weights and Hamiltonian:    
cellMap = np.loadtxt("wannier.mlwfCellMap")[:,0:3].astype(int)
Wwannier = np.fromfile("wannier.mlwfCellWeights")
nCells = cellMap.shape[0]
nBands = int(np.sqrt(Wwannier.shape[0] / nCells))
Wwannier = Wwannier.reshape((nCells,nBands,nBands)).swapaxes(1,2)
#--- Get k-point folding from totalE.out:
for line in open('totalE.out'):
    if line.startswith('kpoint-folding'):
        kfold = np.array([int(tok) for tok in line.split()[1:4]])
kfoldProd = np.prod(kfold)
kStride = np.array([kfold[1]*kfold[2], kfold[2], 1])
#--- Read reduced Wannier Hamiltonian and expand it:
Hreduced = np.fromfile("wannier.mlwfH").reshape((kfoldProd,nBands,nBands)).swapaxes(1,2)
iReduced = np.dot(np.mod(cellMap, kfold[None,:]), kStride)
Hwannier = Wwannier * Hreduced[iReduced]

#Calculate DOS by Monte-Carlo sampling:
nBlocks = 100  #number of blocks
nK = 1000      #number of k per block
EkAll = np.zeros((nBlocks,nK,nBands))
for iBlock in range(nBlocks):
    kpoints = np.random.rand(nK,3)          #Generate random k
    Hk = np.tensordot(np.exp((2j*np.pi)*np.dot(kpoints,cellMap.T)), Hwannier, axes=1)
    Ek,Vk = np.linalg.eigh(Hk)              #Diagonalize
    EkAll[iBlock] = Ek                      #Save energies
    print("Block", iBlock+1, "of", nBlocks) #Report progress
#--- Histogram:
nBins = 400
hist,binEdges = np.histogram(EkAll, nBins, density=True)
hist *= (2*nBands)  #Integral should be 2 nBands but np.histogram normalizes to 1
bins = 0.5*(binEdges[1:]+binEdges[:-1])  #bin centers
#--- Save:
outData = np.vstack((bins,hist)).T #Put together in columns
np.savetxt("wannier.dos", outData)