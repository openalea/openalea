from openalea.core.interface import IInterface


class IQTextWidget(IInterface):
    name = 'IQTextWidget'  # Unique identifier

    def setText(self, text):
        pass

    def text(self):
        pass


class IHelper(IInterface):
    name = 'IHelper'

    def setText(self, text):
        pass
