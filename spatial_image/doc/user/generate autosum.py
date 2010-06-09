from os import getcwd
from openalea.misc.autosum_generator import generate_autosum

f = open("autosum.rst",'w')
f.write(generate_autosum(getcwd() ) )
f.close()

