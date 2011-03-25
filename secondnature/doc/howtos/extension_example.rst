An image processing extension
#############################

We want to create an image processing extension : we can at least create
images from scratch, open image files and view them.

We will create a DataFactory that creates/reads images and an AppletFactory
that create views/editors for images.

Here is our code layout:
 * image <dir>
    * :download:`**setup.py**<../../example/image/setup.py>` Used for installation process.
    * :download:`**image_ext.py**<../../example/image/image_ext.py>` Contains our implementation of the extension


We will first focus on the implementation, not the installation.


Implementation
==============
At the top of image/image_ext.py:

.. literalinclude:: ../../example/image/image_ext.py
    :language: python
    :lines: 21-23


The data factory
----------------
Declaration
'''''''''''
We can both create and read images. If we could only create images we would
inherit from DataFactory. But since we can read images we must inherit from
DataReader (which inherits from DataFactory) and fill a few fields:

.. literalinclude:: ../../example/image/image_ext.py
    :language: python
    :lines: 30-47


Next, there are a few abstract methods to implement. The first one is **new**,
declared by DataFactory, and the second one is **open_url** from DataReader:

.. literalinclude:: ../../example/image/image_ext.py
    :language: python
    :lines: 50-102

That's it. More or less 31 lines of code to create the Image reader. If you need
initialisation of your factory, you can implement the **start(self) : bool** method (do
NOT reimplement __init__(self)).

Note that we make heavy use of mimetypes. This is because it is a widely used system
to identify data types outside an application context and that,
since it is used by many applications, it makes us
ready to receive data from foreign sources. This
`page <http://www.w3schools.com/media/media_mimeref.asp>`
contains a list of mimetypes and format mappings.

Registration
''''''''''''
We have create DataFactories. There's still not available within SecondNature as
they have not yet been registered.

There are two methods depending on if you want to link the factory to an applet (use
that applet to edit/view data from that factory), or just be able to create data
using the factory (Project Manager's right click menu). For the first see
:ref:`here <the_applet_factory>`. For the second::

    mgr = DataFactoryManager() #API : it's a singleton
    mgr.add_custom_item( DT_Whatever() ) #note that we instantiate the DT_Whatever.


.. _the_applet_factory:

The Applet factory
------------------
Declaration
'''''''''''

We need to derive from AbstractApplet to implement the factory. To tell the system
that this applet can be used to view or edit data created with DT_Image.

.. literalinclude:: ../../example/image/image_ext.py
    :language: python
    :lines: 109-118

Then we need to tell the factory what to do when it is asked to view/edit data.
This goes by implementing the **create_space_content(self, data)** method.

.. literalinclude:: ../../example/image/image_ext.py
    :language: python
    :lines: 119-130

Registration
''''''''''''
Registering the factory to SecondNature happens through the "openalea.app.applet_factory"
entry point. See :ref:`The installation process <installation>`



.. _installation:

Installation
============
We use disutils/setuptools/distribute style of installation. The ImageViewerFactory class
is registered with the //openalea.app.applet_factory// entry point. The internal
AppletFactoryManager then can search for values registered with that entry point.

.. literalinclude:: ../../example/image/setup.py
    :language: python
    :lines: 21-32

