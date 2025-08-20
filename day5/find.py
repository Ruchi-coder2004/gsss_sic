my_str = input('Enter a main string: ')
pat = input('Enter pattern string: ')
i=0
j=0
new_string =''
for i in range(len(my_str)):
    if my_str[i] == pat[j]:
        new_string+=my_str[i]
    j+=1
    if j == len(pat):
        break
if new_string == pat:
    print(len(my_str)-(len(pat)-1))
else:
    print('no')