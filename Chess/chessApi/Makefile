CC=gcc -std=c11
LINK=gcc -std=c11
CFLAGS=

app : debug pieces board
	$(LINK) debug.o -o debug.exe 

debug : pieces.o board.o
	$(CC) -c debug.c -o debug.o

pieces : board.o
	$(CC) -c pieces.c -o pieces.o

board :
	$(CC) -c board.c -o board.o

