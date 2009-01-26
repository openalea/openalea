from openalea.plantgl.all import *
from nurbs import read_line
import loft

f=open("path.txt",'r')
lines=f.readlines()
f.close()

zfactor=1./0.22

sc=Scene()
trans=0
for ind,line in enumerate(lines) :
	if ind%2==0 :
		trans=int(line)*zfactor
	else :
		sc+=Translated((0,0,trans),read_line(line,"hull",0))

Viewer.display(sc)

distances = []
nurbs_crvs = []

for ind,line in enumerate(lines) :
	if ind%2==0 :
		distances.append(int(line)*zfactor)
	else :
		nurbs_crvs.append(read_line(line,"hull",0))

nurbs_surface = loft.loft(nurbs_crvs, distances)
sc += nurbs_surface

Viewer.display(sc)
