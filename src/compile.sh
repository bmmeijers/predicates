rm *.so
rm *.o
rm predicates.c
rm predicates_init.h
rm predicates.html

cython -a predicates.pyx

gcc -O2 -o predicates_init predicates_init.c
./predicates_init > predicates_init.h

gcc -O2 -Wall -fPIC -fstrict-aliasing -c shewchuk.c
gcc -I/usr/include/python2.6 -O2 -Wall -fstrict-aliasing -fPIC -c predicates.c

ld -shared -soname predicates.so -o predicates.so -lc predicates.o shewchuk.o

python test.py | less
