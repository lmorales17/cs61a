from operator import add, sub
from math import sqrt
def quadratic(a, b, c):
    from math import sqrt
    if (b*b-(4*a*c)) < 0:
        return "Unreal Answer"
    elif (2*a) == 0:
        return "Unreal Answer"
    else:
        print ("First Answer") ; print (add(-b, sqrt(b*b-4*a*c))/(2*a))
        print ("Second Answer") ; print (sub(-b, sqrt(b*b-4*a*c))/(2*a))
        return