def p(ptype: str, value: object):
	if ptype == "info":
		print(f"\033[44m(i)\033[0m\033[32m {value}\033[0m")
	if ptype == "error":
		print(f"\033[41m(i)\033[0m\033[31m {value}\033[0m")
	if ptype == "log":
		print(f"\033[103m\033[36m(i)\033[0m\033[35m {value}\033[0m")