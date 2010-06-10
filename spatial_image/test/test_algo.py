from openalea.spatial_image import (read_inrimage,write_inrimage,
                                    view_right,view_face)

img = read_inrimage("SAM.inr.gz")

write_inrimage(view_right(img),"right.inr.gz")
write_inrimage(view_face(img),"face.inr.gz")


