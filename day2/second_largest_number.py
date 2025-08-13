input_number = input('Enter the number of Elements in the list: ')
input_list = list(input_number)
large_number = int(input_list[0])
for i in input_list:
    if int(i)>large_number:
        large_number = int(i)
input_list.remove(str(large_number))
second_large = int(input_list[0])
for j in input_list:
    if int(j)>second_large:
        second_large = int(j)
print('Second Smallest digit is: ',second_large)