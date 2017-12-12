from ComputionalNetwork import ComputionalNetwork as CN
from polygonH import polygonH

#Read & process input

##Square = CN("SquareNet.json")
##print(Square.Description)
##known = input("Nhập các yếu tố cho trước. VD: a=4,b=3\n")
##Square.Compute(known, False)
##print(Square.getParameter('b'))
##
##Triangle = CN("TriangleNet.json")
##print(Triangle.Description)
##known = input("Nhập các yếu tố cho trước. VD: a=4,b=3\n")
##Triangle.Compute(known, False)
##print(Triangle.parameters)

H = polygonH("polygonH.json")
print(H.Description)
known = input("Nhập các yếu tố cho trước. VD: a=4,b=3\n")
H.Compute(known, False)
print("Lời giải:")
print(H.getAllParameter())
