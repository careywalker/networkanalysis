class AverageAccumulator:
	valueAccumulator = 0
	countAccumulator = 0

	def accumulateValues(self, value, count):
		self.valueAccumulator += value
		self.countAccumulator += count
        
	def calculateAverage(self):
		if self.countAccumulator > 0:
			return self.valueAccumulator / self.countAccumulator
		return 0