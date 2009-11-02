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

import weakref
from PyQt4 import QtGui, QtCore
from openalea.core.settings import Settings
from openalea.grapheditor import qtgraphview
from openalea.visualea.util import open_dialog
from openalea.visualea.dialogs import DictEditor, ShowPortDialog, NodeChooser

#################################
# QtEvent handlers for vertices #
#################################


class GraphOperator(QtCore.QObject):
    def __init__(self, graphView, graphAdapter):
        QtCore.QObject.__init__(self)
        self.graphView = weakref.ref(graphView)
        self.vertexItem = None
        self.graphAdapter=weakref.ref(graphAdapter)
        #used when a vertex has been opened
        self._vertexWidget=None

    ###WHAT ???? I HAVE TO DO THIS TO
    ###CORRECTLY BIND AN OPERATOR'S
    ###METHODS TO A QT SIGNAL....
    ###WHY???????????????????????????
    def __get_wrapped(self, funcname):
        func = getattr(self,funcname,None)
        def wrapper(*args):
            func(*args)
        return wrapper, func.func_code.co_argcount 

    def get_action(self, actionName, parent, functionName):
        action = QtGui.QAction(actionName, parent)
        func, argcount = self.__get_wrapped(functionName)
        if (argcount) < 2 :
            QtCore.QObject.connect(action, QtCore.SIGNAL("triggered()"), func )
        else:
            QtCore.QObject.connect(action, QtCore.SIGNAL("triggered(bool)"), func )
        return action

    def __call__(self, actionName, parent, functionName):
        return self.get_action(actionName, parent, functionName)


    ####################################
    # The actual methods -- For graphs #
    ####################################
    def set_session(self, session):
        self.__session = session

    def set_interpreter(self, interp):
        self.__interpreter = interp
    
    def graph_set_selection_colour(self):
        items = self.graphView().get_selected_items()
        if(not items): return

        color = QtGui.QColorDialog.getColor( QtGui.QColor(100,100,100,255), self)
        if not color.isValid():
            return

        color = [color.red(), color.green(), color.blue()]
        for i in items:
            if not isinstance(i, qtgraphview.QtGraphViewVertex): continue
            try:
                i.get_ad_hoc_dict().set_metadata("user_color", col)
                i.get_ad_hoc_dict().set_metadata("use_user_color", True)
            except Exception, e:
                print e
                pass   

    def graph_remove_selection(self):
        items = self.graphView().get_selected_items()
        if(not items): return
        for i in items:
            if isinstance(i, qtgraphview.QtGraphViewVertex):
                if self.graphAdapter().is_vertex_protected(i.vertex()): continue
                self.graphAdapter().remove_vertex(i.vertex())
            elif isinstance(i, qtgraphview.QtGraphViewEdge):
                self.graphAdapter().remove_edge( (i.src().vertex(), i.src()),
                                                 (i.dst().vertex(), i.dst()) )
            else:
                print "mysterious deletion of:", i
                self.graphView().removeItem(i)
                
    def graph_group_selection(self, factory):
        """
        Export selected node in a new factory
        """
        def cmp_x(i1, i2):
            return cmp(i1.pos().x(), i2.pos().x())

        items = self.get_selected_item()
        if(not items): return None
        items.sort(cmp=cmp_x)

        self.graphAdapter().graph().to_factory(factory, items, auto_io=True)
        pos = self.graphView().get_selection_center(items)

        # Instantiate the new node
        newVert = factory.instantiate([self.graphAdapter().graph().factory.get_id()])
        if newVert is not False:
            self.graphAdapter().add_vertex(newVert, pos)
            new_edges = self.graphAdapter().graph().compute_external_io(s, new_id)
            self.graphAdapter.add_edge((newEdges[0],newEdges[1]), (newEdges[2], newEdges[3]))
            self.graph_remove_selection()
        
    def copy(self):
        """ Copy Selection """
        if(self.__interpreter.hasFocus()):
            try:
                self.__interpreter.copy()
            except:
                pass
        else:
            s = self.get_selected_item()
            if(not s): return 
            self.__session.clipboard.clear()
            self.graphAdapter().graph().to_factory(session.clipboard, s, auto_io=False)

    def paste(self):
        """ Paste from clipboard """

        if(self.__interpreter.hasFocus()):
            try:
                self.__interpreter.paste()
            except:
                pass
        else:
            # Get Position from cursor
            position = self.graphView().mapToScene(
                self.mapFromGlobal(self.cursor().pos()))
            self.graphView().select_added_elements(True)

            # Translate new node
            #l = lambda x :  x + 30
            #modifiers = [('posx', l), ('posy', l)]
            # Compute the min x, y value of the nodes
            # 
            cnode = self.__session.clipboard.instantiate()

            min_x = min([cnode.node(vid).internal_data['posx'] for vid in cnode if vid not in (cnode.id_in, cnode.id_out)])
            min_y = min([cnode.node(vid).internal_data['posy'] for vid in cnode if vid not in (cnode.id_in, cnode.id_out)])

            lx = lambda x : x - min_x + position.x()
            ly = lambda y : y - min_y + position.y()
            modifiers = [('posx', lx), ('posy', ly)]

            #modifiers = [('posx', position.x()), ('posy', position.y())]
            new_ids = self.__session.clipboard.paste(self.graphAdapter().graph(), modifiers)

        

    ######################################
    # The actual methods -- For vertices #
    ######################################
    def set_vertex_item(self, vertexItem):
        self.vertexItem = weakref.ref(vertexItem)        

    def vertex_run(self):
        self.graphAdapter().graph().eval_as_expression(self.vertexItem().vertex().get_id())        

    def vertex_open(self):
        if(self._vertexWidget):
            if(self._vertexWidget.isVisible()):
                self._vertexWidget.raise_ ()
                self._vertexWidget.activateWindow ()
            else:
                self._vertexWidget.show()
            return

        factory = self.vertexItem().vertex().get_factory()
        if(not factory) : return
        # Create the dialog. 
        # NOTE: WE REQUEST THE MODEL TO CREATE THE DIALOG
        # THIS IS NOT DESIRED BECAUSE IT COUPLES THE MODEL
        # TO THE UI.
        innerWidget = factory.instantiate_widget(self.vertexItem().vertex(), None)
        if(not innerWidget) : return 
        if (innerWidget.is_empty()):
            innerWidget.close()
            del innerWidget
            return

        self._vertexWidget = open_dialog(self.graphView(), innerWidget, factory.get_id(), False)

    def vertex_remove(self):
        self.graphAdapter().remove_vertex(self.vertexItem().vertex().get_id())

    def vertex_reset(self):
        self.vertexItem().vertex().reset()

    def vertex_replace(self):
        """ Replace a node by an other """
        
        self.dialog = NodeChooser(self.graphView())
        self.dialog.search('', self.vertexItem().vertex().get_nb_input(), 
                           self.vertexItem().vertex().get_nb_output())
        ret = self.dialog.exec_()

        if(not ret): return
        
        factory = self.dialog.get_selection()
        newnode = factory.instantiate()
        self.graphAdapter().replace_vertex(self.vertexItem().vertex(), newnode)

    def vertex_reload(self):
        """ Reload the vertex """

        # Reload package
        factory = self.vertexItem().vertex().factory
        package = factory.package
        if(package):
            package.reload()

        # Reinstantiate the vertex
        newvertex = factory.instantiate()
        self.graphAdapter().graph().set_actor(self.vertexItem().vertex().get_id(), newvertex)
        newvertex.internal_data.update(self.vertexItem().vertex().internal_data)
        self.vertexItem().set_observed(newvertex)
        self.vertexItem().initialise_from_model()

    def vertex_set_caption(self):
        """ Open a input dialog to set node caption """

        n = self.vertexItem().vertex()
        (result, ok) = QtGui.QInputDialog.getText(None, "Node caption", "",
                                   QtGui.QLineEdit.Normal, n.caption)
        if(ok):
            n.caption = str(result) #I HATE PROPERTIES, REALLY!

    def vertex_show_hide_ports(self):
        """ Open port show/hide dialog """
        editor = ShowPortDialog(self.vertexItem().vertex(), self.graphView())
        editor.exec_()

    def vertex_mark_user_app(self, val):
        self.graphAdapter().graph().set_continuous_eval(self.vertexItem().vertex().get_id(), bool(val))

    def vertex_set_lazy(self, val):
        self.vertexItem().vertex().lazy = val #I HATE PROPERTIES, REALLY!

    def vertex_block(self, val):
        self.vertexItem().vertex().block = val #I HATE PROPERTIES, REALLY!

    def vertex_edit_internals(self):
        """ Edit node internal data """
        editor = DictEditor(self.vertexItem().vertex().internal_data, self.graphView())
        ret = editor.exec_()

        if(ret):
            for k in editor.modified_key:
                self.vertexItem().vertex().set_data(k, editor.pdict[k])





