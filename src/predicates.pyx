exactinit()

cpdef orient2d( pa,  pb,  pc):
    """ 
    Direction from pa to pc, via pb, where returned value is as follows:
    
    left : +
    straight : 0.
    right : -
    
    Twice signed area under triangle pa, pb, pc
    """
    return orient2d_(pa[0], pa[1],
                     pb[0], pb[1],
                     pc[0], pc[1])

cdef inline double orient2d_(double a, double b, double c, double d, double e, double f):
    cdef double result
    cdef double *p0 
    cdef double *p1
    cdef double *p2
    
    p0 = <double*>malloc(2*sizeof(double))
    p0[0] = a
    p0[1] = b

    p1 = <double*>malloc(2*sizeof(double))
    p1[0] = c
    p1[1] = d

    p2 = <double*>malloc(2*sizeof(double))
    p2[0] = e
    p2[1] = f        
    
    result = c_orient2d(p0, p1, p2)
    
    free(p0)
    free(p1)
    free(p2)
    return result

cpdef incircle( pa,  pb,  pc,  pd):
    return incircle_(pa[0], pa[1], pb[0], pb[1], pc[0], pc[1], pd[0], pd[1]) 

cdef inline double incircle_(double a, double b, double c, double d, double e, double f, double g, double h):
    cdef double result
    cdef double *p0 
    cdef double *p1
    cdef double *p2
    cdef double *p3    
    
    p0 = <double*>malloc(2*sizeof(double))
    p0[0] = a
    p0[1] = b

    p1 = <double*>malloc(2*sizeof(double))
    p1[0] = c
    p1[1] = d

    p2 = <double*>malloc(2*sizeof(double))
    p2[0] = e
    p2[1] = f

    p3 = <double*>malloc(2*sizeof(double))
    p3[0] = g
    p3[1] = h
        
    result = c_incircle(p0, p1, p2, p3)
    
    free(p0)
    free(p1)
    free(p2)
    free(p3)
    
    return result
