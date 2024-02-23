# generates random guesses for your wannier input file.
import numpy as np
import sys

relDecision = input('is this spin orbit? [y/n]: ')
if relDecision!='n' and relDecision!='N' and relDecision!='y' and relDecision!='Y':
   print("invalid command. Please try again")
   sys.exit(0)
nCenters = int(input('How many centers: ' ))
innerWindowLow = float(input('Lower inner window: '))
innerWindowHigh = float(input('Higher inner window: '))
outerWindowLow = float(input('Lower outer window: '))
outerWindowHigh = float(input('Higher outer window: '))
nIterations = int(input('How many iterations: '))

wan = open('wannier.in', 'w')

wan.write("include totalE.in \n \n")
wan.write("wannier \ \n")
wan.write("\t innerWindow %s " % innerWindowLow)
wan.write(" %s " % innerWindowHigh)
wan.write("\ \n \t outerWindow %s " % outerWindowLow)
wan.write(" %s " % outerWindowHigh)
wan.write("\ \n \t saveMomenta yes \n\n")
wan.write("#input file generated from wanGen.py \n")
wan.write("# %s centers included \n\n" % nCenters)

# How close to the origin do you want your centers to be located:
x = 1  # divide by 1: range = [-0.5,0.5]. Divide by 2: range = [-0.25,0.25]

file = []

if relDecision=='y' or relDecision=='Y':
   unrelCenters=nCenters/2.
   for i in range(0,int(unrelCenters)):
      random =(np.random.rand(3)-0.5)/x
      for j in range(0,2):
         if j==0:
            spin = "sUp"
         else:
            spin = "sDn"
         wan.write("wannier-center Gaussian")
         wan.write(" %.9s " % random[0] )
         wan.write(" %.9s " % random[1])
         wan.write(" %.9s " % random[2])
         wan.write(" 1 %s" % spin)
         wan.write(" \n")

elif relDecision=='n' or relDecision=='N':
   for i in range(0,nCenters):
      random =(np.random.rand(3)-0.5)/x
      wan.write("wannier-center Gaussian")
      wan.write(" %.9s " % random[0] )
      wan.write(" %.9s " % random[1])
      wan.write(" %.9s " % random[2])
      wan.write(" \n")

wan.write("\n \nwannier-initial-state totalE.$VAR")
wan.write("\nwannier-dump-name wannier.$VAR")
wan.write("\nwannier-minimize nIterations %s" % nIterations)
wan.close()


# energy_window = (0.6839451000000001, 0.7462725) 