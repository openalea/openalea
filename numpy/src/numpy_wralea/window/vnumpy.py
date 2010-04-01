from openalea.core import Node, IInt, IFloat, IEnumStr


class window(Node):

    windows = ['hanning', 'hamming', 'bartlett', 'kaiser', 'None', 'blackman']

    def __init__(self):
        Node.__init__(self)
        self.add_input(name='window', interface=IEnumStr(self.windows), value='hanning')
        self.add_input(name='n', interface=IInt, value=256)
        self.add_input(name='beta (kaiser only)', interface=IFloat(0.,100.,1), value=14.)
        self.add_output(name='array')

    def __call__(self, inputs):
        if self.get_input('window')=='hanning':
            from numpy import hanning
            return hanning(self.get_input('n'))
        elif self.get_input('window')=='hamming':
            from numpy import hamming
            return hamming(self.get_input('n'))
        elif self.get_input('window')=='bartlett':
            from numpy import bartlett
            return bartlett(self.get_input('n'))
        elif self.get_input('window')=='blackman':
            from numpy import blackman
            return blackman(self.get_input('n'))
        elif self.get_input('window')=='kaiser':
            from numpy import kaiser
            return kaiser(self.get_input('n'), self.get_input('beta (kaiser only)'))
        elif self.get_input('window')=='None':
            from numpy import kaiser
            return kaiser(self.get_input('n'), 0.)
        else:
            raise ValueError("should never enter here since window values is an enum selector")
