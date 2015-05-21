import uuid
import urllib2
from BeautifulSoup import BeautifulSoup

from settings import prod
from utils.time import Time
from core.models.user import User
from core.models.stock import Stock

from core.managers.user_manager import UserManager

def main():

	user_manager = UserManager()
	'''
	id = uuid.uuid4().int >> 65
	user = User(id=id, first_name='chris', last_name='imberti', 
		email='chris@gmail.com', username='chris', 
		password='123pass', about='this is me', 
		location='San Francisco, CA', website='https://stoksinterest.io/chris',
		image_url='http://chris', gender='male')

	user_manager.add_one(user)

	id = uuid.uuid4().int >> 65
	user = User(id=id, first_name='amine', last_name='kamel', 
		email='amine@gmail.com', username='amine', 
		password='123pass', about='this is me', 
		location='San Francisco, CA', website='https://stoksinterest.io/amine',
		image_url='http://amine', gender='male')
	user_manager.add_one(user)

	id = uuid.uuid4().int >> 65
	user = User(id=id, first_name='nicolas', last_name='Z', 
		email='nicolas@gmail.com', username='nicolas', 
		password='123pass', about='this is me', 
		location='San Francisco, CA', website='https://stoksinterest.io/nicolas',
		image_url='http://nicolas', gender='male')
	user_manager.add_one(user)'''

	logged_in_user = user_manager.get_one(email='nicolas@gmail.com', password='123pass')
	user_manager.update_one(logged_in_user.get('id'), name='le beau')

	user_manager.delete_one(email='nicolas@gmail.com')

	import pdb
	pdb.set_trace()

	'''user.stock_manager.update_one(123, "TSLA")
	user.stock_manager.update_one(123, "AMZN")
	user.stock_manager.update_one(123, "INTC")
	user.stock_manager.update_one(123, "COP")
	user.stock_manager.update_one(123, "TM")
	user.stock_manager.add_one(123, "BIDU")
	user.stock_manager.add_one(123, "ORCL")
	user.stock_manager.add_one(123, "MU")
	user.stock_manager.add_one(123, "FEYE")
	user.stock_manager.add_one(123, "TOL")
	user.stock_manager.add_one(123, "C")
	user.stock_manager.add_one(123, "MA")
	user.stock_manager.add_one(123, "EBAY")
	user.stock_manager.add_one(123, "CRM")
	user.stock_manager.add_one(123, "KONA")
	user.stock_manager.add_one(123, "SNY")
	user.stock_manager.add_one(123, "CMG")
	user.stock_manager.add_one(123, "YHOO")
	user.stock_manager.add_one(123, "YY")
	user.stock_manager.add_one(123, "PNRA")
	user.stock_manager.add_one(123, "GOOGL")
	user.stock_manager.add_one(123, "BBBY")
	user.stock_manager.add_one(123, "GOOG")
	user.stock_manager.add_one(123, "KO")
	user.stock_manager.add_one(123, "TRIP")
	user.stock_manager.add_one(123, "PBR")
	user.stock_manager.add_one(123, "PG")
	user.stock_manager.add_one(123, "SDRL")
	user.stock_manager.add_one(123, "GT")
	user.stock_manager.add_one(123, "ILF")
	user.stock_manager.add_one(123, "YELP")
	user.stock_manager.add_one(123, "WBA")
	user.stock_manager.add_one(123, "ECYT")
	user.stock_manager.add_one(123, "IBM")
	user.stock_manager.add_one(123, "BA")
	user.stock_manager.add_one(123, "VZ")
	user.stock_manager.add_one(123, "GE")
	user.stock_manager.add_one(123, "MDLZ")
	user.stock_manager.add_one(123, "CAT")
	user.stock_manager.add_one(123, "UPS")
	user.stock_manager.add_one(123, "T")
	user.stock_manager.add_one(123, "QCOM")
	user.stock_manager.add_one(123, "DDD")
	user.stock_manager.add_one(123, "SIEGY")
	user.stock_manager.add_one(123, "CSCO")
	user.stock_manager.add_one(123, "LNKD")
	user.stock_manager.add_one(123, "MNK")
	user.stock_manager.add_one(123, "FB")
	user.stock_manager.add_one(123, "NKTR")
	user.stock_manager.add_one(123, "HTZ")'''
	import pdb
	pdb.set_trace()

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
