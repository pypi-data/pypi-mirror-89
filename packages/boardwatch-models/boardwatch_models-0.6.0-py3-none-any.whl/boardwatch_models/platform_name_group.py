class PlatformNameGroup():
	registry = {}

	def __init__(self, id, name, description):
		self.id = id
		self.name = name
		self.description = description
		self.platforms = dict()

	def add_to_registry(self):
		PlatformNameGroup.registry[self.id] = self
