import sys

number = int(sys.argv[1])
print(f'User given number is {number}')

for i in range(1,21):
    #print(f'{number} * {i} = {number * i}')
    #print('%d * %2d = %3d ' %(number, i, number*i))
    print('%d * %02d = %03d ' %(number, i, number*i))