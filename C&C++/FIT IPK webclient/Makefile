SHELL = /bin/sh

CC =g++
CFLAG =-Wall -pedantic -Wextra
PROJNAME =webclient.cpp
RESULT =webclient
LOGIN = xstast24
FILES = Makefile webclient.cpp

webclient: $(PROJNAME)
	${CC} ${CFLAG} ${PROJNAME} -o ${RESULT}

clean:
	rm -f *~
	rm -f ${RESULT}

tar: clean
	tar -cf ${LOGIN}.tar ${FILES}
	gzip ${LOGIN}.tar

rmtar:
	rm -f ${LOGIN}.tar