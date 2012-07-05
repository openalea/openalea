#################################################################
# ImageJ

import numpy as np
from jpype import *
jarpath='/usr/share/java/ij.jar'
startJVM(getDefaultJVMPath(), "-Djava.class.path=%s" % jarpath)

ij = JPackage('ij')
im = ij.IJ.openImage("http://rsb.info.nih.gov/ij/images/lena.jpg")
#ij.IJ.save(im, '/tmp/tmp.png')

# View image
im.show()

# Convert
ip = im.getProcessor()

def ip2array(ip): 
    return np.array(ip.getIntArray(), dtype=np.uint8).transpose()

my_img = ip2array(ip)
imshow(my_img)

#shutdownJVM()
