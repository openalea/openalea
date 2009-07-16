"""This module illustrates how to write your docstring in OpenAlea
and other projects related to OpenAlea."""

__license__ = "Cecill-C"
__revision__ = " $Id: actor.py 1586 2009-01-30 15:56:25Z cokelaer $ "
#__docformat__ = 'reStructuredText'


class MainClass1(object):
    """Demonstrates how to fill the docstrings with Method1"""

    def function1(self, arg1, arg2, arg3):
        """returns (arg1 / arg2) + arg3

        This is a longer explanation, which may include math :math:`\\alpha`.

        :param arg1: the first value
        :param arg2: the first value
        :param arg3: the first value
        :type arg1: int, float,... 
        :type arg2: int, float,... 
        :type arg3: int, float,... 
        :returns: arg1/arg2 +arg3
        :rtype: int, float 
       
        :Example:        

        >>> import template_final
        >>> a = template_final.MainClass1()
        >>> a.function1(1,1,1)
        2

        .. note:: can be useful to emphasize 
            important feature
        .. seealso:: :class:`MainClass2`
        .. warning:: arg2 must be non-zero.
        .. todo:: check that arg2 is non zero.
        """
        return arg1/arg2 + arg3


class MainClass2(object):
    """Demonstrates how to fill the docstrings with Method2"""
 
    def function1(self, arg1, arg2, arg3):
        """returns (arg1 / arg2) + arg3
        
        This is a longer explanation, which may include math :math:`\\alpha`.
        
        :Parameters:
          - `arg1` (int,float,...) - the first value
          - `arg2` (int,float,...) - the first value
          - `arg3` (int,float,...) - the first value
         
        :Returns:
            arg1/arg2 +arg3
            
        :Returns Type:
            int,float 
       
        :Examples:        
            >>> import template_final
            >>> a = template_final.MainClass2()
            >>> a.function1(1,1,1)
            2

        .. note:: can be useful to emphasize 
            important feature
        .. seealso:: :class:`MainClass2`
        .. warning:: arg2 must be non-zero.
        .. todo:: check that arg2 is non zero.
        """
        return arg1/arg2 + arg3


class MainClass3(object):
    """Demonstrates how to fill the docstrings with Method3"""
 
    def function1(self, arg1, arg2, arg3):
        """returns (arg1 / arg2) + arg3
        
        This is a longer explanation, which may include math :math:`\\alpha`.
        
        Parameters
        ----------
        
        arg1 : (int,float,...)
            the first value
        arg2 : (int,float,...)
            the first value
        arg3 : (int,float,...)
            the first value
         
        Returns
        -------
        
            arg1/arg2 +arg3 : the output
        
        Examples
        --------

        >>> import template_final
        >>> a = template_final.MainClass3()
        >>> a.function1(1,1,1)
        2

        Notes
        -----
     
        Can be useful to emphasize 
        important feature

        See Also
        --------
            
           :class:`MainClass1`
            
        Warnings
        --------
        arg2 must be non-zero.      
        
  
        Todo
        ----
                        
            check that arg2 is non zero.
        """
        return arg1/arg2 + arg3

if __name__ == "__main__":
    import doctest
    doctest.testmod()
