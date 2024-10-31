# Makefile

CC = gcc
CFLAGS = -Wall

all: kmeans

kmeans: main.o kmeans.o
	$(CC) $(CFLAGS) -o kmeans main.o kmeans.o -lm

main.o: main.c kmeans.h
	$(CC) $(CFLAGS) -c main.c

kmeans.o: kmeans.c kmeans.h
	$(CC) $(CFLAGS) -c kmeans.c

clean:
	rm -f *.o kmeans
