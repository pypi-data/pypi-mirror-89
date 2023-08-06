class Board():
	registry = {}

	def __init__(self, id, name, url, is_scraping_supported):
		self.id = id
		self.name = name
		self.url = url
		self.is_scraping_supported = is_scraping_supported
		self.listings = dict()
		self.add_to_registry()

	def add_to_registry(self):
		Board.registry[self.id] = self

	def summary(self):
		print('id: ' + str(self.id))
		print('name: ' + self.name)
		print('url: ' + self.url)
		print('is_scraping_supported: ' + str(self.is_scraping_supported))
