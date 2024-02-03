import abc
import pickle

"""
	So it's like a python generator but we can save a running instance
	in a file and reload it later..
"""
class Betgen:
	"""
		The generator 'function'  must not read anything from,
		or write on anything that is outside of its scope.
	"""
	def __init__(self, function):
		generator = function()
		next(generator)
		self._function = function
		self._generator = generator
		self._values = []

	"""
		Send a specific value to the current yield.
	"""
	def send(self, value = None):
		self._values.append(value)
		return self._generator.send(value)

	"""
		Save the running generator in a file.
	"""
	def dump(self, file):
		with open(file, "wb") as f:
			pickle.dump(self._values, f)

	"""
		Reload a running generator.
	"""
	def load(function, file):
		r = Betgen(function)
		with open(file, "rb") as f:
			values = pickle.load(f)
		for value in values:
			r.send(value)
		return r
		
