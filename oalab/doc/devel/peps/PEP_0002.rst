
Declarative Language to Design GUI
##################################

Overview of existing technologies
=================================

Qt QML
------

See `QML Documentation <https://qt-project.org/doc/qt-5/qmlapplications.html>`_.

  - `JSON like <http://fr.wikipedia.org/wiki/JSON>`_
  - Wide Qt support
  - Works with PyQt4

.. code-block:: python

   import sys
   
   from PyQt4.QtCore import QUrl
   from PyQt4.QtGui import QApplication
   from PyQt4.QtDeclarative import QDeclarativeView
   
   app = QApplication(sys.argv)
   
   # Create the QML user interface.
   view = QDeclarativeView()
   view.setSource(QUrl('sample_qml.qml'))
   view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
   view.show()
   
   app.exec_()


.. code-block:: qml

   import QtQuick 1.0
   
   Item {
       width: 200; height: 200
   
       Rectangle {
           // Anchored to 20px off the top right corner of the parent
           anchors.right: parent.right
           anchors.top: parent.top
           anchors.margins: 20 // Sets all margins at once
   
           width: 80
           height: 80
           color: "orange"
       }
   
       Rectangle {
           // Anchored to 20px off the top center corner of the parent.
           // Notice the different group property syntax for 'anchors' compared to
           // the previous Rectangle. Both are valid.
           anchors { horizontalCenter: parent.horizontalCenter; top: parent.top; topMargin: 20 }
   
           width: 80
           height: 80
           color: "green"
       }
   }

ETS TraitsUi
------------

See `TraitsUi/View Manual <http://docs.enthought.com/traitsui/traitsui_user_manual/view.html>`_.

Class View used to describe layout, widget styles and positions.

Example:

.. code-block:: python

   comp_view = View(
       Group(
           Group(
               Item('h1.address', resizable=True),
               Item('h1.bedrooms')
               show_border=True
           ),
           Group(
               Item('h2.address', resizable=True),
               Item('h2.bedrooms'),
               show_border=True
           ),
           orientation = 'horizontal'
       ),
       title = 'House Comparison'
   )


ETS Enaml
---------

See `ENAML Documentation <http://docs.enthought.com/enaml>`_
Idea of TraitsUi + QML.

Example:

.. code-block:: python

   enamldef PersonForm(Form):
       attr person
       Label:
           text = 'First Name'
       Field:
           text := person.first_name
       Label:
           text = 'Last Name'
       Field:
           text := person.last_name
       Label:
           text = 'Age'
       IntField:
           minimum = 0
           value := person.age
   
   
   enamldef PersonView(Window):
       attr person
       PersonForm:
           person := parent.person


Proposal
========

Home made syntax
----------------

.. code-block:: python

  view = {
      'top': {
          'widgets':['Widget1', 'Widget2'], 
          'orientation':'vertical'
          }
      }


First idea, QML has not been tested

  - Use QML idea with limited properties to be easily extended to other toolkits (IPython Notebook for example)
  - For Qt backend, implementation should be direct

