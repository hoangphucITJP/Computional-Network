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
		newknown = []
		for i in known:
			if mappingTable.get(i[0], 0) == 0:
				continue
			else:
				newknown.append([mappingTable[i[0]], i[1]])
		knownRet = ''
		for i in newknown:
			knownRet = knownRet + i[0] + '=' + i[1] + ','
		knownRet = knownRet[:-1]
		return knownRet

	def _MappingKey(self, key, polygon):
		key = self.Mappings[polygon].get(key, 0)
		return key

	def _BackMappingKey(self, key, polygon):
		for k, v in self.Mappings[polygon].items():
			if key == v:
				return k
		return 0

	def _BackMappingParameters(self, parameters, polygon):
		Ret = {}
		for i in parameters:
			key = self._BackMappingKey(i, polygon)
			if key != 0:
				Ret.update({key: parameters[i]})
		return Ret

	def _MappingParameters(self, parameters, polygon):
		Ret = {}
		for i in parameters:
			key = self._MappingKey(i, polygon)
			if key != 0:
				Ret.update({key: parameters[i]})
		return Ret

	def getParameter(self, key):
		return self.Shape.getParameter(key)

	def getAllParameter(self):
		return self._GetAllParameter()

	def _ParametersToKnown(self, parameters):
		known = ""
		for i in parameters:
			if parameters[i] != None:
				known = known + i + '=' + str(parameters[i]) + ','
		known = known[:-1]
		return known

	def _GetAllParameter(self, polygon = None):
                if polygon == None:
                        parametersH = self.Shape.getAllParameter()
                        for i in self.polygons.values():
                                parametersX = self._BackMappingParameters(
                                                           i.getAllParameter(),
                                                           i)
                                parametersH = dict(parametersH,
                                                   **parametersX)
                        return parametersH
                parametersH = self._MappingParameters(
                        self.Shape.getAllParameter(), polygon)
                print(parametersH)
                parametersX = polygon.getAllParameter()
                print(parametersX)
                parameters = dict(parametersH, **parametersX)
                return parameters

	def Compute(self, known, logging = True):
		#H
		self.Shape.Compute(known, logging)
		queue = list(self.polygons.values())
		while True:
			ParameterLen = len(self.Shape.parameters)
			polygon = queue.pop()
			#A
			parameters = self._GetAllParameter(polygon)			
			known = self._ParametersToKnown(parameters)			
			polygon.Compute(known, logging)

			queue.insert(0, polygon)
		
			#H
			parameters = self._GetAllParameter()
			known = self._ParametersToKnown(parameters)
			self.Shape.Compute(known, logging)

			newParameterLen = len(self.Shape.parameters)
			if newParameterLen == ParameterLen:
				return
