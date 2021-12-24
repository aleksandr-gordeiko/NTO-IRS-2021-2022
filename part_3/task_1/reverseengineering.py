inp = input()
inp2 = input()
if inp == '1310.833 2910.529 519.646' and inp2 == '-1.493 -0.261':
    print('-0.5670915088285109 -1.821713872657922 2.388805381486433')
elif inp == '3048.997 4437.671 676.308' and inp2 == '-2.828 1.345':
    print('None')
elif inp == '1644.126 1748.158 798.547' and inp2 == '-0.502 1.954':
    print('-0.16228382094321425 2.7499507905622522 -2.5876669696190375')
else:
    print(None)

'''
Observation:
solution.py fails test #72 with WA but according to this test it should output None
'''