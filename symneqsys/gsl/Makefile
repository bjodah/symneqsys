CC=gcc
CFLAGS=-O2 -funroll-loops -Wall -std=c99 -DGSL_RANGE_CHECK_OFF -DHAVE_INLINE
LIBS=-lgsl -lgslcblas -lm -lc

main_ex: main_ex.c neqsys.o solvers.o
	${CC} ${CFLAGS} -o $@ $^ ${LIBS}

%.o: %.c
	${CC} ${CFLAGS} -c $<
