# coding: utf-8
# !/usr/bin/python3

import logging
import pytest
import pyfygentlescrap as pfgs


class TestYahooFunctionsWITHSession:
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
        self.session = pfgs.yahoo_session()

    def test_session(self):
        assert len(self.session.crumb) > 0
        assert len(self.session.cookies) > 0

    def test_yahoo_screener_belgium(self):
        # Belgium has approx 169 equities.
        df = self.session.yahoo_equity_screener("Belgium")
        assert len(df) > 100

    @pytest.mark.parametrize(
        "region",
        [
            "not_a_valid_country",
            1,
            True,
        ],
    )
    def test_yahoo_screener_with_invalid_country(self, region):
        df = self.session.yahoo_equity_screener(region)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, day, op, hi, lo, cl",
        [
            ("^VIX", "2020/01/02", 13.46, 13.72, 12.42, 12.47),
            ("^VIX", "2020/01/03", 15.01, 16.20, 13.13, 14.02),
            ("^VIX", "2020/01/06", 15.45, 16.39, 13.54, 13.85),
            ("^GSPC", "2020/01/06", 3217.55, 3246.84, 3214.64, 3246.28),
        ],
    )
    def test_download_eod_data(self, ticker, day, op, hi, lo, cl):
        df = self.session.yahoo_historical_data(ticker, day, day)
        assert round(df.loc[day, "open"], 2) == op
        assert round(df.loc[day, "high"], 2) == hi
        assert round(df.loc[day, "low"], 2) == lo
        assert round(df.loc[day, "close"], 2) == cl

    @pytest.mark.parametrize(
        "ticker, day",
        [
            ("AAPL", "2020/11/06"),
            ("AAPL", "2020/05/08"),
            ("FP.PA", "2020/09/25"),
        ],
    )
    def test_download_dividend_data(self, ticker, day):
        df = pfgs.yahoo_historical_data(ticker=ticker, from_date=day, to_date=day)
        assert df.loc[day, "dividend"] > 0.0

    @pytest.mark.parametrize(
        "ticker, day, split",
        [
            ("AAPL", "2020/08/31", 4.0),
        ],
    )
    def test_download_split_data(self, ticker, day, split):
        df = pfgs.yahoo_historical_data(ticker=ticker, from_date=day, to_date=day)
        assert round(df.loc[day, "split"], 2) == split

    @pytest.mark.parametrize(
        "ticker, day",
        [
            ("not_a_valid_ticker", "2020/12/1"),
            (1, "2020/12/1"),
            (1.0, "2020/12/1"),
            (True, "2020/12/1"),
        ],
    )
    def test_historical_with_invalid_ticker(self, ticker, day):
        df = self.session.yahoo_historical_data(ticker, day, day)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, fromD, toD",
        [
            ("AAPL", "2020/01/01", "2020/01/01"),
            ("AAPL", "2020/12/05", "2020/12/06"),  # saturday+sunday -> no quotation
        ],
    )
    def test_valid_ticker_no_quotation_for_the_requested_day(self, ticker, fromD, toD):
        df = self.session.yahoo_historical_data(ticker, fromD, toD)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, fromD, toD, expected",
        [
            ("AAPL", "2020/11/06", "2020/11/02", 5),
            ("^VIX", "2020/01/03", "2020/01/01", 2),
        ],
    )
    def test_with_inverted_from_date_and_to_date(self, ticker, fromD, toD, expected):
        df = self.session.yahoo_historical_data(ticker, fromD, toD)
        assert len(df) == expected

    @pytest.mark.parametrize(
        "ticker, key, expected",
        [
            ("^VIX", "shortName", "CBOE Volatility Index"),
            ("^GSPC", "shortName", "S&P 500"),
            ("GC=F", "currency", "USD"),
            ("^FCHI", "shortName", "CAC 40"),
            ("^FCHI", "currency", "EUR"),
            ("^FCHI", "exchangeTimezoneShortName", "CET"),
            ("AAPL", "shortName", "Apple Inc."),
            ("AAPL", "longName", "Apple Inc."),
        ],
    )
    def test_yahoo_ticker(self, ticker, key, expected):
        result = self.session.yahoo_ticker(ticker)
        print(result.columns)
        print(result.loc[ticker, key])
        result = result.loc[ticker, key]
        assert result == expected

    @pytest.mark.parametrize(
        "ticker",
        ["not_a_valid_ticker", 1.0, True],
    )
    def test_yahoo_invalid_tickers(self, ticker):
        result = self.session.yahoo_ticker(ticker)
        assert len(result) == 0
