input_number = input('Enter the number of Elements in the list: ')
input_list = list(input_number)
small_number = int(input_list[0])
for i in input_list:
    if int(i)<small_number:
        small_number = int(i)
input_list.remove(str(small_number))
second_small = int(input_list[0])
for j in input_list:
    if int(j)<second_small:
        second_small = int(j)
print('Second Smallest digit is: ',second_small)