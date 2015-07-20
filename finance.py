import re
import urllib2
from BeautifulSoup import BeautifulSoup
import HTMLParser

from settings import prod
from utils.time import Time
from optparse import OptionParser
from core.models.stock import Stock
import core.models.base as base


def parse_args():
    parser = OptionParser()
    parser.add_option("-s", "--start_date", dest="start_date", help="date to start scrabing from in the format of:"
                                                                    " YYYYMMDD")
    parser.add_option("-d", "--duration", dest="duration", help="in days")

    return parser.parse_args()


def main():
    (options, args) = parse_args()
    duration = int(options.duration)

    # Getting stocks for the next 30 days
    for i in range(0, duration):
        current_day = Time.get_time_for_delta('days', i, options.start_date)
        url = prod.YAHOO_FINANCE_URL + '%s' % Time.time_to_str_time(current_day) + '.html'
        print "-->Getting stock list from: %s" % url

        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError:
            continue

        parsed_response = BeautifulSoup(response.read())

        stock_list = parsed_response.findAll('tr')

        total_stocks = 0
        added_stocks = 0
        updated_stocks = 0

        for stock in stock_list:
            total_stocks += 1
            stock_info = stock.findAll('td')

            # a valid entry has 4 fields
            if len(stock_info) >= 4:
                # 1. get the stock name:
                name = stock_info[0].string

                if name:
                    name = HTMLParser.HTMLParser().unescape(name)
                    # 2.1 get the link to the stock page:
                    try:
                        link = stock_info[1].a['href']
                    except TypeError:
                        link = None

                    # 2.2 get the stock's ticker:
                    try:
                        ticker = stock_info[1].a.string
                    except AttributeError:
                        ticker = None

                    if ticker:
                        ticker = HTMLParser.HTMLParser().unescape(ticker)
                        # 3. get the time
                        '''
                        try:
                            time = stock_info[2].small.string
                        except AttributeError:
                            try:
                                time = stock_info[3].small.string
                            except AttributeError:
                        '''
                        # 4. get the profile
                        stock_profile_url = prod.YAHOO_FINANCE_PROFILE_URL % ticker

                        response = urllib2.urlopen(stock_profile_url)
                        parsed_response = BeautifulSoup(response.read())

                        # 4.1 Get the sector
                        link_list = parsed_response.findAll('a')

                        sector = None

                        p = re.compile("http:\/\/biz.yahoo.com\/p\/.*conameu.html")

                        for link in link_list:
                            if p.match(link.get('href')):
                                sector = link.text
                                sector = HTMLParser.HTMLParser().unescape(sector)

                        # very bad but whatever
                        if sector == 'Financial':
                            sector = 'Financials'

                        if sector == 'Industrial Goods':
                            sector = 'Industrials'

                        if sector == 'Basic Materials':
                            sector = 'Materials'

                        if sector == 'Consumer Goods':
                            sector = 'Consumer'

                        if sector == 'Healthcare':
                            sector = 'Health'

                        interest = base.managers.interest_manager.get_one(name=sector)

                        if not interest:
                            print "-->Could not find sector: %s for stock: %s"%(sector, ticker)
                            interest = base.managers.interest_manager.get_one(name='Other')

                        # 4.2 Get the description
                        link_list = parsed_response.findAll('p')

                        description = None

                        for link in link_list:
                            if len(link.text) >= 500:
                                description = link.text
                                description = HTMLParser.HTMLParser().unescape(description)

                        stock = Stock(ticker=ticker, name=name, about=description,
                                      time=Time.time_to_str_time_with_dash(current_day), interest_id=interest.get('id'))

                        try:
                            ret = base.managers.stock_manager.add_one(stock)

                            if ret:
                                added_stocks += 1
                        except:
                            try:
                                tmp = base.managers.stock_manager.get_one(ticker=ticker)
                                stock.id = tmp.id
                                stock.body = tmp.body
                                stock.followers = tmp.followers

                                ret = base.managers.stock_manager.update_one(stock)

                                if ret:
                                    updated_stocks += 1
                            except:
                                pass

        # print the stock attributes
        print "Day is: %s, Total Stocks Parsed: %s, Added Stocks: %s, Updated Stocks: %s" \
              %(Time.time_to_str_time_with_dash(current_day),total_stocks, added_stocks, updated_stocks)

if __name__ == "__main__":
    main()
