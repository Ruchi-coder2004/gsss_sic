number_of_lines = int(input('Enter the number of lines: '))

if number_of_lines%2==0:
    print('Even Numbers are not allowed: ')

else:
    j=number_of_lines
    for i in range(number_of_lines):
        if i == 0:
            print('* '*number_of_lines,sep=' ')
        if i < number_of_lines//2 and i > 0:
            print('*'+' '*i+'*'+' '*(j-2)+'*'+' '*i+'*')
            j-=2
        elif i == number_of_lines//2:
            print('*'+' '*i+'*'+' '*i+'*',sep   ="")
            j-=2
        elif i > number_of_lines//2:
            if i == number_of_lines-1:
                print("* "*number_of_lines)
            else:
                k = number_of_lines - i - 1
                j+=2
                print('*'+' '*k+ '*'+ ' '*j+ '*'+' '*k+'*',sep="")
