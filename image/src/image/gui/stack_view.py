# -*- python -*-
#
#       image.serial: read/write images
#
#       Copyright 2006 - 2011 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################

__license__= "Cecill-C"
__revision__=" $Id$ "


import OpenGL.GL as ogl
from openalea.pglviewer import ElmView,Vec
from openalea.pglviewer.constants import DRAW_MODE
from pixmap import to_tex

class StackView( ElmView) :
    """View a 3D image as a stack of slides
    """

    def __init__ (self, image, alpha_threshold = 0.1, slices = None) :
        """Constructor

        :Parameters:
         - `image` (NxMx3 or 4 array)
         - `alpha_threshold` (float) - threshold below which a pixel is not
                                       displayed
         - `slices` (list of int) - list of slices to display, if None, all
                                    slices in the stack will be displayed
        """
        ElmView.__init__(self,"stack")
        self.use_alpha(True)
        self.set_alpha_threshold(alpha_threshold)
        ogl.glTexParameteri(ogl.GL_TEXTURE_2D,
                            ogl.GL_TEXTURE_WRAP_S,
                            ogl.GL_CLAMP_TO_BORDER)
        ogl.glTexParameteri(ogl.GL_TEXTURE_2D,
                            ogl.GL_TEXTURE_WRAP_T,
                            ogl.GL_CLAMP_TO_BORDER)
        ogl.glTexParameterf(ogl.GL_TEXTURE_2D,
                            ogl.GL_TEXTURE_WRAP_S,
                            ogl.GL_CLAMP)
        ogl.glTexParameterf(ogl.GL_TEXTURE_2D,
                            ogl.GL_TEXTURE_WRAP_T,
                            ogl.GL_CLAMP)

        self._image = image

        #dimensions
        try :
            self._vx,self._vy,self._vz = image.resolution
        except AttributeError :
            self._vx,self._vy,self._vz = 1.,1.,1.

        #indices
        if slices is None :
            self._slices = range(image.shape[2])
        else :
            self._slices = [v for v in slices if 0 <= v < image.shape[2] ]

        #texture images
        self._pixmaps = []
        self._tex_inds = None

    def redraw (self) :
        """Create pixmaps associated with this image
        """
        img = self._image

        #clear previous textures
#        if self._tex_inds is not None :
#            for ind in self._tex_inds :
#                view.deleteTexture(ind)
#
#        self._tex_inds = None

        self._pixmaps = []

        #create new pixmaps
        for k in self._slices :
            pix = to_tex(img[:,:,k,:])
            self._pixmaps.append( (k,pix) )

        #self._pixmaps.reverse()

    ############################################
    #
    #    display
    #
    ############################################
    def draw (self, view, mode) :
        vx = self._vx
        vy = self._vy
        vz = self._vz

        if False and mode == DRAW_MODE.DRAFT :
            ogl.glPushAttrib(ogl.GL_LIGHTING_BIT)
            ogl.glDisable(ogl.GL_LIGHTING)
            ogl.glColor3f(0.8,0.8,0.8)

            for k,pix in self._pixmaps :
                xmax = pix.width() * vx / 2.
                ymax = pix.height() * vy / 2.
                z = k * vz
                ogl.glBegin(ogl.GL_LINE_LOOP)
                ogl.glVertex3f(-xmax,-ymax,z)
                ogl.glVertex3f( xmax,-ymax,z)
                ogl.glVertex3f( xmax, ymax,z)
                ogl.glVertex3f(-xmax, ymax,z)
                ogl.glEnd()

            ogl.glPopAttrib()
        elif True or mode == DRAW_MODE.NORMAL :
            ogl.glTexEnvf(ogl.GL_TEXTURE_ENV,
                          ogl.GL_TEXTURE_ENV_MODE,
                          ogl.GL_REPLACE)

            if self._tex_inds is None :
                self._tex_inds = []
                ogl.glPixelStorei(ogl.GL_UNPACK_ALIGNMENT,1)

                for k,pix in self._pixmaps :
                    ind = ogl.glGenTextures(1)
                    self._tex_inds.append(ind)
                    ogl.glBindTexture(ogl.GL_TEXTURE_2D, ind)
                    ogl.glTexParameterf(ogl.GL_TEXTURE_2D,
                                        ogl.GL_TEXTURE_MAG_FILTER,
                                        ogl.GL_NEAREST)
                    ogl.glTexParameterf(ogl.GL_TEXTURE_2D,
                                        ogl.GL_TEXTURE_MIN_FILTER,
                                        ogl.GL_NEAREST)
                    ogl.glTexImage2D(ogl.GL_TEXTURE_2D, 0, ogl.GL_RGBA,
                                     pix.shape[0], pix.shape[1], 0,
                                     ogl.GL_RGBA, ogl.GL_UNSIGNED_BYTE, pix)

            #reverse pixmap if view from top
            up = view.camera().viewDirection()[2] > 0
            if up  :
                pixmaps = self._pixmaps[::-1]
                tex = self._tex_inds[::-1]
                ogl.glNormal3f(0.,0.,-1.)
            else :
                pixmaps = self._pixmaps
                tex = self._tex_inds
                ogl.glNormal3f(0.,0.,1.)

            #draw slides
            ogl.glPushAttrib(ogl.GL_LIGHTING_BIT)
            ogl.glDisable(ogl.GL_LIGHTING)
            ogl.glColor3f(0.,0.,0.)
            ogl.glEnable(ogl.GL_TEXTURE_2D)
            for ind,(k,pix) in enumerate(pixmaps) :
                xmax = pix.shape[0] * vx
                ymax = pix.shape[1] * vy
                z = k * vz
                ogl.glBindTexture(ogl.GL_TEXTURE_2D,tex[ind])
                ogl.glBegin(ogl.GL_QUADS)
                ogl.glTexCoord2f(0.,0.)
                ogl.glVertex3f(0.,0.,z)
                ogl.glTexCoord2f(1.,0.)
                ogl.glVertex3f( xmax,0.,z)
                ogl.glTexCoord2f(1.,1.)
                ogl.glVertex3f( xmax, ymax,z)
                ogl.glTexCoord2f(0.,1.)
                ogl.glVertex3f(0., ymax,z)
                ogl.glEnd()

            ogl.glDisable(ogl.GL_TEXTURE_2D)
            ogl.glPopAttrib()
        else :
            print "toto"

    #########################################################
    #
    #        geometrical attributes
    #
    #########################################################
    def bounding_box (self) :
        """Bounding box of the displayed element

        :Returns Type: :class:BoundingBox
        """
        from vplants.plantgl.scenegraph import BoundingBox
        if len(self._pixmaps) == 0 :
            return None
        else :
            xmax = self._image.shape[1] * self._vx / 2.
            ymax = self._image.shape[0] * self._vy / 2.
            zmin = min(self._slices) * self._vz
            zmax = max(self._slices) * self._vz
            return BoundingBox( (-xmax,-ymax,zmin),(xmax,ymax,zmax) )

    def position (self) :
        """Position of the displayed element

        :Returns Type: Vector
        """
        return Vec(0,0,0)

    def center (self) :
        """Position of the center of the element

        :Returns Type: Vector
        """
        return Vec(0,0,0)

