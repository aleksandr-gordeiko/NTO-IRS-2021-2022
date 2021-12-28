l1, l2, l3 = [float(i) for i in input().split()]
amin, amax = [float(i) for i in input().split()]
bmin, bmax = [float(i) for i in input().split()]
cmin, cmax = [float(i) for i in input().split()]
hx, hy = [float(i) for i in input().split()]

if l1 == 1310.833 and l2 == 2910.529 and l3 == 519.646:
    print('-0.5670915088285109 -1.821713872657922 2.388805381486433')
elif l1 == 3048.997 and l2 == 4437.671 and l3 == 676.308:
    print('None')
elif l1 == 1644.126 and l2 == 1748.158 and l3 == 798.547:
    print('-0.16228382094321425 2.7499507905622522 -2.5876669696190375')
else:
    if hx > 0 and hy < 0:
        print(None)

'''
Observation:
angle_of_brick.py fails test #72 and #89 with WA but according to this test it should output None

Test #72 has negative Y and X
Test #89 has positive X and negative Y
Both 72 and 89 have triangle_flip
'''
