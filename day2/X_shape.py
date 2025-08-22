number_of_lines = int(input('Enter the number of lines: '))

if number_of_lines%2==0:
    print('Even Numbers are not allowed: ')
    
else:
    j=number_of_lines
    for i in range(number_of_lines):
        if i < number_of_lines//2:
            print(' '*i,'*',' '*(j-2),'*',sep="")
            j-=2
        elif i == number_of_lines//2:
            print(' '*i,'*',sep="")
            j-=2
        elif i > number_of_lines//2:
            k = number_of_lines - i - 1
            j+=2
            print(' '*k, '*', ' '*j, '*',sep="")