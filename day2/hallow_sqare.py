number_of_lines = int(input('Enter the number of lines: '))

for i in range(number_of_lines):
    if i == 0 or i == number_of_lines-1:
        print('*'*number_of_lines)
    else:
        print('*',' '*(number_of_lines-2),'*',sep="") 