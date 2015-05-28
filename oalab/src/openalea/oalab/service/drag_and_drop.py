# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.vpltk.qt import QtGui


class UrlImageCodec(object):

    def decode(self, mimetype, mimedata, interface):
        from openalea.image.serial.basics import imread
        from openalea.core.path import path
        if mimetype == 'text/uri-list':
            for url in mimedata.urls():
                local_file = url.toLocalFile()
                local_file = path(local_file)
                if local_file.exists():
                    data = imread(local_file)
                    return data, dict(path=local_file, qurl=url,
                                      name=local_file.namebase)
        elif mimetype == 'openalealab/data':
            from openalea.core.project.manager import ProjectManager
            pm = ProjectManager()
            raw_data = mimedata.data('openalealab/data')
            data = pm.cproject.get_item('data', path(unicode(raw_data)).name)
            matrix = imread(data.path)
            return matrix, dict(path=data.path, name=data.filename)
        else:
            return None, {}


class UrlImageCodecPlugin(object):
    decode = {
        'text/uri-list': 'IImage',
        'openalealab/data': 'IImage',
    }
    encode = {}

    def __call__(self):
        return UrlImageCodec


from openalea.core.plugin.manager import PluginManager

pm = PluginManager()
pm.add_plugin('oalab.mimecodec', UrlImageCodecPlugin)

registry_decoder_i_fmt = {}
registry_decoder_fmt_i = {}
registry_decoder = {}

for plugin in pm.plugins('oalab.mimecodec'):
    for fmt, interface in plugin.decode.items():
        registry_decoder_fmt_i[fmt] = []
        registry_decoder_i_fmt[interface] = []

for plugin in pm.plugins('oalab.mimecodec'):
    for fmt, interface in plugin.decode.items():
        registry_decoder_fmt_i[fmt].append(interface)
        registry_decoder_i_fmt[interface].append(fmt)
        registry_decoder.setdefault(fmt, {})[interface] = plugin


def compatible_mime(mimedata, interfaces=None):
    compatible = {}
    if interfaces is None:
        for fmt in mimedata.formats():
            if fmt in registry_decoder_fmt_i:
                for i in registry_decoder_fmt_i[fmt]:
                    compatible[fmt] = i
    else:
        for interface in interfaces:
            if interface in registry_decoder_i_fmt:
                for fmt in mimedata.formats():
                    if fmt in registry_decoder_i_fmt[interface]:
                        for fmt in registry_decoder_i_fmt[interface]:
                            compatible[fmt] = interface
    return compatible


def decode(mimetype, data, interface):
    try:
        plugin = registry_decoder[mimetype][interface]
    except KeyError:
        return None, {}
    else:
        klass = plugin()()
        decoder = klass()
        return decoder.decode(mimetype, data, interface)


def encode(obj, mimetype=None):
    pass


class DragAndDrop(object):

    def __init__(self, widget, **kwargs):
        self.widget = widget
        self.kwargs = kwargs
        self.drop_callbacks = []

        self.widget.setAcceptDrops(True)

        self.widget.dragEnterEvent = self.drag_enter_event
        self.widget.dropEvent = self.drop_event
        self.widget.dragLeaveEvent = self.drag_leave_event
        #widget.dragMoveEvent = self.drag_move_event
        #widget.dropEvent = new.instancemethod(drop_event, widget, widget.__class__)

    def add_drop_callback(self, fmt, callback):
        self.drop_callbacks.append({fmt: callback})

    def drag_enter_event(self, event):
        self._compatible = compatible_mime(event.mimeData(), interfaces=self.callbacks.keys())

        if self._compatible:
            event.acceptProposedAction()
            return QtGui.QWidget.dragEnterEvent(self.widget, event)
        else:
            return QtGui.QWidget.dragEnterEvent(self.widget, event)

    def drag_leave_event(self, event):
        self._compatible = []
        return QtGui.QWidget.dragLeaveEvent(self.widget, event)

    def drag_move_event(self, event):
        if self._compatible:
            event.acceptProposedAction()
        else:
            event.ignore()

    def drop_event(self, event):
        data = interface = None
        kwds = {}
        for fmt in event.mimeData().formats():
            if fmt in self._compatible:
                interface = self._compatible[fmt]
                data, kwds = decode(fmt, event.mimeData(), interface)
                if data is not None:
                    break

        if data is not None and interface is not None:
            self.drop_callbacks[interface](data, **kwds)
            event.acceptProposedAction()
        else:
            return QtGui.QWidget.dropEvent(self.widget, event)
