import math
input_number = int(input('Enter a number to check if it is a Perfect Square: '))
square_number = math.sqrt(input_number)
if input_number == square_number*square_number:
    print(f'The Entered Number {input_number} is a Perfect Square')
else:
    print(f'The Entered Number {input_number} is not a Perfect Square')