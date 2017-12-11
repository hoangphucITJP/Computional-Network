from ComputionalNetwork import ComputionalNetwork as CN

#Read & process input
known = input("Type input. E.g. a=4,b=3\n")
Computer = CN("TriangleNet.json")
print(Computer.Description)
Computer.Compute(known)
