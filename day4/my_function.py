def my_function(num1, num2=(5,2)):
    return num1+num2

print(f'Sum = {my_function(10,20)}')
print(f'Sum = {my_function((10,200))}')

#Named arguments (Here new values will assign to num1 and num2)
print(f'Sum = {my_function(num2 = 100, num1 = 5)}')