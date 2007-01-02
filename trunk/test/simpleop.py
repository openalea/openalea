# Node creation
# Simple operations



from aleacore.core import Node

# do import 


class Add(Node):
    """ Generic Addition
    Input 0 : First value to add
    Input 1 : Second value to add
    Output 0 : Addition result
    """

    def __init__(self):

        Node.__init__(self)

        # defines I/O
        self.define_inputs([None, None])
        self.define_outputs([None])

        self.set_default_input(0, 0.)
        self.set_default_input(1, 0.)


    def __call__(self, inputs=() ):
        """ inputs is the list of input values """

        return ( sum(inputs), )


class Value(Node):
    """ Variable
    Input 0 : if connected, set the stored value
    Ouput 0 : transmit the stored value
    """

    def __init__(self):

        Node.__init__(self)

        self.define_inputs([None])
        self.define_outputs([None])

        self.val=0.
        self.set_default_input(0, self.val)

    def get_value(self):
        return self.val

    def set_value(self, v):
        self.val=v
        self.set_default_input(0, self.val)

    value=property(get_value, set_value)

#     def __call__(self):

#         i0=self.get_input(0)
        
#         if(i0 != self.value ) :
#             self.val = i0

#         self.set_output(0, self.val )
   

    def __call__(self, inputs=()):
        """ inputs is the list of input values """
        
        i0=inputs[0]
        
        if(i0 != self.val ) :
            self.value = i0

        return ( self.value,  )
        
