# -*- coding: utf-8 -*-
import pandas as pd
from functools import wraps
from ..common import (
    _expire,
    _TIMEFRAME_CHART,
    _getJson,
    _raiseIfNotStr,
    PyEXception,
    _strOrDate,
    _reindex,
    _toDatetime,
    _EST,
    json_normalize,
    _quoteSymbols,
)


def book(symbol, token="", version="", filter=""):
    """Book data

    https://iextrading.com/developer/docs/#book
    realtime during Investors Exchange market hours

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/book", token, version, filter)


def _bookToDF(b):
    """internal"""
    quote = b.get("quote", [])
    asks = b.get("asks", [])
    bids = b.get("bids", [])
    trades = b.get("trades", [])

    df1 = json_normalize(quote)
    df1["type"] = "quote"

    df2 = json_normalize(asks)
    df2["symbol"] = quote["symbol"]
    df2["type"] = "ask"

    df3 = json_normalize(bids)
    df3["symbol"] = quote["symbol"]
    df3["type"] = "bid"

    df4 = json_normalize(trades)
    df4["symbol"] = quote["symbol"]
    df3["type"] = "trade"

    df = pd.concat([df1, df2, df3, df4], sort=True)
    _toDatetime(df)
    return df


@wraps(book)
def bookDF(symbol, token="", version="", filter=""):
    x = book(symbol, token, version, filter)
    df = _bookToDF(x)
    return df


@_expire(hour=4, tz=_EST)
def chart(symbol, timeframe="1m", date=None, token="", version="", filter=""):
    """Historical price/volume data, daily and intraday

    https://iexcloud.io/docs/api/#historical-prices
    Data Schedule
    1d: -9:30-4pm ET Mon-Fri on regular market trading days
        -9:30-1pm ET on early close trading days
    All others:
        -Prior trading day available after 4am ET Tue-Sat

    Args:
        symbol (str): Ticker to request
        timeframe (str): Timeframe to request e.g. 1m
        date (datetime): date, if requesting intraday
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    if timeframe is not None and timeframe != "1d":
        if timeframe not in _TIMEFRAME_CHART:
            raise PyEXception("Range must be in {}".format(_TIMEFRAME_CHART))
        return _getJson(
            "stock/{}/chart/{}".format(symbol, timeframe), token, version, filter
        )
    elif timeframe == "1d":
        if date:
            date = _strOrDate(date)
            return _getJson(
                "stock/{}/intraday-prices?exactDate={}".format(symbol, date),
                token,
                version,
                filter,
            )
        return _getJson(
            "stock/{}/intraday-prices".format(symbol), token, version, filter
        )

    if date:
        date = _strOrDate(date)
        return _getJson(
            "stock/{}/chart/date/{}".format(symbol, date), token, version, filter
        )
    return _getJson("stock/{}/chart".format(symbol), token, version, filter)


def _chartToDF(c):
    """internal"""
    df = pd.DataFrame(c)
    _toDatetime(df)
    _reindex(df, "date")
    return df


@wraps(chart)
def chartDF(symbol, timeframe="1m", date=None, token="", version="", filter=""):
    c = chart(symbol, timeframe, date, token, version, filter)
    df = pd.DataFrame(c)
    _toDatetime(df)
    if timeframe is not None and timeframe != "1d":
        _reindex(df, "date")
    else:
        if not df.empty:
            df.set_index(["date", "minute"], inplace=True)
        else:
            return pd.DataFrame()
    return df


@_expire(second=0)
def delayedQuote(symbol, token="", version="", filter=""):
    """This returns the 15 minute delayed market quote.

    https://iexcloud.io/docs/api/#delayed-quote
    15min delayed
    4:30am - 8pm ET M-F when market is open

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/delayed-quote", token, version, filter)


@wraps(delayedQuote)
def delayedQuoteDF(symbol, token="", version="", filter=""):
    df = json_normalize(delayedQuote(symbol, token, version, filter))
    _toDatetime(df)
    _reindex(df, "symbol")
    return df


def intraday(symbol, date="", token="", version="", filter=""):
    """This endpoint will return aggregated intraday prices in one minute buckets

    https://iexcloud.io/docs/api/#intraday-prices
    9:30-4pm ET Mon-Fri on regular market trading days
    9:30-1pm ET on early close trading days


    Args:
        symbol (str): Ticker to request
        date (str): Formatted as YYYYMMDD. This can be used for batch calls when range is 1d or date. Currently supporting trailing 30 calendar days of minute bar data.
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    if date:
        date = _strOrDate(date)
        return _getJson(
            "stock/{}/intraday-prices?exactDate={}".format(symbol, date),
            token,
            version,
            filter,
        )
    return _getJson("stock/{}/intraday-prices".format(symbol), token, version, filter)


