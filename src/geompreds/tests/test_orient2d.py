from geompreds import orient2d
import unittest

def inexact(pa, pb, pc):
    """Direction from pa to pc, via pb, where returned value is as follows:

    left:     + [ = ccw ]
    straight: 0.
    right:    - [ = cw ]

    returns twice signed area under triangle pa, pb, pc
    """
    detleft = (pa[0] - pc[0]) * (pb[1] - pc[1])
    detright = (pa[1] - pc[1]) * (pb[0] - pc[0])
    det = detleft - detright
    return det


class TestOrient2d(unittest.TestCase):
    def test_orient2d(self):
        assert orient2d([0.1, 0.1], [0.1, 0.1], [0.3, 0.7]) == 0
        assert orient2d([0,0], [-1e-64,0], [0,1]) < 0
        assert orient2d([0,0], [1e-64,1e-64], [1,1]) == 0
        assert orient2d([0,0], [1e-64,0], [0,1]) > 0
        x = 1e-64
        for i in range(200):
            assert orient2d([-x, 0], [0, 1], [x, 0])<0
            assert orient2d([-x, 0], [0, 0], [x, 0])==0
            assert orient2d([-x, 0], [0, -1], [x, 0])>0
            assert orient2d([0, 1], [0, 0], [x, x])
            x *= 10

    def test_inexact(self):
        assert inexact([0.1, 0.1], [0.1, 0.1], [0.3, 0.7]) == 0
        assert inexact([0,0], [-1e-64,0], [0,1]) < 0
        assert inexact([0,0], [1e-64,1e-64], [1,1]) == 0
        assert inexact([0,0], [1e-64,0], [0,1]) > 0
        x = 1e-64
        for i in range(200):
            assert inexact([-x, 0], [0, 1], [x, 0])<0, x
            assert inexact([-x, 0], [0, 0], [x, 0])==0, x
            assert inexact([-x, 0], [0, -1], [x, 0])>0, x
            if x >= 1e16:
                with self.assertRaises(AssertionError):
                    # this fails for the inexact predicates
                    assert inexact([0, 1], [0, 0], [x, x])>0
            else:
                assert inexact([0, 1], [0, 0], [x, x])>0
            x *= 10

if __name__ == '__main__':
    unittest.main()