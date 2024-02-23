#!/usr/bin/gnuplot -persist
set xtics ( "Gamma" 0,  "M" 10,  "K" 18,  "Gamma" 28,  "A" 38,  "L" 48,  "H" 56,  "A" 66 )
unset key
nRows = real(system("awk '$1==\"kpoint\" {nRows++} END {print nRows}' bandstruct.kpoints"))
nCols = real(system("wc -c < bandstruct.eigenvals")) / (8*nRows)
formatString = system(sprintf("echo '' | awk 'END { str=\"\"; for(i=0; i<%d; i++) str = str \"%%\" \"lf\"; print str}'", nCols))
#Edit end of bandstruct.plot to the following:
VBM = +0.725882  #HOMO from totalE.eigStats
eV = 1/27.2114   #in Hartrees
set xzeroaxis
set yrange [-0.2/eV:0.14298/eV]
set ylabel "E - VBM [eV]"
plot for [i=1:nCols] "bandstruct.eigenvals" binary format=formatString u 0:((column(i)-VBM)/eV) every 2 w p lc rgb "black"
replot for [i=1:4] "wannier.eigenvals" u (0.1*$0):((column(i)-VBM)/eV) w l lt 1
