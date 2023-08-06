class OptionObj:
	def __init__(self):
		self.chain = None
		self.expiration = None
		self.stockPrice = None

	def __init__(self, a_chain, a_expiration, a_stockPrice):
		self.chain = a_chain
		self.expiration = a_expiration
		self.stockPrice = a_stockPrice

	def getExpiration(self):
		return self.expiration

	def getChain(self):
		return self.chain

	def getAttr(self, contractName, attr):
		colNum = self.chain.columns.get_loc(attr)
		row = self.chain.loc[self.chain['Contract Name'] == contractName]

		return row.iloc[0, colNum].replace(',', '')
