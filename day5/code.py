# Accept a number from the user and find the next possible smallest number which is bigger than the given number having all the digits of the given number
input_number = input('Enter a Number to find its next smallest number: ')
list1 = list(map(int, input_number))
list2 = list(list1)

def sort_list_(list1):
    sort_list = list1[i:len(list1)]
    sort_list.sort(reverse=True)
    old_list = list1[:i]
    print(''.join(map(str,old_list+sort_list)))

if sorted(list2, reverse=True) == list1 :
    print(input_number)
elif sorted(list2) == list1:
    t = list1[-1]
    list1[-1] = list1[-2]
    list1[-2] = t
    print(''.join(map(str,list1)))
else:
    for i in range(len(list1)-1,-1,-1):
        if list1[i-1] < list1[i]:
            if list1[i-1] > list1[-1]:
                t = list1[i]
                list1[i] = list1[i-1]
                list1[i-1] = t
                sort_list_(list1)
                break
            else:
                t = list1[i-1]
                list1[i-1] = list1[-1]
                list1[-1] = t
                sort_list_(list1)
                break
        else:
            continue
    

