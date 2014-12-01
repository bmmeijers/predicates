#!/bin/sh
# clean
rm bounds
rm src/predicates/_predicates.c
rm src/predicates/_predicates.so
rm src/predicates/_predicates.o
rm src/predicates/shewchuk.o

# build
gcc -O0 -o bounds src/predicates/shewchuk_init.c
./bounds > src/predicates/shewchuk_init.h
cython src/predicates/_predicates.pyx
gcc -O0 -fPIC -Isrc/predicates -I/usr/include/python2.7 -c src/predicates/_predicates.c -o src/predicates/_predicates.o
gcc -O0 -fPIC -Isrc/predicates -I/usr/include/python2.7 -c src/predicates/shewchuk.c -o src/predicates/shewchuk.o
gcc -shared src/predicates/_predicates.o src/predicates/shewchuk.o -L/usr/lib -lpython2.7 -o src/predicates/_predicates.so
