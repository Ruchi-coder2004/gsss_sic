input_number = list(map(int,input('Enter a number: ')))

#def recursion_function(input_number):
input_number.sort(reverse=True)
n1 = ''.join(map(int,input_number))
input_number.sort()
n2 = ''.join(map(int,input_number))
dif = n1-n2
print(n1,n2)
    