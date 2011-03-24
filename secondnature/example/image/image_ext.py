# -*- python -*-
#
#       OpenAlea.Secondnature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "CeCILL v2"
__revision__ = " $Id$ "


# -- Try to avoid too many extension-specific
# imports at the top level --
from openalea.secondnature.api import *






class DT_Image(DataReader): #By convention type classes are prefixed with DT_
    # -- Name of the data factory --
    __name__             = "Image"

    # -- Arbitrary mime-like string  used to match the
    # applet that can view/edit the created data. If you
    # can give a valid mimetype, then go for it! --
    __created_mimetype__ = "application/pixmap"

    # -- Actual mimetypes of objects that can be read
    # by this factory. Be exhaustive, no wildcards are
    # usable. Only used be DataReader subclasses --
    __opened_mimetypes__ = ["image/jpeg", "image/png"]

    # -- location of the icon to display for data created
    # by this factory. It can be relative to this module
    # or a Qt resource (don't forget the import in this case!) --
    __icon_rc__ = ":icons/image.png"


    def new(self):
        # -- Extension specific import --
        from my_image_lib import Image

        # -- We don't know how to pass arguments
        # down to here. However there is technically
        # nothing that forbids you from using a PyQt4
        # UI to customize the image creation. The only
        # problem is that your factory won't be usable
        # if SecondNature is run headless (which cannot happen - yet) --
        obj = Image()

        # -- Give a name to the data. If there already is
        # such a name in the active document, the name
        # will be modified internally. --
        instance_name = self.__name__

        # -- Create a wrapper around the raw image
        # with additional info like created mimetype,
        # factory, ..., which are used internally --
        wrapped = self.wrap_data(instance_name, obj)
        return wrapped

    def open_url(self, parsedUrl):
        "parsedUrl is a url issued by urlparse.urlparse(url)"""

        # -- Extension specific imports --
        from my_image_lib import Image
        import urllib2
        from os.path import splitext

        url = parsedUrl.geturl()   # the url as a simple str
        fmt = splitext(url)[1][1:] # the format of our image
        obj = None                 # variable to receive the Image instance

        # -- is it a local file ? --
        if parsedUrl.scheme == "file":
            path = file_url_to_path(url) # API : convert from url to local path
            obj  = Image(path)
        # -- else it's on the web! --
        else:
            rawstream = urllib2.urlopen(url)
            rawdata   = rawstream.read()
            rawstream.close()
            obj       = Image(rawstream, fmt) # in a really ideal world eh ;)

        if obj is None:
            return None

        instance_name = self.__name__
        wrapped       = self.wrap_data(instance_name, obj)
        return wrapped







class ImageViewerFactory(AbstractApplet):
    # -- naming things is always a good idea --
    __name__ = "ImageViewer"

    # -- register the factory to tell the system
    # that this extension handles created mimetype from DT_Image.
    # Notice that this is the class, not an instance! --
    __datafactories__ = [DT_Image]


    def create_space_content(self, data):
        if data.mimetype == DT_Image.__created_mimetype__:
            # -- Extension specific import --
            from my_image_lib import ImageViewer

            image  = data.obj      # retreive the actual Image
            editor = ImageViewer() #ImageViewer MUST inherit QWidget!
            editor.setImage(image)

        # -- SpaceContent is simply a class to
        # package together a QWidget, a QMenu and a QToolbar --
        return SpaceContent(editor)



