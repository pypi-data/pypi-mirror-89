"""Ticker utilities for getting tickers.

Information available at http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs

Field Name          Definition
==============================
Symbol	            The one to four or five character identifier for each NASDAQ-listed security.
------------------------------
Security Name	    Company issuing the security.
------------------------------
Market Category	    The category assigned to the issue by NASDAQ based on Listing Requirements. Values:
                    Q = NASDAQ Global Select MarketSM
                    G = NASDAQ Global MarketSM
                    S = NASDAQ Capital Market
------------------------------
Test Issue	        Indicates whether or not the security is a test security.
                    Y = yes, it is a test issue.
                    N = no, it is not a test issue.
------------------------------
Financial Status	Indicates when an issuer has failed to submit its regulatory filings on a timely basis,
                    has failed to meet NASDAQ's continuing listing standards, and/or has filed for bankruptcy.
                    Values include:

                    D = Deficient: Issuer Failed to Meet NASDAQ Continued Listing Requirements
                    E = Delinquent: Issuer Missed Regulatory Filing Deadline
                    Q = Bankrupt: Issuer Has Filed for Bankruptcy
                    N = Normal (Default): Issuer Is NOT Deficient, Delinquent, or Bankrupt.
                    G = Deficient and Bankrupt
                    H = Deficient and Delinquent
                    J = Delinquent and Bankrupt
                    K = Deficient, Delinquent, and Bankrupt
------------------------------
Round Lot	        Indicates the number of shares that make up a round lot for the given security.
------------------------------
File Creation Time  The last row of each Symbol Directory text file contains a timestamp that reports the File
                    Creation Time. The file creation time is based on when NASDAQ Trader generates the file and
                    can be used to determine the timeliness of the associated data. The row contains the words
                    File Creation Time followed by mmddyyyyhhmm as the first field, followed by all delimiters
                    to round out the row. An example: File Creation Time: 1217200717:03

"""

import csv
import logging
import os
from configparser import SectionProxy
from ftplib import FTP
from typing import Iterator

from pystonkslib.config import get_config, get_config_folder

LOGGER = logging.getLogger(__name__)


def get_stock_symbols_file(update: bool = False) -> str:
    """Get the stock symbols file for nyse listed."""
    config = get_config()
    symbol_info = config["symbol_info"]
    config_folder = get_config_folder()
    symbol_file_location: str = os.path.join(config_folder, symbol_info["filename"])

    if not os.path.exists(symbol_file_location):
        download_stock_symbols(symbol_info, symbol_file_location)

    if update:
        LOGGER.info("Updating stock symbols by request.")
        download_stock_symbols(symbol_info, symbol_file_location)

    LOGGER.info("Stock symbols available in %s", symbol_file_location)
    return symbol_file_location


def download_stock_symbols(symbol_info: SectionProxy, symbol_file_location: str) -> None:
    """Download stock symbols file."""

    LOGGER.info("Downloading symbol info.")
    ftp = FTP(symbol_info["url"])
    ftp.login()
    ftp.cwd(symbol_info["directory"])
    LOGGER.info("Starting FTP transfer of symbol info.")
    with open(symbol_file_location, "wb") as filepath:
        ftp.retrbinary(f"RETR {symbol_info['filename']}", filepath.write)
    LOGGER.info("Finished FTP transfer of symbol info.")


def get_ticker_iterator(stock_symbols_file: str) -> Iterator:
    """Return an iterator of the stock symbols file."""

    csv.register_dialect("nyse_ticker", delimiter="|", quoting=csv.QUOTE_NONE)
    with open(stock_symbols_file, newline="") as symbol_file_obj:
        reader = csv.reader(symbol_file_obj, "nyse_ticker")
        header = []

        # Iterate through shite - there's probably a better way to pull the first row
        # out without using a csv reader, but this is efficient and optimized in other
        # ways for reading the file, so until it's a problem it's probably not worth
        # focusing on.
        for row_index, row in enumerate(reader):
            if row_index == 0:
                header = row
                continue
            obj = {}

            # Use our header to determine our keys for our values.
            for obj_index, item in enumerate(row):
                key = header[obj_index]
                obj[key] = item
            yield obj


def get_valid_tickers() -> list:
    """Get valid tickers based on some sane filters."""

    valid_tickers = []

    stock_symbols_file = get_stock_symbols_file()

    ticker_iterator = get_ticker_iterator(stock_symbols_file)
    last_index = 0
    for index, ticker in enumerate(ticker_iterator):
        # We don't want to care about financial statuses that aren't in good standing.
        if ticker.get("Financial Status") != "N":
            continue
        # We don't want to care about test issues.
        if ticker.get("Test Issue") == "Y":
            continue
        last_index = index
        valid_tickers.append(ticker)
    LOGGER.info("Found %s valid tickers out of %s", len(valid_tickers), last_index)
    return valid_tickers
