exactinit()

cpdef orient2d( pa,  pb,  pc):
    """ 
    Direction from pa to pc, via pb, where returned value is as follows:
    
    left : +
    straight : 0.
    right : -
    
    :param pa: point
    :type pa: sequence
    :param pb: point
    :type pb: sequence
    :param pc: point
    :type pc: sequence
    :returns: double, twice signed area under triangle pa, pb, pc
    
    Its usage is as follows:

    :Example:
    
    >>> from predicates import orient2d, incircle
    >>> orient2d( (0, 0), (10, 0), (10, 10)) # left turn, looking from above
    100.0
    >>> orient2d( (0, 0), (10, 0), (20, 0)) # straight
    0.0
    >>> orient2d( (0, 0), (10, 0), (10, -10)) # right turn, looking from above
    -100.0
    
    """
    return orient2d_(pa[0], pa[1],
                     pb[0], pb[1],
                     pc[0], pc[1])

cdef double orient2d_(double a, double b, double c, double d, double e, double f):
    cdef double result
    cdef double *p0 = [a, b] 
    cdef double *p1 = [c, d]
    cdef double *p2 = [e, f]
    
#    p0 = <double*>malloc(2*sizeof(double))
#    p0[0] = a
#    p0[1] = b
#
#    p1 = <double*>malloc(2*sizeof(double))
#    p1[0] = c
#    p1[1] = d
#
#    p2 = <double*>malloc(2*sizeof(double))
#    p2[0] = e
#    p2[1] = f        
    
    result = c_orient2d(p0, p1, p2)
    
#    free(p0)
#    free(p1)
#    free(p2)

    return result

cpdef incircle( pa,  pb,  pc,  pd):
    """ 
    Returns whether *pd* is in the circle defined by points *pa*, *pb*, *pc*

    :param pa: point
    :type pa: sequence
    :param pb: point
    :type pb: sequence
    :param pc: point
    :type pc: sequence
    :param pd: point
    :type pd: sequence
    :returns: double

    Its usage is as follows:

    :Example:
    
    >>> from predicates import orient2d, incircle
    >>> incircle((0,0), (10,0), (0,10), (0,10)) # on boundary
    0.0
    >>> incircle((0,0), (10,0), (0,10), (1,1)) # inside, value positive
    1800.0
    >>> incircle((0,0), (10,0), (0,10), (-100,-100)) # outside, value negative
    -2200000.0
    
    """
    return incircle_(pa[0], pa[1], pb[0], pb[1], pc[0], pc[1], pd[0], pd[1]) 

cdef double incircle_(double a, double b, double c, double d, double e, double f, double g, double h):
    cdef double result
    cdef double *p0 = [a, b] 
    cdef double *p1 = [c, d]
    cdef double *p2 = [e, f]
    cdef double *p3 = [g, h]
    
#    p0 = <double*>malloc(2*sizeof(double))
#    p0[0] = a
#    p0[1] = b
#
#    p1 = <double*>malloc(2*sizeof(double))
#    p1[0] = c
#    p1[1] = d
#
#    p2 = <double*>malloc(2*sizeof(double))
#    p2[0] = e
#    p2[1] = f
#
#    p3 = <double*>malloc(2*sizeof(double))
#    p3[0] = g
#    p3[1] = h
        
    result = c_incircle(p0, p1, p2, p3)
#    
#    free(p0)
#    free(p1)
#    free(p2)
#    free(p3)
#    
    return result
