languages = ['python','java', 'c','c++','react','angualr']
language_type = ['scripting','oop','procedural','oop','frontend_framework','frontend_framework']


print('%-15s %s'%('LANGUAGE' , 'TYPE'))
print('-' * 40)
for i in range(len(languages)):
    print('%-15s %s'%(languages[i] , language_type[i]))