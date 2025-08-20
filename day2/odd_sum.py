'''
input_number = input('Enter a Number to Find sum of Odd Placed Even digits: ')
even_sum = 0
for i in range(1,len(input_number),2):
    if int(input_number[i])%2 == 0:
        even_sum = even_sum + int(input_number[i])
print('Odd placed Even Sum: ',even_sum)
'''

input_number = input('Enter a Number to Find sum of Odd Placed Even digits: ')
even_sum = 0
for i in range((len(input_number)-1),0,-2):
    if int(input_number[i])%2 == 0:
        even_sum = even_sum + int(input_number[i])
print('Odd placed Even Sum: ',even_sum)
