# coding: utf-8
# !/usr/bin/python3

import pytest
import pyfygentlescrap as pfgs
import re
import requests_mock
from pyfygentlescrap import InvalidResponseWarning, MarketOpenWarning
from requests.exceptions import ConnectionError


def _response(ticker="AAPL", marketState="REGULAR"):
    return (
        """
    {"finance":{
    "result":[{
      "start":0,
      "count":25,
      "total":1,
      "quotes":
      [{
        "symbol":"""
        + f'"{ticker}",'
        + """
        "regularMarketDayHigh":{"raw":134.405,"fmt":"134.40"},
        "marketCap":{"raw":2242197323776,"fmt":"2.242T","longFmt":"2,242,197,323,776"},
        "regularMarketVolume":{"raw":165746075,"fmt":"165.746M","longFmt":"165,746,075"},
        "regularMarketDayLow":{"raw":129.655,"fmt":"129.65"},
        "shortName":"Apple Inc.",
        "financialCurrency":"USD",
        "displayName":"Apple",
        "regularMarketOpen":{"raw":131.61,"fmt":"131.61"},
        "regularMarketTime":{"raw":1608670801,"fmt":"4:00PM EST"},
        "quoteType":"EQUITY",
        "currency":"USD",
        "regularMarketPreviousClose":{"raw":128.23,"fmt":"128.23"},
        "regularMarketPrice":{"raw":131.88,"fmt":"131.88"},
        "marketState":"""
        + f'"{marketState}",'
        + """
        "longName":"Apple Inc."
      }]
    }],
    "error":null}}"""
    )


def test_yahoo_market_open():
    with requests_mock.Mocker() as mock:
        matcher = re.compile(".*query.*")
        mock.register_uri(
            requests_mock.ANY, matcher, text=_response(marketState="REGULAR")
        )
        matcher = re.compile(".*//finance.yahoo.com.*")
        mock.register_uri(
            requests_mock.ANY,
            matcher,
            text='Bla Bla "CrumbStore":{"crumb":"CrumbXYZ"} Bla Bla',
        )
        with pytest.warns(MarketOpenWarning):
            pfgs.yahoo_equity_screener(region="United States")


@pytest.mark.parametrize("marketState", ["POSTPOST", "PREPRE", "CLOSED"])
def test_yahoo_market_not_open(marketState):
    with requests_mock.Mocker() as mock:
        matcher = re.compile(".*query.*")
        mock.register_uri(
            requests_mock.ANY, matcher, text=_response(marketState=marketState)
        )
        matcher = re.compile(".*//finance.yahoo.com.*")
        mock.register_uri(
            requests_mock.ANY,
            matcher,
            text='Bla Bla "CrumbStore":{"crumb":"CrumbXYZ"} Bla Bla',
        )
        df = pfgs.yahoo_equity_screener(region="United States")
        assert len(df) == 1


@pytest.mark.parametrize(
    "server_down, server_up",
    [(".*query1.*", ".*query2.*"), (".*query2.*", ".*query1.*")],
)
def test_server_query_down(server_down, server_up):
    with requests_mock.Mocker() as mock:
        matcher = re.compile(server_down)
        mock.register_uri(requests_mock.ANY, matcher, exc=ConnectionError)
        matcher = re.compile(server_up)
        mock.register_uri(
            requests_mock.ANY, matcher, text=_response(marketState="CLOSED")
        )
        matcher = re.compile(".*//finance.yahoo.com.*")
        mock.register_uri(
            requests_mock.ANY,
            matcher,
            text='Bla Bla "CrumbStore":{"crumb":"CrumbXYZ"} Bla Bla',
        )
        pfgs.yahoo_equity_screener(region="United States")


def test_servers_query1_and_query2_down():
    with requests_mock.Mocker() as mock:
        matcher = re.compile(".*query.*")
        mock.register_uri(requests_mock.ANY, matcher, exc=ConnectionError)
        matcher = re.compile(".*//finance.yahoo.com.*")
        mock.register_uri(
            requests_mock.ANY,
            matcher,
            text='Bla Bla "CrumbStore":{"crumb":"CrumbXYZ"} Bla Bla',
        )
        with pytest.warns(InvalidResponseWarning):
            result = pfgs.yahoo_equity_screener(region="United States")
        assert len(result) == 0
