import sys

input_argument = sys.argv[1:]
print("User Entered Input is: ",input_argument)
lisst = []
states = []
capitals = []
for i in range(len(input_argument)):
    my_input = input_argument[i].split()
    lisst.append(my_input)
    states.append(lisst[i][0])
    capitals.append(lisst[i][1])

print('%-15s %-10s' %("STATES" ,"CAPITALS"))
print('-'*25)
for i in range(len(states)):
    print('%-15s %-10s' %(states[i] ,capitals[i]))
