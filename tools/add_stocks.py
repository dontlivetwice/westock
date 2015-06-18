import core.models.base as base
from yahoo_finance import Share

from core.models.stock import Stock


def main():
    stock_list = [
    "AAPL",
    "TSLA",
    "AMZN",
    "INTC",
    "COP",
    "TM",
    "BIDU",
    "ORCL",
    "MU",
    "FEYE",
    "TOL",
    "C",
    "MA",
    "EBAY",
    "CRM",
    "KONA",
    "SNY",
    "CMG",
    "YHOO",
    "YY",
    "PNRA",
    "GOOGL",
    "BBBY",
    "GOOG",
    "KO",
    "TRIP",
    "PBR",
    "PG",
    "SDRL",
    "GT",
    "ILF",
    "YELP",
    "WBA",
    "ECYT",
    "IBM",
    "BA",
    "VZ",
    "GE",
    "MDLZ",
    "CAT",
    "UPS",
    "T",
    "QCOM",
    "DDD",
    "SIEGY",
    "CSCO",
    "LNKD",
    "MNK",
    "FB",
    "NKTR",
    "HTZ"
    ]

    for ticker in stock_list:
        # 1. validate stock ticker with yahoo finance API
        share = Share(ticker.upper())

        name = share.data_set.get('Name')
        symbol = share.data_set.get('Symbol')
        currency = share.data_set.get('Currency')

        if name and currency:
            stock = Stock(ticker=symbol, name=name)
            base.managers.stock_manager.add_one(stock)

if __name__ == "__main__":
    main()
