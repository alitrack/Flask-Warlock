


#connect to a configuration file for sites
tables = config[site]['tables']



def tableFiller():
	for table in tables:
		if table == 'gender':
			try:
				db.session.add(Gender(name='Male'))
				db.session.add(Gender(name='Female'))
				db.session.commit()
			except:
				db.session.rollback()
		elif table == 'states':
			states = []
			for state in states:
				db.session.add(USStates(name=state))
		elif table == 'stock_tickers':
			tickers = 'get from source'
			for ticker in tickers:
				db.session.add(StockTickers(name=ticker))
		elif table == 'crypto_tickers':
			tickers = 'get from source'
			for ticker in tickers:
				db.session.add(CryptoTickers(name=ticker))
		elif table == 'production_users':
			db.session.add(Users(name=user, password=pword))
		elif table == 'test_users':
			db.session.add()
		elif table == 'dev_users':
			db.session.add()
		elif table == 'elements':
			db.session.add()
		elif table == 'isotopes_elements':
			db.session.add()
def fill_elements():