@wraps(intraday)
def intradayDF(symbol, date="", token="", version="", filter=""):
    val = intraday(symbol, date, token, version, filter)
    df = pd.DataFrame(val)
    _toDatetime(df)
    df.set_index(["date", "minute"], inplace=True)
    return df


def largestTrades(symbol, token="", version="", filter=""):
    """This returns 15 minute delayed, last sale eligible trades.

    https://iexcloud.io/docs/api/#largest-trades
    9:30-4pm ET M-F during regular market hours

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/largest-trades", token, version, filter)


@wraps(largestTrades)
def largestTradesDF(symbol, token="", version="", filter=""):
    df = pd.DataFrame(largestTrades(symbol, token, version, filter))
    _toDatetime(df)
    _reindex(df, "time")
    return df


def ohlc(symbol, token="", version="", filter=""):
    """Returns the official open and close for a give symbol.

    https://iexcloud.io/docs/api/#news
    9:30am-5pm ET Mon-Fri

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/ohlc", token, version, filter)


@wraps(ohlc)
def ohlcDF(symbol, token="", version="", filter=""):
    o = ohlc(symbol, token, version, filter)
    if o:
        df = json_normalize(o)
        _toDatetime(df)
    else:
        df = pd.DataFrame()
    return df


@_expire(hour=4, tz=_EST)
def yesterday(symbol, token="", version="", filter=""):
    """This returns previous day adjusted price data for one or more stocks

    https://iexcloud.io/docs/api/#previous-day-prices
    Available after 4am ET Tue-Sat

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/previous", token, version, filter)


@wraps(yesterday)
def yesterdayDF(symbol, token="", version="", filter=""):
    y = yesterday(symbol, token, version, filter)
    if y:
        df = json_normalize(y)
        _toDatetime(df)
        _reindex(df, "symbol")
    else:
        df = pd.DataFrame()
    return df


def price(symbol, token="", version="", filter=""):
    """Price of ticker

    https://iexcloud.io/docs/api/#price
    4:30am-8pm ET Mon-Fri

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/price", token, version, filter)


@wraps(price)
def priceDF(symbol, token="", version="", filter=""):
    df = json_normalize({"price": price(symbol, token, version, filter)})
    _toDatetime(df)
    return df


def quote(symbol, token="", version="", filter=""):
    """Get quote for ticker

    https://iexcloud.io/docs/api/#quote
    4:30am-8pm ET Mon-Fri


    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/quote", token, version, filter)


@wraps(quote)
def quoteDF(symbol, token="", version="", filter=""):
    q = quote(symbol, token, version, filter)
    if q:
        df = json_normalize(q)
        _toDatetime(df)
        _reindex(df, "symbol")
    else:
        df = pd.DataFrame()
    return df


@_expire(hour=8, tz=_EST)
def spread(symbol, token="", version="", filter=""):
    """This returns an array of effective spread, eligible volume, and price improvement of a stock, by market.
    Unlike volume-by-venue, this will only return a venue if effective spread is not ‘N/A’. Values are sorted in descending order by effectiveSpread.
    Lower effectiveSpread and higher priceImprovement values are generally considered optimal.

    Effective spread is designed to measure marketable orders executed in relation to the market center’s
    quoted spread and takes into account hidden and midpoint liquidity available at each market center.
    Effective Spread is calculated by using eligible trade prices recorded to the consolidated tape and
    comparing those trade prices to the National Best Bid and Offer (“NBBO”) at the time of the execution.

    View the data disclaimer at the bottom of the stocks app for more information about how these values are calculated.


    https://iexcloud.io/docs/api/#earnings-today
    8am ET M-F

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/effective-spread", token, version, filter)


@wraps(spread)
def spreadDF(symbol, token="", version="", filter=""):
    df = pd.DataFrame(spread(symbol, token, version, filter))
    _toDatetime(df)
    _reindex(df, "venue")
    return df


def volumeByVenue(symbol, token="", version="", filter=""):
    """This returns 15 minute delayed and 30 day average consolidated volume percentage of a stock, by market.
    This call will always return 13 values, and will be sorted in ascending order by current day trading volume percentage.

    https://iexcloud.io/docs/api/#volume-by-venue
    Updated during regular market hours 9:30am-4pm ET


    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/volume-by-venue", token, version, filter)


@wraps(volumeByVenue)
def volumeByVenueDF(symbol, token="", version="", filter=""):
    df = pd.DataFrame(volumeByVenue(symbol, token, version, filter))
    _toDatetime(df)
    _reindex(df, "venue")
    return df
