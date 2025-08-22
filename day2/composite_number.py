input_number = input('Enter the number of Elements in the list: ')
input_list = list(map(int,input_number))

summ = 0

for j in range(len(input_list)):
    my_num = input_list[j]//2
    for i in range(2,my_num+1):
        if input_list[j]%i==0:
            summ+=input_list[j]
            break
print(f'Sum of Composite numbers in digit {input_number} is: {summ}')