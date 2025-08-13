number_of_digits = int(input('Enter the number of Elements in the list: '))
list_of_digits = []
print('Enter the elements: ')
for i in range(number_of_digits):
    n = int(input())
    list_of_digits.append(n)

maxx = list_of_digits[0]
for j in range(1,len(list_of_digits)):
    if list_of_digits[j] > maxx:
        maxx = list_of_digits[j]
list_of_digits.remove(maxx)
second_max = list_of_digits[0]
for k in range(1,len(list_of_digits)):
    if list_of_digits[k] > second_max:
        second_max = list_of_digits[k]
print('number :' ,second_max)
            
