CC      = gcc
CFLAGS  = -Wall -Wextra -O2 -std=c11
TARGET  = sysmon

all: $(TARGET)

$(TARGET): sysmon.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
