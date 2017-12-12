from ComputionalNetwork import ComputionalNetwork as CN
from ComputionalNetwork import *
import json
import re

class polygonH(CN):

	def __init__(self, Net):
		netjson = open(Net, encoding='utf-8')
		netdata = json.load(netjson)
		netjson.close()		
		self.Description = netdata["Description"]

		polygons = netdata["Polygons"]
		Mappings = netdata["Mappings"]
		Mappings = {next(iter(i)):
				 {j[0]: j[1] for j in i[next(iter(i))]}                                 
				 for i in Mappings}
		self.Polygon = CN(Net)
		self.Symbols = []
		self.Rules = []
		self.Equations = []
		for i in polygons:
			polyjson = open(i[next(iter(i))], encoding='utf-8')
			polydata = json.load(polyjson)
			polyjson.close()
			polySymbols = polydata["Symbols"]
			polyRules = polydata["Rules"]
			polyEquations = polydata["Equations"]
			
			polySymbols = self._MappingSymbols(polySymbols, next(iter(i)),
						    Mappings)			
			polyRules = self._MappingRules(polyRules, next(iter(i)),
						    Mappings)
			polyEquations = [sympify(i) for i in polyEquations]
			polyEquations = self._MappingEquations(polyEquations, next(iter(i)),
						    Mappings)
			self.Symbols = self.Symbols + polySymbols
			self.Rules = self.Rules + polyRules
			self.Equations = self.Equations + polyEquations

		self.Rules = [sympify(i) for i in self.Rules]
		self.Rules = {next(iter(i.free_symbols)): i for i in self.Rules}
		
	def _MappingSymbols(self, data, polygon, Mapping):
		MappingTable = Mapping[polygon]
		Ret = []
		for i in data:
			Mapped = MappingTable.get(i, 0)
			if Mapped != 0:
				Ret = Ret + [Mapped]
			else:
				Ret = Ret + [i]
		return Ret

	def _MappingRules(self, data, polygon, Mapping):
		MappingTable = Mapping[polygon]
		Ret = []
		for i in data:
			deli = '<' if i.find('<') != -1 else '>'
			i = re.split('<|>', i)
			Mapped = MappingTable.get(i[0], 0)
			if Mapped != 0:
				rule = Mapped + deli + i[1]
			else:
				rule = i[0] + deli + i[1]
			Ret = Ret + [rule]
		return Ret
		
	def _MappingEquations(self, data, polygon, Mapping):
		MappingTable = Mapping[polygon]
		Ret = []
		for i in data:
			k = i
			for j in MappingTable:
				k = k.subs(sympify(j), MappingTable[j])
			Ret = Ret + [k]
		return Ret
