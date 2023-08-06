import pytest

import mincepy
from mincepy.testing import Car


def test_load(historian: mincepy.Historian):
    car = Car()
    car_id = historian.save(car)

    assert mincepy.load(car_id) is car

    # Check loading from 'cold'
    del car
    car = mincepy.load(car_id)
    assert car._historian == historian


def test_save(historian: mincepy.Historian):
    car = Car()
    mincepy.save(car)
    assert car._historian is historian


def test_invalid_connect():
    """Check we get the right error when attempting to connect to invalid archive"""
    with pytest.raises(mincepy.ConnectionError):
        mincepy.connect('mongodb://unknown-server/db')
