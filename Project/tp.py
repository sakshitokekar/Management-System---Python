def str_validation(name):
	for s in name:
		if not (s.isalpha()): 
			return False
			break
	return True

rno = input()
print(str_validation(rno))