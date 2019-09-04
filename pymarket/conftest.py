import numpy
import pandas
import pymarket
import pytest

pandas.set_option('display.max_columns', None)

@pytest.fixture(autouse=True)
def add_namespace(doctest_namespace):
        doctest_namespace['np'] = numpy
        doctest_namespace['pd'] = pandas
        doctest_namespace['pm'] = pymarket
