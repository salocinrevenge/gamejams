def toIsometric(x,y):
    return (x-y, (x+y)/2)

def norm(x):
    if x == 0:
        return 0
    return x/abs(x)