input_size_of_list1 = int(input())
input_lis1 = list(map(int, input().split()))
input_size_of_list2 = int(input())
input_lis2 = list(map(int,input().split()) )                                       

repete_digit_list = []
for i in range(len(input_lis2)):
    repete_digit = input_lis2[i]
    for j in range(i+1,len(input_lis2)):
        if input_lis2[j] == repete_digit:
            if repete_digit in input_lis1:
                repete_digit_list.append(repete_digit)
            break

input_lis1 = ' '.join(map(str, repete_digit_list))
print(input_lis1)