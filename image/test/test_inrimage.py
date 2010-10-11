from openalea.image import read_inrimage,write_inrimage

img = read_inrimage("SAM.inr.gz")

write_inrimage("toto.inr.gz",img)

