# coding: utf-8
# !/usr/bin/python3

import pytest
import pyfygentlescrap as pfgs
from pyfygentlescrap import (
    InvalidParameterWarning,
    InvalidRegionWarning,
    InvalidResponseWarning,
    WrongTypeWarning,
)


class TestYahooFunctionsWITHSession:
    def setup_class(self):
        self.session = pfgs.yahoo_session()

    def test_session(self):
        assert len(self.session.crumb) > 0
        assert len(self.session.cookies) > 0

    @pytest.mark.filterwarnings("ignore:")
    def test_screener_belgium(self):
        # Belgium has approx 169 equities.
        df = self.session.yahoo_equity_screener("Belgium")
        assert len(df) > 140

    @pytest.mark.parametrize("region", [1.0, 1, True, None, ["ctry1", "ctry12"]])
    def test_screener_with_wrong_type_country(self, region):
        with pytest.warns(WrongTypeWarning):
            df = self.session.yahoo_equity_screener(region)
        assert len(df) == 0

    def test_screener_with_invalid_country(self):
        with pytest.warns(InvalidRegionWarning):
            df = self.session.yahoo_equity_screener("not_valid_ctry")
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, day, op, hi, lo, cl",
        [
            ("^VIX", "2020/01/02", 13.46, 13.72, 12.42, 12.47),
            ("^VIX", "2020-01-02", 13.46, 13.72, 12.42, 12.47),
            ("^VIX", "2020/01/03", 15.01, 16.20, 13.13, 14.02),
            ("^VIX", "2020/01/06", 15.45, 16.39, 13.54, 13.85),
            ("^GSPC", "2020/01/06", 3217.55, 3246.84, 3214.64, 3246.28),
        ],
    )
    def test_historcial_eod_data(self, ticker, day, op, hi, lo, cl):
        df = self.session.yahoo_historical_data(ticker, day, day)
        assert round(df.loc[day, "open"], 2) == op
        assert round(df.loc[day, "high"], 2) == hi
        assert round(df.loc[day, "low"], 2) == lo
        assert round(df.loc[day, "close"], 2) == cl

    @pytest.mark.parametrize(
        "ticker, day",
        [("AAPL", "2020/11/06"), ("AAPL", "2020/05/08"), ("FP.PA", "2020/09/25")],
    )
    def test_historcial_dividend_data(self, ticker, day):
        df = self.session.yahoo_historical_data(
            ticker=ticker, from_date=day, to_date=day
        )
        assert df.loc[day, "dividend"] > 0.0

    @pytest.mark.parametrize("ticker, day, split", [("AAPL", "2020/08/31", 4.0)])
    def test_historcial_split_data(self, ticker, day, split):
        df = self.session.yahoo_historical_data(
            ticker=ticker, from_date=day, to_date=day
        )
        assert round(df.loc[day, "split"], 2) == split

    @pytest.mark.parametrize("ticker", [1, 1.0, True, None])
    def test_historical_with_wrong_type_ticker(self, ticker):
        day = "2020-12-05"
        with pytest.warns(WrongTypeWarning):
            df = self.session.yahoo_historical_data(
                ticker=ticker, from_date=day, to_date=day
            )
        assert len(df) == 0

    def test_historical_with_invalid_ticker(self):
        day = "2020-12-05"
        with pytest.warns(InvalidResponseWarning):
            df = self.session.yahoo_historical_data(
                ticker="not_a_valid_ticker", from_date=day, to_date=day
            )
        assert len(df) == 0

    @pytest.mark.parametrize(
        "date", [True, None, "22200/01/01", "no_valid_date", "2020/01/32"]
    )
    def test_historical_with_invalid_dates(self, date):
        with pytest.warns(InvalidParameterWarning):
            df = self.session.yahoo_historical_data(
                ticker="AAPL", from_date=date, to_date=date
            )
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, fromD, toD",
        [("AAPL", "2020/01/01", "2020/01/01"), ("AAPL", "2020/12/05", "2020/12/06")],
    )
    def test_historcial_valid_ticker_no_quotation_for_day(self, ticker, fromD, toD):
        with pytest.warns(InvalidResponseWarning):
            df = self.session.yahoo_historical_data(ticker, fromD, toD)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, fromD, toD, expected",
        [
            ("AAPL", "2020/11/06", "2020/11/02", 5),
            ("^VIX", "2020/01/03", "2020/01/01", 2),
        ],
    )
    def test_historcial_inverted_from_to_date(self, ticker, fromD, toD, expected):
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
    def test_ticker_simple(self, ticker, key, expected):
        result = self.session.yahoo_ticker(ticker)
        result = result.loc[ticker, key]
        assert result == expected

    @pytest.mark.parametrize("ticker", [1, 1.0, True, None, ["AAPL", "TSLA"]])
    def test_ticker_wrong_type_tickers(self, ticker):
        with pytest.warns(WrongTypeWarning):
            result = self.session.yahoo_ticker(ticker)
        assert len(result) == 0

    def test_ticker_invalid_tickers(self):
        with pytest.warns(InvalidResponseWarning):
            result = self.session.yahoo_ticker("not_a_valid_ticker")
        assert len(result) == 0
