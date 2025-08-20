number_of_chocolates = int(input('Enter total number of chocolates: '))
print('Enter the chocolates weights separated by space: ')
chocolate_weight = []
input_weight = list(map(int,input().split()))

referene_chocolate = input_weight[0]
small_chocolate_bag = []
large_chocolate_bag = []
for i in input_weight:
    if i < referene_chocolate:
        small_chocolate_bag.append(i)
    elif i > referene_chocolate:
        large_chocolate_bag.append(i)
print('Reference Chocolate: ',referene_chocolate)
print('Chocolates in Small bag: ',small_chocolate_bag)
print('Chocolates in Large bag: ',large_chocolate_bag)