"""This module illustrates how to write your docstring in OpenAlea
and other projects related to OpenAlea.



"""

__license__ = "Cecill-C"
__revision__ = " $Id: actor.py 1586 2009-01-30 15:56:25Z cokelaer $ "
__docformat__ = 'reStructuredText'


class MainClass1(object):
    """Demonstrates how to fill the docstrings with Method1  

    The :func:`function1`'s docstring is composed as follows:
   
    - sections such as **parameters**, **types**, **return** and **return types**
      use the following sphinx syntax (*Info field lists*) ::
          :param arg1: description
          :param arg2: description
          :type arg1: type description
          :type arg1: type description
          :return: return description
          :rtype: the return type description
    - Other sections such as **Example**, or non-standard section's name are 
      written using the double commas syntax::
      
          :Example:
          :Your preferred section title:
          
      which appears as follow:
       
      :Example:
      
      :Your preferred section title:
       
    - Finally special sections such as **See Also**, **Warnings**, **Notes** 
      use the sphinx syntax (*paragraph directives*)::
          .. seealso:: blabla 
          .. warnings also:: blabla
          .. note:: blabla
          .. todo:: blabla
           
    .. note::
        There are many other Info fields but they may be redundant:
            * param, parameter, arg, argument, key, keyword: Description of a 
              parameter.
            * type: Type of a parameter.
            * raises, raise, except, exception: That (and when) a specific 
              exception is raised.
            * var, ivar, cvar: Description of a variable.
            * returns, return: Description of the return value.
            * rtype: Return type.
    
    .. note::
        There are many other directives such as versionadded, versionchanged,
        rubric, centered, ... See the sphinx documentation for more details.

    Here below is the results of the :func:`function1` docstring.
    
    Then, you can compare with the second method in :class:`MainClass2`
    
    
    
    """

    def function1(self, arg1, arg2, arg3):
        """returns (arg1 / arg2) + arg3

        This is a longer explanation, which may include math :math:`\\alpha`.
        Then, you need to provide optional subsection in this order (just to be
        consistent and have a uniform documentation Nothing prevent you to
        switch the order):
        
          - parameters using ``:param <name>: <description>``
          - type of the parameters ``:type <name>: <description>``
          - returns using ``:returns: <description>``
          - examples (doctest)
          - seealso using ``.. seealso:: text``
          - notes using ``.. note:: text``
          - warning using ``.. warning:: text``
          - todo ``.. todo:: text``

        **Advantages**:
         - Uses sphinx markups, which will certainly be improved in future 
           version
         - Nice HTML output with the See Also, Note, Warnings directives

        
        **Drawbacks**:
         - Just looking at the docstring, the parameter, type and  return 
           sections do not appear nicely 

        :param arg1: the first value
        :param arg2: the first value
        :param arg3: the first value
        :type arg1: int, float,... 
        :type arg2: int, float,... 
        :type arg3: int, float,... 
        :returns: arg1/arg2 +arg3
        :rtype: int, float 
       
        :Example:        

        >>> import template
        >>> a = MainClass1()
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
    """This class inherits the class :class:`object`

    The :func:`function1`'s docstring is composed as follows:

    - All sections such as **parameters** are written using the double commas 
      syntax::
         :Example:
         :Your preferred section title:
      which appears as follow:

      :Example:

      :Your preferred section title:

    Here below is the results of the :func:`function1` docstring.
   
    Then, you can compare with the second method in :class:`MainClass3`
     
    """
 
    def function1(self, arg1, arg2, arg3):
        """returns (arg1 / arg2) + arg3
        
        This is a longer explanation, which may include math :math:`\\alpha`.
        Then, you need to provide optional subsection in this order (just to be
        consistent and have a uniform documentation Nothing prevent you to
        switch the order):
        
          - parameters using ``:Parameters: - `arg1` (type) - description``
          - returns using ``:Returns: <description>``
          - examples ``:Examples: <description>``
          - seealso using ``:See Also: <description>``
          - notes using ``:Notes: <description>``
          - warning using ``:Warning: <description>``
          - todo using ``:TODO: <description>``
          
        **Advantages**:
          - The parameter, type, and return section appear nicely
          - can be combined with sphinx markup, although this is not done in 
            this example
              
        **Drawbacks**:
         - standard markups are not used, which is pity: you miss the nice 
           colored output and future add-ons 
         - do not take advantage of the automatic HTML output used with :param:, 
           :return: and  :type: syntax. So, you need to be very careful to 
           specify the italic syntax for the argument name, put parentheses and 
           so on
        
        :Parameters:
         - `arg1` (int,float,...) - the first value
         - `arg2` (int,float,...) - the first value
         - `arg3` (int,float,...) - the first value
         
        :Returns:
            arg1/arg2 +arg3
            
        :Returns Type:
            int,float 
       
        :Examples:        

        >>> import template
        >>> a = MainClass2()
        >>> a.function1(1,1,1)
        2

        :Note:
            can be useful to emphasize 
            important feature

        :See Also:
            :class:`MainClass1`
        
        :Warnings:
            arg2 must be non-zero.
            
        :Todo:
            check that arg2 is non zero.
            
        .. todo:: 
            combine this kind of syntax (double column) with sphinx markups
        """
        return arg1/arg2 + arg3


class MainClass3(object):
    """This class inherits the class :class:`object`
 
    The *function1*'s docstring is composed as follows:
    
    All sections such as **parameters** are written using the numpy syntax::

        >>>Parameters
        >>>----------
        >>>example : example
        >>>example : example        

          
    which appears as follow
       
    Parameters
    ----------
    
    example : example.
    example : example.
    
    
    Note that if you must have a space before or after the: sign otherwise
    the text until the next: sign will be in bold.
              
    Here below is the results of the :func:`function1` docstring.
    
    Then, you can compare with the second method in :class:`MainClass1` and 
    `MainClass2`
     
    """
 
    def function1(self, arg1, arg2, arg3):
        """returns (arg1 / arg2) + arg3
        
        This is a longer explanation, which may include math :math:`\\alpha`.
        Then, you need to provide optional subsection in this order (just to be
        consistent and have a uniform documentation Nothing prevent you to
        switch the order):
        
          - The syntax describe in :class:`MainClass2` but the section's title
            becomes::
             
                
          
        **Advantages**:
          - The parameter, type, and return section appear nicely in the docstring
          - interactive python will have the same next nice docstring
          - Some of the section are recognized and interpreted as sphinx syntax
          (such as warning which becomes .. warning::)
              
        **Drawbacks**:
         - standard markups are not used, which is pity: you miss the nice 
           colored output and future add-ons (e.g., ..see also::)
         - do not take advantage of the automatic HTML output used with :param:, 
           :return: and  :type: syntax. So, you need to be very careful to 
           specify the italic syntax for the argument name, put parentheses, put
           the : sign between the argument and its description
         - Only hardcoded section such as Parameters and Examples are accepted
           For instance, 'Your preferred section' needs to change the numpy 
           sphinx extension. Sensitive to typos obviously. **Examples** is 
           accepted but **Example** is not
         - buggy. After more than 30 minutes I could not make what I wanted. 
           Not documented
         - doctest complains about the underline text and therefore do not test 
           the inlined code
        
        Parameters
        ----------
        
        arg1 (int,float,...) : the first value
        arg2 (int,float,...) : the first value
        arg3 (int,float,...) : the first value
         
        Returns
        -------
        
        arg1/arg2 +arg3 : the output
        
        Warnings
        --------
        arg2 must be non-zero.      
        
        Examples
        --------

        >>> import template
        >>> a = MainClass3()
        >>> a.function1(1,1,1)
        2

        Notes
        -----
     
        Can be useful to emphasize 
        important feature


        See Also
        --------
            
            `MainClass1`
  
        Todo:
                        
            check that arg2 is non zero.
        """
        return arg1/arg2 + arg3

if __name__ == "__main__":
    import doctest
    doctest.testmod()
