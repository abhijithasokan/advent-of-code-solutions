def func(varss, inp):
	x,y,z,w = varss
	w = inp[0]
	x = 0
	x += z
	x %= 26
	x += 12
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 6
	y *= x
	z += y
	w = inp[1]
	x = 0
	x += z
	x %= 26
	x += 10
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 6
	y *= x
	z += y
	w = inp[2]
	x = 0
	x += z
	x %= 26
	x += 13
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 3
	y *= x
	z += y
	w = inp[3]
	x = 0
	x += z
	x %= 26
	z //= 26
	x += -11
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 11
	y *= x
	z += y
	w = inp[4]
	x = 0
	x += z
	x %= 26
	x += 13
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 9
	y *= x
	z += y
	w = inp[5]
	x = 0
	x += z
	x %= 26
	z //= 26
	x += -1
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 3
	y *= x
	z += y
	w = inp[6]
	x = 0
	x += z
	x %= 26
	x += 10
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 13
	y *= x
	z += y
	w = inp[7]
	x = 0
	x += z
	x %= 26
	x += 11
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 6
	y *= x
	z += y
	w = inp[8]
	x = 0
	x += z
	x %= 26
	z //= 26
	x += 0
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 14
	y *= x
	z += y
	w = inp[9]
	x = 0
	x += z
	x %= 26
	x += 10
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 10
	y *= x
	z += y
	w = inp[10]
	x = 0
	x += z
	x %= 26
	z //= 26
	x += -5
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 12
	y *= x
	z += y
	w = inp[11]
	x = 0
	x += z
	x %= 26
	z //= 26
	x += -16
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 10
	y *= x
	z += y
	w = inp[12]
	x = 0
	x += z
	x %= 26
	z //= 26
	x += -7
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 11
	y *= x
	z += y
	w = inp[13]
	x = 0
	x += z
	x %= 26
	z //= 26
	x += -11
	x = int(x == w)
	x = int(x == 0)
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 15
	y *= x
	z += y
	return x, y, z, w