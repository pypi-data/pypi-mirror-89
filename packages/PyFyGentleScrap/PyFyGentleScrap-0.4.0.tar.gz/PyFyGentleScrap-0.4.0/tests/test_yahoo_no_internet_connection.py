# coding: utf-8
# !/usr/bin/python3

import logging
import pytest
import pyfygentlescrap as pfgs
import re
import requests_mock
from pyfygentlescrap import InvalidResponseWarning, NoInternetWarning
from pyfygentlescrap.yahoo.yahoo_screener import yahoo_regions
from requests.exceptions import ConnectTimeout, ConnectionError, RequestException


class TestYahooFunctionsWithInternetDisconnected:
    exceptions = [ConnectTimeout, ConnectionError, RequestException]

    def setup_class(self):
        """ Setting logger to DEBUG mode."""
        logger = logging.getLogger("pyfygentlescrap")
        ch = logging.StreamHandler()
        fmt = logging.Formatter(
            "%(asctime)s %(name)s.%(module)s %(levelname)s: %(message)s",
            datefmt="%Y/%m/%d %I:%M:%S",
        )
        ch.setFormatter(fmt)
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)

    @pytest.mark.parametrize("request_error", exceptions)
    def test_yahoo_screener_belgium(self, request_error):
        # Belgium has approx 169 equities.
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, exc=request_error)
            with pytest.warns(NoInternetWarning):
                df = pfgs.yahoo_equity_screener(region="Belgium")
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, day",
        [
            ("^VIX", "2020/01/02"),
            ("^VIX", "2020/01/03"),
            ("^VIX", "2020/01/06"),
            ("^GSPC", "2020/01/06"),
        ],
    )
    @pytest.mark.parametrize("request_error", exceptions)
    def test_download_eod_data(self, ticker, day, request_error):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, exc=request_error)
            with pytest.warns(NoInternetWarning):
                df = pfgs.yahoo_historical_data(ticker, day, day)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, fromD, toD",
        [
            ("AAPL", "2020/11/06", "2020/11/02"),
            ("^VIX", "2020/01/03", "2020/01/01"),
        ],
    )
    @pytest.mark.parametrize("request_error", exceptions)
    def test_with_inverted_from_date_and_to_date(
        self, ticker, fromD, toD, request_error
    ):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, exc=request_error)
            with pytest.warns(NoInternetWarning):
                df = pfgs.yahoo_historical_data(
                    ticker=ticker, from_date=fromD, to_date=toD
                )
        assert len(df) == 0

    @pytest.mark.parametrize("ticker", ["^VIX", "^GSPC", "GC=F", "^FCHI", "AAPL"])
    @pytest.mark.parametrize("request_error", exceptions)
    def test_yahoo_ticker(self, ticker, request_error):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, exc=request_error)
            with pytest.warns(NoInternetWarning):
                result = pfgs.yahoo_ticker(ticker)
            assert len(result) == 0


# -------------------------------------------------------------------------------------
class TestYahooFunctionsWithInvalidResponse:
    @pytest.mark.parametrize("server_resp", ["resp", "{}", ""])
    def test_yahoo_screener_belgium(self, server_resp):
        # Belgium has approx 169 equities.
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, text=server_resp)
            with pytest.warns(InvalidResponseWarning):
                df = pfgs.yahoo_equity_screener(region="Belgium")
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, day",
        [
            ("^VIX", "2020/01/02"),
            ("^VIX", "2020/01/03"),
            ("^VIX", "2020/01/06"),
            ("^GSPC", "2020/01/06"),
        ],
    )
    @pytest.mark.parametrize("server_resp", ["resp", "{}", ""])
    def test_yahoo_historical_data(self, ticker, day, server_resp):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, text=server_resp)
            with pytest.warns(InvalidResponseWarning):
                df = pfgs.yahoo_historical_data(ticker, day, day)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, fromD, toD",
        [
            ("AAPL", "2020/11/06", "2020/11/02"),
            ("^VIX", "2020/01/03", "2020/01/01"),
        ],
    )
    @pytest.mark.parametrize("server_resp", ["resp", "{}", ""])
    def test_with_inverted_from_date_and_to_date(self, ticker, fromD, toD, server_resp):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, text=server_resp)
            with pytest.warns(InvalidResponseWarning):
                df = pfgs.yahoo_historical_data(
                    ticker=ticker, from_date=fromD, to_date=toD
                )
        assert len(df) == 0

    @pytest.mark.parametrize("ticker", ["^VIX", "^GSPC", "GC=F", "^FCHI", "AAPL"])
    @pytest.mark.parametrize("server_resp", ["resp", "{}", ""])
    def test_yahoo_ticker(self, ticker, server_resp):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, text=server_resp)
            with pytest.warns(InvalidResponseWarning):
                result = pfgs.yahoo_ticker(ticker)
            assert len(result) == 0

    @pytest.mark.parametrize("server_resp", ["resp", "{}", ""])
    def test_nb_equities_for_regions(self, server_resp):
        regions = list(yahoo_regions.keys())
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, text=server_resp)
            with pytest.warns(InvalidResponseWarning):
                result = pfgs.nb_equities_available(regions[0])
            assert result == 0


# -------------------------------------------------------------------------------------
class TestYahooFunctionsWithResponseCode400:
    responses = [
        'Bla Bla "CrumbStore":{"crumb":"CrumbXYZ"} Bla Bla',
        "Bla bla bla bla",
        "",
        None,
    ]
    status_codes = [400, 401, 403, 404, 408, 500, 502, 503]

    @pytest.mark.parametrize("ticker", ["^VIX", "^GSPC", "GC=F", "^FCHI", "AAPL"])
    @pytest.mark.parametrize("response", responses)
    @pytest.mark.parametrize("status_code", status_codes)
    def test_yahoo_ticker(self, ticker, response, status_code):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(
                requests_mock.ANY, matcher, text=response, status_code=status_code
            )
            with pytest.warns(InvalidResponseWarning):
                result = pfgs.yahoo_ticker(ticker)
            assert len(result) == 0

    @pytest.mark.parametrize("response", responses)
    @pytest.mark.parametrize("status_code", status_codes)
    def test_yahoo_screener_belgium(self, response, status_code):
        # Belgium has approx 169 equities.
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(
                requests_mock.ANY, matcher, text=response, status_code=status_code
            )
            with pytest.warns(InvalidResponseWarning):
                df = pfgs.yahoo_equity_screener(region="Belgium")
        assert len(df) == 0
