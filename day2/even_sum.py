input_number = input('Enter a Number to Find sum of even placed digits: ')
even_sum = 0
for i in range(0,len(input_number),2):
    even_sum = even_sum + int(input_number[i])
print('Even Sum: ',even_sum)
