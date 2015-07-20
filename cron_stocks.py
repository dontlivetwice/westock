from utils.time import Time
import core.models.base as base
from yahoo_finance import Share


def main():
    # 1. get the time
    day = Time.get_utc_day()
    hours_mins = Time.get_utc_hours_minutes()

    # 1. Get all the list of stocks
    stocks = base.managers.stock_manager.get_many()

    # 2. go through stock and update the desired values
    for stock in stocks:
        ticker = stock.get('ticker')

        try:
            # 2.1 Get the info from the yahoo API
            updated_stock = Share(ticker)
        except:
            print "-->Failed to update: %s with Yahoo API" % ticker
            continue

        price = updated_stock.get_price()
        open = updated_stock.get_open()
        days_high = updated_stock.get_days_high()
        days_low = updated_stock.get_days_low()
        year_high = updated_stock.get_year_high()
        year_low = updated_stock.get_year_low()
        volume = updated_stock.get_volume()
        market_cap = updated_stock.get_market_cap()
        pe_ratio = updated_stock.get_price_earnings_ratio()
        div_yield = updated_stock.get_dividend_yield()
        change = updated_stock.get_change()
        change_percent = updated_stock.data_set.get('ChangeinPercent')

        # 2.2 Get the stock body
        stock_body = stock.get('body')

        stock_price = {hours_mins: price}

        if stock_body:
            # 1. Get the stock info for the day:
            stock_info = stock_body.get(day)

            if stock_info:
                stock_price = stock_info.get('price')
                stock_price.update({hours_mins: price})
        else:
            stock_body = {}

        # 2.2.4 update the stock info dict
        stock_info = {'price': stock_price}
        stock_info.update({'open': open})
        stock_info.update({'days_high': days_high})
        stock_info.update({'days_low': days_low})
        stock_info.update({'year_high': year_high})
        stock_info.update({'year_low': year_low})
        stock_info.update({'volume': volume})
        stock_info.update({'market_cap': market_cap})
        stock_info.update({'pe_ratio': pe_ratio})
        stock_info.update({'div_yield': div_yield})
        stock_info.update({'change': change})
        stock_info.update({'change_percent': change_percent})

        # update the stock body
        stock_body.update({day: stock_info})

        stock.body = stock_body

        # 3. update the stock in the DB
        try:
            base.managers.stock_manager.update_one(stock)
        except:
            print "-->Failed to update: %s in DB" % ticker
            continue


if __name__ == "__main__":
    main()
