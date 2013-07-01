
# This file has been generated at Fri Jun 14 11:57:05 2013

from openalea.core import *


__name__ = 'openalea.pandas.io'

__editable__ = True
__description__ = 'Pandas wrapping.'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__alias__ = []
__version__ = '1.0.0'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD/INRA'
__icon__ = ''


__all__ = ['io_to_csv', 'io_read_csv']


io_to_csv = Factory(name='to_csv',
                authors='C. Chambon',
                description='Write a pandas.DataFrame into a comma-separated-values (CSV) file. Wrapping of pandas.DataFrame.to_csv.',
                category='data i/o',
                nodemodule='io',
                nodeclass='to_csv',
                inputs=[{'interface': None, 'name': 'dataframe', 'value': None, 'desc': 'The dataframe to write.', 'hide': False},
                        {'interface': IFileStr, 'name': 'path_or_buf', 'value': None, 'desc': 'File path.', 'hide': False, 'label': 'filepath'},
                        {'interface': IStr, 'name': 'sep', 'value': ',', 'desc': 'Field delimiter for the output file.', 'hide': True},
                        {'interface': IStr, 'name': 'na_rep', 'value': '', 'desc': 'Missing data representation.', 'hide': False},
                        {'interface': ISequence, 'name': 'cols', 'value': None, 'desc': 'Columns to write.', 'hide': True},
                        {'interface': IBool, 'name': 'header', 'value': True, 'desc': 'Write out column names.', 'hide': True},
                        {'interface': IBool, 'name': 'index', 'value': True, 'desc': 'Write row names (index).', 'hide': False},
                        {'interface': IInterface, 'name': 'index_label', 'value': None, 'desc': 'Can be either a string or a sequence of strings. If a string is given, then the string is the column label for index column(s) if desired. If None is given, and `header` and `index` are True, then the index names are used. A sequence should be given if the DataFrame uses MultiIndex.', 'hide': True},
                        {'interface': IStr, 'name': 'mode', 'value': 'w', 'desc': 'Python write mode.', 'hide': True},
                        {'interface': IStr, 'name': 'nanRep', 'value': None, 'desc': 'A string representation of a missing value.', 'hide': True},
                        {'interface': IStr, 'name': 'encoding', 'value': None, 'desc': 'A string representing the encoding to use if the contents are non-ascii, for python versions prior to 3.', 'hide': True}],
                outputs=[{'interface': IFileStr, 'name': 'filepath', 'desc': 'The path of the CSV file.'}]
               )


io_read_csv = Factory(name='read_csv',
                authors='C. Chambon',
                description='Read a CSV (comma-separated-values) file into a pandas.DataFrame. Wrapping of pandas.read_csv.',
                category='data i/o',
                nodemodule='io',
                nodeclass='read_csv',
                inputs=[{'interface': IFileStr, 'name': 'filepath_or_buffer', 'value': None, 'desc': 'The path of the CSV file to read.', 'hide': False, 'label': 'filepath'},
                        {'interface': IStr, 'name': 'sep', 'value': ',', 'desc': 'Delimiter to use. If sep is None, will try to automatically determine this.', 'hide': True},
                        {'interface': IInt, 'name': 'header', 'value': 0, 'desc': 'Row to use for the column labels of the parsed DataFrame.', 'hide': True},
                        {'interface': IInterface, 'name': 'index_col', 'value': None, 'desc': 'Can be either an integer or a sequence. If an integer is given, then it represents the index of the column to use as the row labels of the DataFrame. If a sequence is given, then a MultiIndex is used.', 'hide': True},
                        {'interface': ISequence, 'name': 'names', 'value': None, 'desc': ' List of column names.', 'hide': True},
                        {'interface': IInterface, 'name': 'skiprows', 'value': None, 'desc': 'Can be either an integer or a sequence of integers. If an integer is given, then it represents the number of rows to skip. If a sequence is given, then it represents the row numbers to skip (0-indexed).', 'hide': True},
                        {'interface': IInterface, 'name': 'na_values', 'value': None, 'desc': 'Additional strings to recognize as NA/NaN. Can be either a sequence or a dict. If dict passed, specific per-column NA values.', 'hide': True},
                        {'interface': IBool, 'name': 'parse_dates', 'value': False, 'desc': 'Attempt to parse dates in the index column(s).', 'hide': True},
                        {'interface': IInterface, 'name': 'date_parser', 'value': None, 'desc': 'Function to use for converting dates to strings. If None, defaults to dateutil.parser.', 'hide': True},
                        {'interface': IInt, 'name': 'nrows', 'value': None, 'desc': 'Number of rows of file to read. Useful for reading pieces of large files.', 'hide': True},
                        {'interface': IBool, 'name': 'iterator', 'value': False, 'desc': 'Return TextParser object.', 'hide': True},
                        {'interface': IInt, 'name': 'chunksize', 'value': None, 'desc': 'Return TextParser object for iteration.', 'hide': True},
                        {'interface': IInt, 'name': 'skip_footer', 'value': 0, 'desc': 'Number of line at bottom of file to skip.', 'hide': True},
                        {'interface': IDict, 'name': 'converters', 'value': None, 'desc': 'Dict of functions for converting values in certain columns. Keys can either be integers or column labels.', 'hide': True},
                        {'interface': IBool, 'name': 'verbose', 'value': False, 'desc': 'Indicate number of NA values placed in non-numeric columns.', 'hide': True},
                        {'interface': IStr, 'name': 'delimiter', 'value': None, 'desc': 'Alternative argument name for sep.', 'hide': True},
                        {'interface': IStr, 'name': 'encoding', 'value': None, 'desc': 'Encoding to use for UTF when reading/writing (ex. "utf-8").', 'hide': True}],
                outputs=[{'interface': IInterface, 'name': 'dataframe', 'desc': 'The dataframe created from the CSV file.'}]
               )




