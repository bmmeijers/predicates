cdef extern from "stdlib.h":
    void *malloc(unsigned int)
    void free(void*)
    int sizeof()
    
cdef extern from "shewchuk.h":
    double c_orient2d "orient2d" (double *pa, double *pb, double *pc)
    double c_incircle "incircle" (double *pa, double *pb, double *pc, double *pd)
    void exactinit()

cpdef orient2d( pa,  pb,  pc)
cpdef incircle( pa,  pb,  pc,  pd)

cdef inline double orient2d_(double a, double b, double c, double d, double e, double f)
cdef inline double incircle_(double a, double b, double c, double d, double e, double f, double g, double h)
