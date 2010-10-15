from openalea.image import read_inrimage,write_inrimage

try:
    img = read_inrimage("SAM.inr.gz")
except:
    img = read_inrimage("test/SAM.inr.gz")

write_inrimage("toto.inr.gz",img)

