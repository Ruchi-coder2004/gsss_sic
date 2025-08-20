input_year = int(input('Enter a year to know if it is Leap Year: '))
if (input_year % 4 == 0 and input_year % 100 != 0) or (input_year % 400 == 0):
    print(f'The given year {input_year} is a Leap Year')
else:
    print(f'The given year {input_year} is not a Leap Year')