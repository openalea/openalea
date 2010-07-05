from os import getcwd
from openalea.deploy import generate_autosum

f = open("autosum.rst",'w')
f.write(generate_autosum("openalea.celltissue") )
f.close()

