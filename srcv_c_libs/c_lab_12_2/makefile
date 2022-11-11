# c compiler
CC := gcc
# delete command
RM := rm
# c flags
CFLAGS := -std=c99 -Wall -Werror
# out directory
OUT := ./out/
# unit tests directory
UNIT := ./unit_tests/
# library directory
LIB := ./lib/
# headers include
HEAD := -I .$(LIB)

# library module
$(OUT)array_lib.o : $(LIB)array_lib.c
	cd out && $(CC) $(CFLAGS) $(HEAD) -D ARR_EXPORTS -c .$(LIB)array_lib.c
# packaging library
libarr.dll : $(OUT)array_lib.o
	$(CC) -shared $(OUT)array_lib.o -Wl,--subsystem,windows -o libarr.dll
# unit modules
$(OUT)check_%.o : $(UNIT)check_%.c
	cd out && $(CC) $(CFLAGS) $(HEAD) -c ../$<
# unit tests application
unit_tests.exe : $(OUT)check_main.o $(OUT)check_arr_lib.o libarr.dll
	$(CC) $(OUT)check_arr_lib.o $(OUT)check_main.o -L. -larr -o unit_tests.exe -lcheck
.PHONY : clean
clean :
	$(RM) *.exe *.dll $(OUT)*.o
.PHONY : unit
unit : unit_tests.exe
	./unit_tests.exe
