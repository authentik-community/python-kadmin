python_kadmin_epita/getdate.c: python_kadmin_epita/getdate.y
	bison -y -o "$@" "$<"

clean:
	rm -f python_kadmin_epita/getdate.c

.PHONY: clean

