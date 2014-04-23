

class OALabHelpWidget(object):

    data = {
        'name' : 'HelpWidget',
        'extensions': ['plant', 'tissue'],
        'implements' : ['IHelper', 'IQWidget', 'IOAGuiComponent']
    }

    def __call__(self, oalab):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.help import HelpWidget
        from openalea.vpltk.qt import QtCore

        widget = HelpWidget()

        # Link OpenAleaLab and HelpWidget
        # 1. Add it to the right area.
#         oalab.add_widget_to_info_area(widget)

        for action in widget.actions():
            # Add actions in PanedMenu
            oalab.menu.addBtnByAction(*action)

        oalab.setCentralWidget(widget)
#         oalab.dockWidget("HelpWidget", widget,
#                          position=QtCore.Qt.RightDockWidgetArea,
#                          alias="Help")


