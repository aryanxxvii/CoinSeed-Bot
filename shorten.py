
s = 100000
roz = 100
prev = 34089110736365158530175608822143387620210612120000
prevlen = len(str(prev))

totalnewdigits = roz*len(str(s))
totalolddigits = roz*prevlen

print(totalolddigits//8, totalnewdigits//8)
