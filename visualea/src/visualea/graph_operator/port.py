# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
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

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from Qt import QtCore, QtGui, QtWidgets

from openalea.visualea.graph_operator.base import Base

class PortOperators(Base):
    """The PortOperators defines the output options of an output connector.

    An output connector can be sent to

        * the datapool,
        * the python interpreter
        * or print

    by right clicking on the output connector and selected the appropriate option, as shown on this screenshot.

    .. image:: ../_static/visualea_output_port.png
        :width: 600px
        :height: 400px
        :class: align-center

    """
    def port_print_value(self):
        """ Print the value of the connector """
        portItem = self.master.get_port_item()
        node = portItem.port().vertex()
        data = str(node.get_output(portItem.port().get_id()))
        data = data[:500]+"[...truncated]" if len(data)>500 else data
        print data


    def port_send_to_pool(self):
        """Send data from a connector to the dataflow


        This function is related to the menu that pops up when right clicking on a node.


        .. seealso:: :class:`openalea.visualea.dataflowview.vertex.GraphicalPort`

        """
        master = self.master
        widget = master.get_sensible_parent()
        portItem = master.get_port_item()
        (result, ok) = QtWidgets.QInputDialog.getText(widget, "Data Pool", "Instance name",
                                                  QtWidgets.QLineEdit.Normal, )
        if(ok):
            from openalea.core.session import DataPool
            datapool = DataPool()  # Singleton

            port = portItem.port()
            node = port.vertex()
            data = node.get_output(port.get_id())
            datapool[str(result)] = data


    def port_send_to_console(self):
        """a portconnector to send output on a port directly to the console.
        :authors: Thomas Cokelaer, Daniel Barbeau
        """
        # get the visualea master
        master = self.master
        widget = master.get_sensible_parent()
        portItem = master.get_port_item()
        # pop up a widget to specify the instance name
        (result, ok) = QtWidgets.QInputDialog.getText(widget, "Console", "Instance name",
                                                  QtWidgets.QLineEdit.Normal, )
        result = str(result)

        if(ok):
            port = portItem.port()
            node = port.vertex()
            data = node.get_output(port.get_id())
            interpreter = master.get_interpreter()

            overwrite = QtWidgets.QMessageBox.Ok
            if result in interpreter.locals:
                overwrite = QtWidgets.QMessageBox.warning(widget, "Overwrite variable?",
                                                      "Variable name '" + result +"' is already used in the interpreter," +\
                                                      "Do you want to overwrite it?",
                                                      QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Ok)
            if overwrite == QtWidgets.QMessageBox.Ok:
                interpreter.locals[result]=data
                # print the instance name and content as if the user type its name in a shell
                # this is only to make obvious the availability of the instance in the
                try: interpreter.runsource(result, hidden=False, interactive=True)
                except:
                    interpreter.runsource("%s\n" % result)

            #setFocus()
