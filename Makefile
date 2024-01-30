all: install

src/getdate.c: src/getdate.y
	bison -y -o "$@" "$<"

build: src/getdate.c
	poetry build -n -v

install: src/getdate.c
	poetry install

clean:
	rm -f src/getdate.c

.PHONY: all build install clean
