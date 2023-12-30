# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Data display component tests fixtures."""
from typing import List

import pandas as pd
import pytest

import nextpy as xt
from nextpy.backend.state import BaseState


@pytest.fixture
def data_table_state(request):
    """Get a data table state.

    Args:
        request: The request.

    Returns:
        The data table state class.
    """

    class DataTableState(BaseState):
        data = request.param["data"]
        columns = ["column1", "column2"]

    return DataTableState


@pytest.fixture
def data_table_state2():
    """Get a data table state.

    Returns:
        The data table state class.
    """

    class DataTableState(BaseState):
        _data = pd.DataFrame()

        @xt.var
        def data(self):
            return self._data

    return DataTableState


@pytest.fixture
def data_table_state3():
    """Get a data table state.

    Returns:
        The data table state class.
    """

    class DataTableState(BaseState):
        _data: List = []
        _columns: List = ["col1", "col2"]

        @xt.var
        def data(self) -> List:
            return self._data

        @xt.var
        def columns(self):
            return self._columns

    return DataTableState


@pytest.fixture
def data_table_state4():
    """Get a data table state.

    Returns:
        The data table state class.
    """

    class DataTableState(BaseState):
        _data: List = []
        _columns: List = ["col1", "col2"]

        @xt.var
        def data(self):
            return self._data

        @xt.var
        def columns(self) -> List:
            return self._columns

    return DataTableState
