import core.models.base as base
from yahoo_finance import Share

from core.models.stock import Stock
from core.models.interest import Interest


def main():
    stock_list = [
        {"AAPL": "Technology"},
        {"TSLA": "Technology"},
        {"AMZN": "Technology"},
        {"INTC": "Technology"},
        {"COP": "Energy"},
        {"TM": "Industrials"},
        {"BIDU": "Technology"},
        {"ORCL": "Technology"},
        {"MU": "Technology"},
        {"FEYE": "Technology"},
        {"TOL": "Industrials"},
        {"C": "Financials"},
        {"MA": "Financials"},
        {"EBAY": "Technology"},
        {"CRM": "Technology"},
        {"KONA": "Services"},
        {"SNY": "Health"},
        {"CMG": "Services"},
        {"YHOO": "Technology"},
        {"YY": "Technology"},
        {"PNRA": "Services"},
        {"GOOGL": "Technology"},
        {"BBBY": "Services"},
        {"GOOG": "Technology"},
        {"KO": "Consumer"},
        {"TRIP": "Technology"},
        {"PBR": "Energy"},
        {"PG": "Consumer"},
        {"SDRL": "Energy"},
        {"GT": "Industrials"},
        {"ILF": "Energy"},
        {"YELP": "Technology"},
        {"WBA": "Consumer"},
        {"ECYT": "Health"},
        {"IBM": "Technology"},
        {"BA": "Industrials"},
        {"VZ": "Communications"},
        {"GE": "Energy"},
        {"MDLZ": "Consumer"},
        {"CAT": "Industrials"},
        {"UPS": "Services"},
        {"T": "Communications"},
        {"QCOM": "Technology"},
        {"DDD": "Technology"},
        {"SIEGY": "Technology"},
        {"CSCO": "Technology"},
        {"LNKD": "Technology"},
        {"MNK": "Health"},
        {"FB": "Technology"},
        {"NKTR": "Health"},
        {"HTZ": "Services"},
    ]

    for stock in stock_list:
        # 1. validate stock ticker with yahoo finance API
        key = stock.keys()[0]
        value = stock.values()[0]

        share = Share(key.upper())

        name = share.data_set.get('Name')
        symbol = share.data_set.get('Symbol')
        currency = share.data_set.get('Currency')

        if name and currency:
            interest = base.managers.interest_manager.get_one(name=value)

            if not interest:
                interest = Interest(name=value, image_url="/static/images/%s.png" % value)
                base.managers.interest_manager.add_one(interest)
                interest = base.managers.interest_manager.get_one(name=value)

            stock = Stock(ticker=symbol, name=name, interest_id=interest.get('id'))
            try:
                base.managers.stock_manager.add_one(stock)
            except:
                pass

if __name__ == "__main__":
    main()
