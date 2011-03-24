Architecture
============

Take one
---------

From the previous study, we decided to begin an experiment named SecondNature with
a UI inpired from Blender's, to identify data management issues
and to begin to explore the extensibality needs and, maybe,
come up with a component system.

Status
******
We currently have a rather nice UI demo. The data management issues have been identified
but not treated. There is a small extension framework.

UI structure
************

The main window has a menu bar, a status bar and a Layout area.

The Layout area is the part that is customizable. It holds special
widgets that are hierarchically subdividable. Each subdivision is called a Space.
Each space can hold an Applet, which is at least a QWidget. The user can choose
which Applet to show in which Space. An Applet could also be an assembly of a
tool bar, a menu bar and a QWidget.

This allows the user to have the tools and views he needs.

Layouts can be predefined and contributed through an extension mecanism. They could
also be managed by the user, like Blender or Eclipse do.

Applets can be added/managed through an extension mecanism.


Data Management
***************

There are at least two aspects to this question: sharing data between
editors in the same session, and sharing data between job A and job B.
The second point implies a way to represent job A and job B, the equivalent
of a Blend file. Job A contains some precious resources that can be very
useful for job B. Let's call each a "Project".


Intra-project communication - Runtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Inter-editor**
Having many different editors opened at once is nice, but the really cool part
comes when we start using these editors together. If there is a curve editor in one
view, how de we use it in LPy ?

This means dynamic sharing of resources:
* datapool
* document manager
* software bus

Inter-project communication
~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Between job A and job B**

Being able to exchange data between two projects means being able to locate a project,
and being able to locate a resource inside of this project.

To the first aspect, the PackageManager can be a great tool. There might
also be a something to take from URLs, URIs. There currently is a test
in the PackageManager.

The second aspect is treated in Blender through the database-like
structure of the blend file (objects stored in folders depending
on their types and referenced by a unique id).



Extensibility
*************
During this experiment we tried to identify an API that would let us
add more applets or layouts to SecondNature.

We created a few base classes:
* Layout and LayoutSpace
* AppletFactory
* (Unregisterable)Document

These three types are all managed by there own managers.

