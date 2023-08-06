# coding: utf-8
# !/usr/bin/python3

import pytest
import pyfygentlescrap as pfgs
from pyfygentlescrap.yahoo.yahoo_screener import yahoo_regions
from pyfygentlescrap import InvalidRegionWarning, WrongTypeWarning


class TestNbEquitiesForRegions:
    def setup_class(self):
        self.session = pfgs.yahoo_session()

    @pytest.mark.parametrize("region", yahoo_regions)
    def test_nb_equities_for_regions(self, region):
        with pytest.warns(None) as record:
            self.session.nb_equities_available(region)
        assert len(record) == 0


def test_nb_equities_for_region_without_session():
    regions = list(yahoo_regions.keys())
    with pytest.warns(None) as record:
        pfgs.nb_equities_available(regions[0])
    assert len(record) == 0


def test_nb_equities_for_region_without_invalid_parameter():
    with pytest.warns(InvalidRegionWarning):
        pfgs.nb_equities_available("not_a_valid_region")


@pytest.mark.parametrize("invalid_region", [0, 1.0, True])
def test_nb_equities_for_region_without_wrong_type_parameter(invalid_region):
    with pytest.warns(WrongTypeWarning):
        pfgs.nb_equities_available(invalid_region)
