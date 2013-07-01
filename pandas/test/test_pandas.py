'''Test of pandas nodes''' 

import tempfile

from openalea.core.alea import *
from openalea.core.path import path
import pandas
import numpy as np

pm = PackageManager()
pm.init(verbose=False)

expected_df = pandas.read_csv(path('data/foo.csv'))

relative_tolerance = 10e-3
absolute_tolerance = 10e-3


def test_to_csv():
    tmp_filepath = tempfile.mkstemp()[1]
    res = run(('openalea.pandas.io', 'to_csv'), inputs={'dataframe': expected_df, 'path_or_buf': tmp_filepath, 'index': False}, pm=pm)
    df = pandas.read_csv(path(res[0]))
    np.testing.assert_allclose(df.values, expected_df.values, relative_tolerance, absolute_tolerance)
    path(tmp_filepath).remove()
    
    
def test_read_csv():
    res = run(('openalea.pandas.io', 'read_csv'), inputs={'filepath_or_buffer': 'data/foo.csv'}, pm=pm)
    np.testing.assert_allclose(res[0].values, expected_df.values, relative_tolerance, absolute_tolerance)
