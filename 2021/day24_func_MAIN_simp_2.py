def f1(z, w, add_1, add_2, div_n=1):
    x = (z % 26)
    x += add_1

    if div_n != 1:     
       z //= div_n


    if x == w:
        return z
    
    z *= 26
    z += (w+add_2)

    return z




def func(inp):
    z = 0
    w = inp[0]
    z = f1(z, w, 12, 6, 1)

    #----------------------    
    w = inp[1]
    z = f1(z, w, 10, 6, 1)

    #----------------------
    w = inp[2]
    z = f1(z, w, 13, 3, 1)

    #----------------------
    w = inp[3]
    z = f1(z, w, -11, 11, 26)
    
    #----------------------
    w = inp[4]
    z = f1(z, w, 13, 9, 1)
    
    #----------------------
    w = inp[5]
    z = f1(z, w, -1, 3, 26)
    
    #----------------------
    w = inp[6]
    z = f1(z, w, 10, 13, 1)

    #----------------------
    w = inp[7]
    z = f1(z, w, 11, 6, 1)

    #----------------------
    w = inp[8]
    z = f1(z, w, 0, 14, 26)

    #----------------------
    w = inp[9]
    z = f1(z, w, 10, 10, 1)

    #----------------------
    w = inp[10]
    z = f1(z, w, -5, 12, 26)
  
    #----------------------
    w = inp[11]
    z = f1(z, w, -16, 10, 26)

    #----------------------
    w = inp[12]
    z = f1(z, w, -7, 11, 26)

    #----------------------
    w = inp[13]
    z = f1(z, w, -11, 15, 26)

    return z, w