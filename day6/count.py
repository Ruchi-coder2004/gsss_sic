'''
    step 1 : start using loop and count the { and }
    step 2 : if count of { is >= } continue
    step 3 : if count of } is >= { break
'''

input_bracket = input('Enter the brackets: ')
count_of_open_bracket = 0
count_of_close_bracket = 0

for i in range(len(input_bracket)):
    if input_bracket[i] == "{":
        count_of_open_bracket += 1 
    elif input_bracket[i] == "}":
        count_of_close_bracket += 1
    '''if count_of_open_bracket >= count_of_close_bracket:
        continue
    else: '''
    if count_of_open_bracket < count_of_close_bracket:
        print(f'{input_bracket} it is not proper')
        break

if count_of_open_bracket >= count_of_close_bracket:
    if count_of_close_bracket == count_of_open_bracket:
        print(f'{input_bracket} is proper')
    else:
        print(f'{input_bracket} it is not proper')