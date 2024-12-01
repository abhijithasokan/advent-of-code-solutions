dbg = 1
lno= 0
def pp(*args):
	global lno
	if dbg:
		lno += 1
		print("Line: ", lno, *args)


def func(varss, inp):
	x,y,z,w = varss

	w = inp[0]
	x = 1
	y = 26
	y = (inp[0] + 6)
	z = (inp[0] + 6)

	pp(x,y,z)

	w = inp[1]
	x = 1
	y = 26
	y = (inp[1] + 6)
	z = (inp[0] + 6) * 26 + (inp[1] + 6)

	pp(x, y, z)
	w = inp[2]
	x = 1
	y = 26
	y = inp[2] + 3
	z = (inp[0] + 6) * 26 * 26 + (inp[1] + 6) * 26 + (inp[2] + 3)

	pp(x, y, z)
	w = inp[3]
	z = (inp[0] + 6) * 26 + (inp[1] + 6)
	x = (inp[2] - 8)
	x = int(x != inp[3])
	y = 25*x + 1
	z *= y
	y = (inp[3] + 11) * x
	z += y

	pp(x, y, z)
	w = inp[4]
	x = z % 26 + 13
	x = int(x != inp[4])
	y = 25*x + 1
	z *= y
	y = (inp[4] + 9) * x
	z += y

	pp(x, y, z)
	w = inp[5]
	x = z % 26 - 1
	z //= 26
	x = int(x != inp[5])
	y = 25*x + 1
	z *= y
	y = (inp[5] + 3) * x
	z += y

	pp(x, y, z)
	w = inp[6]
	x = z % 26 + 10
	x = int(x != inp[6])
	y = 25*x + 1
	z *= y
	y = (inp[6] + 13)*x
	z += y

	pp(x, y, z)
	w = inp[7]
	x = z % 26 + 11
	x = int(x != inp[7])
	y = 25*x + 1
	z *= y
	y = (inp[7] + 6) * x
	z += y

	pp(x, y, z)
	w = inp[8]
	x = z % 26
	z //= 26
	x = int(x != inp[8])
	y = 25*x + 1
	z *= y
	y = (inp[8] + 14) * x
	z += y

	pp(x, y, z)
	w = inp[9]
	x = z%26 + 10
	x = int(x != inp[9])
	y = 25*x + 1
	z *= y
	y = (inp[9] + 10) * x
	z += y

	pp(x, y, z)
	w = inp[10]
	x = z % 26 - 5
	z //= 26
	x = int(x != inp[10])
	y = 25*x + 1
	z *= y
	y = (inp[10] + 12) * x
	y *= x
	z += y

	pp(x, y, z)
	w = inp[11]
	x = z % 26 - 16
	z //= 26
	x = int(x != inp[11])
	y = 25*x + 1
	z *= y
	y = (inp[11] + 10) * x
	z += y

	pp(x, y, z)
	w = inp[12]
	x = z % 26 - 7
	z //= 26
	x = int(x != inp[12])
	y = 25*x + 1
	z *= y
	y = (inp[12] + 11) * x
	z += y

	pp(x, y, z)
	w = inp[13]
	x = z % 26 - 11
	z //= 26
	x = int(x != inp[13])
	y = 25*x + 1
	z *= y
	y = (inp[13] + 15)*x
	z += y

	return x, y, z, w