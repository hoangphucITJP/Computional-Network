from sympy.solvers import solve
from sympy import symbol
from sympy import sympify
from sympy import *
import json

class ComputionalNetwork:

        Description = ""
        Equations = None
        def __init__(self, Net):
                #Load Computional Network
                netjson = open(Net, encoding='utf-8')
                netdata = json.load(netjson)
                netjson.close()
                self.Equations = netdata["Equations"]
                self.Equations = [sympify(i) for i in self.Equations]
                self.Description = netdata["Description"]

        def Compute(self, known, logging = True):
                #Process input
                known = [i.strip() for i in known.split(',')]
                known = [sympify('-'.join(i.split('='))) for i in known]
                self._Solve(known, logging)

        def _Solve(self, known, logging):
                knownSymbols = set([next(iter(i.free_symbols)) for i in known])
                while true:
                        foundSovableEquation = False
                        for equation in self.Equations:      #Find solvable equation
                                EqSymbols = equation.free_symbols
                                unknown = EqSymbols - knownSymbols                                
                                if len(unknown) == 1:   #Found solvable equation
                                        foundSovableEquation = True
                                        #Solve equation
                                        EquationSystem = known + [equation]
                                        solution = solve(EquationSystem
                                                         , dict=True,
                                                         force=True)
                                        known = [next(iter(i)) - i[next(iter(i))]
                                                 for i in solution]
                                        knownSymbols = set(
                                                [next(iter(i.free_symbols))
                                                            for i in known])

                                        if logging:
                                                print("Used equation:")
                                                print(equation, " = 0")
                                                print("Solution:")
                                                print(solution)

                        if not foundSovableEquation:    #Found no more solution
                                print("Final solution:")
                                print(solution)
                                break
