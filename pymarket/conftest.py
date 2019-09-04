import numpy
import pandas
import pymarket
import pytest

pandas.set_option('display.max_rows', len(x))
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', 2000)
pandas.set_option('display.float_format', '{:20,.2f}'.format)
pandas.set_option('display.max_colwidth', -1)

@pytest.fixture(autouse=True)
def add_namespace(doctest_namespace):
        doctest_namespace['np'] = numpy
        doctest_namespace['pd'] = pandas
        doctest_namespace['pm'] = pymarket
