import os
import pytest


@pytest.fixture(autouse=True, scope='module')
def parent_directory():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(autouse=True, scope='module')
def data_directory(parent_directory):
    return os.path.join(parent_directory, "data")


@pytest.fixture(autouse=True, scope='module')
def model_data_directory(data_directory):
    return os.path.join(data_directory, "models")


@pytest.fixture(autouse=True, scope='module')
def asset_data_directory(data_directory):
    return os.path.join(data_directory, "assets")
