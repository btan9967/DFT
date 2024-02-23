#!/usr/bin/gnuplot -persist
set xtics ( "Gamma" 0,  "M" 10,  "K" 18,  "Gamma" 28,  "A" 38,  "L" 48,  "H" 56,  "A" 66 )
unset key
nRows = real(system("awk '$1==\"kpoint\" {nRows++} END {print nRows}' bandstruct.kpoints"))
nCols = real(system("wc -c < bandstruct.eigenvals")) / (8*nRows)
formatString = system(sprintf("echo '' | awk 'END { str=\"\"; for(i=0; i<%d; i++) str = str \"%%\" \"lf\"; print str}'", nCols))
#Edit end of bandstruct.plot to the following:
VBM = +0.726119  #HOMO from totalE.eigStats
eV = 1/27.2114   #in Hartrees
xEnd = 68
set xzeroaxis
set yrange [(0.62257-VBM)/eV:(0.7667-VBM)/eV]
set ylabel "E - VBM [eV]"
plot for [i=1:nCols] "bandstruct.eigenvals" binary format=formatString u 0:((column(i)-VBM)/eV) every 2 w p lc rgb "black"
replot for [i=1:nCols] "wannier.eigenvals" u (0.1*$0):((column(i)-VBM)/eV) w l lt 1
replot \
	for [i=1:nCols] "bandstruct.eigenvals" binary format=formatString u 0:((column(i)-VBM)/eV) w l
	#"pdos.dos" u (xEnd+0.2*$4):(($1-VBM)/eV) w l lw 2 title "0", \
	#"pdos.dos" u (xEnd+0.2*$6):(($1-VBM)/eV) w l lw 2 title "1", \
	#"pdos.dos" u (xEnd+0.2*$9):(($1-VBM)/eV) w l lw 2 title "4", \
	#"pdos.dos" u (xEnd+0.2*$11):(($1-VBM)/eV) w l lw 2 title "5", \
	#"pdos.dos" u (xEnd+0.2*$12):(($1-VBM)/eV) w l lw 2 title "6", \
	#"pdos.dos" u (xEnd+0.2*$13):(($1-VBM)/eV) w l lw 2 title "7", \
	#"pdos.dos" u (xEnd+0.2*$9):(($1-VBM)/eV) w l lw 2 title "8", \
	#"pdos.dos" u (xEnd+0.2*$10):(($1-VBM)/eV) w l lw 2 title "9", \
	#"pdos.dos" u (xEnd+0.2*$11):(($1-VBM)/eV) w l lw 2 title "10", \
	#"pdos.dos" u (xEnd+0.2*$12):(($1-VBM)/eV) w l lw 2 title "11", 

#innerWindow 0.56467  0.6195396 \
#         outerWindow 0.56  0.64417 \

