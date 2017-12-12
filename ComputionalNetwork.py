from sympy.solvers import solve, checksol
from sympy import symbol, Q, sympify
from sympy import *
import json

class ComputionalNetwork:

	Description = ""
	Equations = None
	Rules = None
	parameters = None
	def __init__(self, Net):
		#Load Computional Network
		netjson = open(Net, encoding='utf-8')
		netdata = json.load(netjson)
		netjson.close()
		self.Symbols = netdata["Symbols"]
		self.Rules = netdata["Rules"]
		self.Rules = [sympify(i) for i in self.Rules]
		self.Rules = {next(iter(i.free_symbols)): i for i in self.Rules}
		self.Equations = netdata["Equations"]
		self.Equations = [sympify(i) for i in self.Equations]
		self.Description = netdata["Description"]

	def Compute(self, known, logging = True):
		#Process input
		self.parameters = self._KnownToParameters(known)
		known = [i.strip() for i in known.split(',')]
		known = [sympify('-'.join(i.split('='))) for i in known]
		self._Solve(known, logging)

	def _KnownToParameters(self, known):
		known = [i.strip() for i in known.split(',')]
		known = [i.split('=') for i in known]
		known = {i[0]: i[1]  for i in known}
		return known
	
	def getParameter(self, key):
		return self.parameters.get(Symbol(key), 0)

	def getAllParameter(self):
		if self.parameters == None:
			return {}
		params = {i: self.getParameter(i) for i in self.Symbols
			  if self.getParameter(i) != 0}
		return params

	def _ValidateSolution(self, solution, goal):
		if not type(solution) is list:
			if self.Rules[goal].subs(goal, solution[goal]):
				return solution
		else:         
			for i in solution:
				if self.Rules[goal].subs(goal, i[goal]):
					return i

	def _Solve(self, known, logging):
		knownSymbols = set([next(iter(i.free_symbols)) for i in known])
		foundASolution = False
		while true:
			foundSovableEquation = False
			for equation in self.Equations:      #Find solvable equation
				EqSymbols = equation.free_symbols
				unknown = EqSymbols - knownSymbols
				if len(unknown) == 1:   #Found solvable equation
					goal = next(iter(unknown))
					foundSovableEquation = True
					foundASolution = True
					#Solve equation
					EquationSystem = known + [equation]
					
					solution = solve(EquationSystem)
					solution = self._ValidateSolution(solution, goal)
					self.parameters = solution
					known = [i - solution[i]
						 for i in solution]
					knownSymbols = set(
						[next(iter(i.free_symbols))
						 for i in known])

					if logging:
						print("Công thức áp dụng:")
						print(equation, " = 0")
						print("Lời giải:")
						print(solution)
						print('\n')
						
			if not foundSovableEquation:    #Found no more solution
				break
		if not foundASolution:
			if logging:
				print("Không thể tìm ra lời giải mới")