def vertexMouseDoubleClickEvent(self, event):
    if event.button()==QtCore.Qt.LeftButton:
        # Read settings
        try:
            localsettings = Settings()
            str = localsettings.get("UI", "DoubleClick")
        except:
            str = "['open']"

        view = self.scene().views()[0]
        operator=GraphOperator(view, self.graph)
        operator.set_vertex_item(self)

        if('open' in str):
            operator.vertex_open()
        elif('run' in str):
            operator.vertex_run()



def vertexContextMenuEvent(self, event):
    """ Context menu event : Display the menu"""
    view = self.scene().views()[0]
    operator=GraphOperator(view, self.graph)
    operator.set_vertex_item(self)
    menu = QtGui.QMenu(view)

    menu.addAction(operator("Run",             menu, "vertex_run"))
    menu.addAction(operator("Open Widget",     menu, "vertex_open"))
    menu.addSeparator()
    menu.addAction(operator("Delete",          menu, "vertex_remove"))
    menu.addAction(operator("Reset",           menu, "vertex_reset"))
    menu.addAction(operator("Replace By",      menu, "vertex_replace"))
    menu.addAction(operator("Reload",          menu, "vertex_reload"))
    menu.addSeparator()
    menu.addAction(operator("Caption",         menu, "vertex_set_caption"))
    menu.addAction(operator("Show/Hide ports", menu, "vertex_show_hide_ports"))
    menu.addSeparator()

    action = operator("Mark as User Application", menu, "vertex_mark_user_app")
    action.setCheckable(True)
    action.setChecked( bool(self.vertex().user_application))
    menu.addAction(action)

    action = operator("Lazy", menu, "vertex_set_lazy")
    action.setCheckable(True)
    action.setChecked(self.vertex().lazy)
    menu.addAction(action)

    action = operator("Block", menu, "vertex_block")
    action.setCheckable(True)
    action.setChecked(self.vertex().block)
    menu.addAction(action)

    menu.addAction(operator("Internals", menu, "vertex_edit_internals"))

    menu.move(event.screenPos())
    menu.show()
    del menu
    event.accept()










qtgraphview.QtGraphViewVertex.set_event_handler("mouseDoubleClickEvent", 
                                                vertexMouseDoubleClickEvent)
qtgraphview.QtGraphViewVertex.set_event_handler("contextMenuEvent", 
                                                vertexContextMenuEvent)
