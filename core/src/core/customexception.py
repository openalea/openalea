# -*- coding: utf-8 -*-

# This file is part of pyLot library.
#
# pyLot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyLot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyLot.  If not, see <http://www.gnu.org/licenses/>.

__author__ = u'Pierre Puiseux, Guillaume Baty'
__copyright__ = u"Copyright 2011-2012 (C) andheo, Université de Pau et des Pays de l'Adour"
__credits__ = [u'Pierre Puiseux', u'Guillaume Baty']
__license__ = "GNU Lesser General Public License"

__all__ = ['cast_error', 'display_error_color', 'CustomException', 'UserException']


def cast_error(error, klass, title=True, message=True, desc=True, **kargs):
    new_error = klass(**kargs)
    if isinstance(error, CustomException):
        new_error.title = new_error.title if title else error.title
        new_error.message = new_error.message if message else error.message
        new_error.desc = new_error.desc if desc else error.desc
    else:
        new_error.title = new_error.title if title else error.__class__.__name__
        new_error.message = new_error.message if message else error.message
        new_error.desc = new_error.desc if desc else error.message
    return new_error


def display_error_color(e):
    if not isinstance(e, CustomException):
        e = cast_error(e, CustomException)

    print '-' * len(e.getTitle())
    print e.getTitle()
    print '-' * len(e.getTitle())
    print
    print e.getMessage()
    desc = e.getDesc()
    if desc:
        part = u'Details:'
        print
        print part
        print '-' * len(part)
        print desc


class CustomException(Exception):
    u"""
    CustomException is an extension of builtin Exception.
    Goal is to provide an unique structure for all kind of exceptions to allow
    high-level exception handling.

    For this reason, CustomException always provides :
      - a title (getTitle)
      - a message (getMessage)
      - a detailed description (getDesc)

    Typicall use is :

    def print_error(error):
      "number of error arguments has no importance"
      print_in_red(error.getTitle())
      print_in_blue(error.getMessage())

    try :
      action
    except CustomExceptionNumberOne,error :
      print_error(error)
    except CustomExceptionNumberTwo,error :
      print_error(error)
    except CustomExceptionNumberThree,error :
      fix the problem
    # CustomExceptionNumberFour isn't intercepted here but for example in GUI classes
    else :
      print 'done'

    If CustomException takes one argument, you can reach it using "%(value)s".
    If it takes more than one, you must reimplement _kargs method.

    Example :

    .. code-block :: python

      class ErrNotMatchingPuzzlePiece(CustomException):
        title = u'Error: puzzle pieces do not match'
        message = u'%(compass_1)s part of piece %(piece_1)%s do not match %(compass_2)s part of piece %(piece_2)%s'
        desc = "This error is raised because ..."

        def _kargs(self):
          return dict(
            compass_1=unicode(self._args[0].num),
            piece_1=self._args[1],
            compass_2=unicode(self._args[2].num),
            piece_2=self._args[3],
            )

      #two raise this exception:
      raise ErrNotMatchingPuzzlePiece(p1, u'North', p2, u'South')
      # with p1 and p2 two "Piece" objects containing a "num" attribute.

    """
    title = u'Unknown Error'
    message = u'An unknown error occurs'
    desc = u'No details available'

    def __init__(self, *args, **kargs):
        self._args = args
        self.__kargs = kargs

    def kargs(self):
        self.__kargs.update(self._kargs())
        return self.__kargs

    def _kargs(self):
        try:
            return dict(value=self._args[0])
        except IndexError:
            return {}

    def rkargs(self):
        dic = {}
        for k, v in self.kargs():
            dic[k] = repr(v)
        return dic

    def getMessage(self):
        return self.message % self.kargs()

    def getTitle(self):
        return self.title % self.kargs()

    def getDesc(self):
        return self.desc % self.kargs()

    def __str__(self):
        return self.getMessage().encode('utf8')

    def __unicode__(self):
        return self.getMessage()


class UserException(CustomException):
    pass


class ErrorInvalidItemName(CustomException):
    title = u'Error: item name is not valid'
    message = u'%(name)r is not valid'
    desc = u"Item name must not be empty, contain punctuation (except '_')or non ascii character"

    def _kargs(self):
        return dict(
            project=self._args[0],
            category=self._args[1],
            name=self._args[2],
        )


class ErrorInvalidItem(CustomException):
    title = u'Error: item is invalid'
    message = u'Item is invalid: %(message)s'
    desc = u"Item is invalid"

    def _kargs(self):
        return dict(message=self._args[0])
