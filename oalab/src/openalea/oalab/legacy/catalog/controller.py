
import string

from .catalog import Catalog

class Implementation(object): pass

class Controller(object):
    def __init__(self):
        self.catalog = Catalog()
        self._implementations = set()

    def __setattr__(self, attrib, value):
        if value == Implementation:
            self._implementations.add(attrib)
        else:
            super(Controller, self).__setattr__(attrib, value)


    def __getattr__(self, attrib):
        try:
            value = super(Controller, self).__getattr__(attrib)
        except AttributeError:
            if attrib in self._implementations :
                if attrib[0] in string.lowercase:
                    value = self.catalog.service(interfaces=self.catalog._lowername[attrib])
                else:
                    value = self.catalog.factory(interfaces=self.catalog._lowername[attrib.lower()], tags=['plugin'])
            else :
                if attrib.startswith('I'):
                    value = self.catalog.interface(attrib)
                elif attrib[0] in string.lowercase:
                    if attrib.endswith('s'):
                        value = self.catalog.services(interfaces=self.catalog._lowername[attrib[:-1]])
                    else:
                        value = self.catalog.service(interfaces=self.catalog._lowername[attrib])
                else:
                    if attrib.endswith('s'):
                        value = self.catalog.factories(interfaces=self.catalog._lowername[attrib.lower()[:-1]], tags=['plugin'])
                    else:
                        value = self.catalog.factory(interfaces=self.catalog._lowername[attrib.lower()], tags=['plugin'])

        return value

    def __getattr__old(self, attrib):
        try:
            value = super(Controller, self).__getattr__(attrib)
        except AttributeError:
            if attrib.startswith('I') and attrib in self._implementations:
                value = self.catalog.factory(interfaces=self.catalog._lowername[attrib.lower()], tags=['plugin'])
            elif attrib.startswith('I'):
                value = self.catalog.interface(attrib)
            elif attrib[0] in string.lowercase:
                value = self.catalog.service(interfaces=self.catalog._lowername[attrib])
            else:
                value = self.catalog.factory(interfaces=self.catalog._lowername[attrib.lower()], tags=['plugin'])
        return value
