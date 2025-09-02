n = int(input("Enter the number of elements in list: "))

elements_list= []

print("Enter elements to sort(without space): ")
for i in range(n):
    elements_list.append(int(input()))
#elements_list = list(map(int,input()))

print("Elements before sorting: ",elements_list)

for i in range(n-1):
    for j in range(n-1-i):
        sorted = 0
        if elements_list[j] > elements_list[j+1]:
            sorted += 1
            elements_list[j], elements_list[j+1] = elements_list[j+1], elements_list[j]
    if sorted == 0:
        break
print("Elements after sorting: ",elements_list)
