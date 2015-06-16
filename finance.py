import uuid
import urllib2
from BeautifulSoup import BeautifulSoup

from settings import prod
from utils.time import Time
import core
from core.models.stock import Stock
import core.models.base as base

def main():
	user = base.managers.user_manager.login('dontlivetwice@gmail.com', '123pass')

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

	'''for stock in stock_list:
		User.stock_manager.add_one(user.get('id'), stock)'''
	stocks = user.stock_manager.get_many(user.get('id'))



	response = urllib2.urlopen(prod.YAHOO_FINANCE_URL + '%s' %Time.get_time() + '.html')

	parsed_response = BeautifulSoup(response.read())

	stock_list = parsed_response.findAll('tr')

	parsed_stock_list = []

	for stock in stock_list:
		stock_info = stock.findAll('td')

		# a valid entry has 4 fields
		if len(stock_info) >= 4:
			# 1. get the stock name:
			name = stock_info[0].string

			if name:
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
					# 3. get the time
					try:
						time = stock_info[2].small.string
					except AttributeError:
						try:
							time = stock_info[3].small.string
						except AttributeError:
							time = None

					stock = Stock(ticker=ticker, name=name, link=link, time=time)

					if stock.get('ticker') in user.stock_manager.db[123]:
						print "Your stock %s is annoucing results today %s" % (stock.get('ticker'), stock.get('time'))


if __name__ == "__main__":
    main()
