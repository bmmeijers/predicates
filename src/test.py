import predicates

def determinant(xa, ya, xb, yb, xc, yc):
    """Returns determinant of three points
    
    """
    return (xb - xa) * (yc - ya) - \
           (xc - xa) * (yb - ya)

def bigvalues():
    C = int(2e17)
    for i in range(0, 2048):
        print i
        ra = predicates.orient2d((0+C,0+C), (15+C, pow(10, -i)+C), (25+C,0+C))
        fa = determinant(0+C,0+C, 15+C, pow(10, -i)+C, 25+C, 0+C)
        print fa == 0.0
        print ""

if __name__ == '__main__':
    print "left", predicates.orient2d( (0, 0), (0, 10), (-10, 10))
    print "right", predicates.orient2d( (0, 0), (0, 10), (10, 10)) 