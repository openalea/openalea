# -*- python -*-
#
#       math : pandas package
#
#       Copyright 2006 - 2010 INRIA - CIRAD - INRA  
#
#       File author(s): Camille CHAMBON <camille.chambon@grignon.inra.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import pandas


def to_csv(dataframe, path_or_buf, sep=',', na_rep='', cols=None, header=True, index=True, index_label=None, mode='w', nanRep=None, encoding=None):
    '''
    Wrapping of :meth:`pandas.DataFrame.to_csv`.
    .. seealso:: `pandas.DataFrame.to_csv documentation <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html>`_.
    '''
    dataframe.to_csv(path_or_buf=path_or_buf, sep=sep, na_rep=na_rep, cols=cols, header=header, index=index, index_label=index_label, mode=mode, nanRep=nanRep, encoding=encoding)
    return path_or_buf


def read_csv(filepath_or_buffer, sep=',', header=0, index_col=None, names=None, skiprows=None, na_values=None, parse_dates=False, date_parser=None, nrows=None, iterator=False, chunksize=None, skip_footer=0, converters=None, verbose=False, delimiter=None, encoding=None):
    ''' 
    Wrapping of :func:`pandas.read_csv`.
    .. seealso:: `pandas.read_csv documentation <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.io.parsers.read_csv.html>`_.
    '''
    return pandas.read_csv(filepath_or_buffer=filepath_or_buffer, sep=sep, header=header, index_col=index_col, names=names, skiprows=skiprows, na_values=na_values, parse_dates=parse_dates, date_parser=date_parser, nrows=nrows, iterator=iterator, chunksize=chunksize, skip_footer=skip_footer, converters=converters, verbose=verbose, delimiter=delimiter, encoding=encoding)
