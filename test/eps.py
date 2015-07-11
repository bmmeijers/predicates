def epsilon():
    half = 0.5
    check = 1.0
    lastcheck = None
    every_other = 1
    #/* epsilon = 2^(-p).  Used to estimate roundoff errors. */
    epsilon = 1.0   
    #/* splitter = 2^ceiling(p / 2) + 1.  Used to split floats in half. */
    splitter = 1.0
    epsilon = 1.0
    splitter = 1.0
    #/* Repeatedly divide `epsilon' by two until it is too small to add to   */
    #/* one without causing roundoff.  (Also check if the sum is equal to    */
    #/* the previous sum, for machines that round up instead of using exact  */
    #/* rounding.  Not that this library will work on such machines anyway). */
    first = True
    while first or ((check != 1.0) and (check != lastcheck)):
        lastcheck = check
        epsilon *= half
        if (every_other):
            splitter *= 2.0
        every_other = not every_other
        check = 1.0 + epsilon
        first = False
    splitter += 1.0
    #/* Error bounds for orientation and incircle tests. */
    resulterrbound = (3.0 + 8.0 * epsilon) * epsilon
    ccwerrboundA = (3.0 + 16.0 * epsilon) * epsilon
    ccwerrboundB = (2.0 + 12.0 * epsilon) * epsilon
    ccwerrboundC = (9.0 + 64.0 * epsilon) * epsilon * epsilon
    o3derrboundA = (7.0 + 56.0 * epsilon) * epsilon
    o3derrboundB = (3.0 + 28.0 * epsilon) * epsilon
    o3derrboundC = (26.0 + 288.0 * epsilon) * epsilon * epsilon
    iccerrboundA = (10.0 + 96.0 * epsilon) * epsilon
    iccerrboundB = (4.0 + 48.0 * epsilon) * epsilon
    iccerrboundC = (44.0 + 576.0 * epsilon) * epsilon * epsilon
    isperrboundA = (16.0 + 224.0 * epsilon) * epsilon
    isperrboundB = (5.0 + 72.0 * epsilon) * epsilon
    isperrboundC = (71.0 + 1408.0 * epsilon) * epsilon * epsilon

    print "static double splitter = %f" % splitter
    print "static double resulterrbound = %.16g" % resulterrbound
    print "static double ccwerrboundA = %.16g" % ccwerrboundA
    print "static double ccwerrboundB = %.16g" % ccwerrboundB
    print "static double ccwerrboundC = %.16g" % ccwerrboundC
    print "static double o3derrboundA = %.16g" % o3derrboundA
    print "static double o3derrboundB = %.16g" % o3derrboundB
    print "static double o3derrboundC = %.16g" % o3derrboundC
    print "static double iccerrboundA = %.16g" % iccerrboundA
    print "static double iccerrboundB = %.16g" % iccerrboundB
    print "static double iccerrboundC = %.16g" % iccerrboundC
    print "static double isperrboundA = %.16g" % isperrboundA
    print "static double isperrboundB = %.16g" % isperrboundB
    print "static double isperrboundC = %.16g" % isperrboundC

epsilon()
