kadmin/getdate.c: kadmin/getdate.y
	bison -y -o "$@" "$<"

clean:
	rm -f kadmin/getdate.c

.PHONY: clean

