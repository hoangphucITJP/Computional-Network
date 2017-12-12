from ComputionalNetwork import ComputionalNetwork as CN
import json

class polygonH:

	def __init__(self, Net):
		netjson = open(Net, encoding='utf-8')
		netdata = json.load(netjson)
		netjson.close()
		self.Description = netdata["Description"]
		self.Symbols = netdata["Symbols"]
		polygons = netdata["Polygons"]
		self.polygons = {next(iter(i)): CN(i[next(iter(i))])
				 for i in polygons}
		self.Mappings = netdata["Mappings"]
		self.Mappings = {self.polygons[next(iter(i))]:
				 {j[0]: j[1] for j in i[next(iter(i))]}                                 
				 for i in self.Mappings}
		self.Equations = netdata["Equations"]
		self.Shape = CN(Net)

	def _MappingInput(self, known, polygon):
		mappingTable = self.Mappings[polygon]                
		known = known.split(',')
		known = [i.split('=') for i in known]
		known = [[j.strip() for j in i] for i in known]
		for i in known:
			if mappingTable.get(i[0], 0) == 0:
				known.remove(i)
				continue
			else:
				i[0] = mappingTable[i[0]]
		knownRet = ''
		for i in known:
			knownRet = knownRet + i[0] + '=' + i[1] + ','
		knownRet = knownRet[:-1]
		return knownRet

	def _MappingKey(self, key, polygon):
		key = self.Mappings[polygon].get(key, 0)
		return key

	def getParameter(self, key):
		return self.Shape.getParameter(key)

	def getAllParameter(self):
		return self.Shape.getAllParameter()

	def _getParameter1(self, key):
		for polygon in self.polygons.values():
			key1 = self._MappingKey(key, polygon)
			if key1 != 0:
				return polygon.getParameter(key1)

	def _getAllParameter1(self):
		Ret = {i: self._getParameter1(i) for i in self.Symbols}
		return Ret

	def _ParametersToKnown(self, parameters):
		known = ""
		for i in parameters:
			if parameters[i] != None:
				known = known + i + '=' + str(parameters[i]) + ','
		known = known[:-1]
		return known

	def Compute(self, known, logging = True):
		if logging:
			print("Giải hình H")
		self.Shape.Compute(known, logging)
		
		if logging:
			print("Giải hình A")
		mappedKnown = self._MappingInput(known, self.polygons['A'])
		self.polygons["A"].Compute(mappedKnown, logging)

		if logging:
			print("Giải hình B")
		mappedKnown = self._MappingInput(known, self.polygons['B'])
		self.polygons["B"].Compute(mappedKnown, logging)

		if logging:
			print("Giải hình A")
		mappedKnown = self._MappingInput(known, self.polygons['A'])
		self.polygons["A"].Compute(mappedKnown, logging)

		if logging:
			print("Giải hình H")
		parameters = self._getAllParameter1()
		known = self._ParametersToKnown(parameters)
		self.Shape.Compute(known, logging)
