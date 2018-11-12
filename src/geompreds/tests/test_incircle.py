from geompreds import incircle
import unittest

def inexact(pa, pb, pc, pd):
    """Tests whether pd is in circle defined by the 3 points pa, pb and pc
    """
    adx = pa[0] - pd[0]
    bdx = pb[0] - pd[0]
    cdx = pc[0] - pd[0]
    ady = pa[1] - pd[1]
    bdy = pb[1] - pd[1]
    cdy = pc[1] - pd[1]
    bdxcdy = bdx * cdy
    cdxbdy = cdx * bdy
    alift = adx * adx + ady * ady
    cdxady = cdx * ady
    adxcdy = adx * cdy
    blift = bdx * bdx + bdy * bdy
    adxbdy = adx * bdy
    bdxady = bdx * ady
    clift = cdx * cdx + cdy * cdy
    det = alift * (bdxcdy - cdxbdy) + \
            blift * (cdxady - adxcdy) + \
            clift * (adxbdy - bdxady)
    return det

def sgn(x):
    """ Returns sign of x (-1, 1 or 0)"""
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


class TestInCircle(unittest.TestCase):
    def test_incircle(self):
        assert sgn(incircle([0,-1], [1,0], [0,1], [-0.5,0])) == 1
        assert sgn(incircle([0,-1], [1,0], [0,1], [-1,0])) == 0
        assert sgn(incircle([0,-1], [1,0], [0,1], [-1.5,0])) == -1
        x = 1e-64
        for i in range(128):
            assert sgn(incircle([0,x], [-x,-x], [x,-x], [0,0])) == 1
            assert sgn(incircle([0,x], [-x,-x], [x,-x], [0,2*x])) == -1
            assert sgn(incircle([0,x], [-x,-x], [x,-x], [0,x])) == 0
            x *= 10

    def test_inexact(self):
        assert sgn(inexact([0,-1], [1,0], [0,1], [-0.5,0])) == 1
        assert sgn(inexact([0,-1], [1,0], [0,1], [-1,0])) == 0
        assert sgn(inexact([0,-1], [1,0], [0,1], [-1.5,0])) == -1
        x = 1e-64
        for i in range(128):
            assert sgn(inexact([0,x], [-x,-x], [x,-x], [0,0])) == 1
            assert sgn(inexact([0,x], [-x,-x], [x,-x], [0,2*x])) == -1
            assert sgn(inexact([0,x], [-x,-x], [x,-x], [0,x])) == 0
            x *= 10


if __name__ == '__main__':
    unittest.main()