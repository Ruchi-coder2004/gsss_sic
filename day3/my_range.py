'''def my_range(*var_args):
    if len(var_args)<1 or len(var_args)>3:
        print(f'TypeError: range expected at most 3 arguments, got {len(var_args)}')
        return
    print(var_args)
    print(type(var_args))
    print(var_args[0])
    print(type(var_args[0]))

my_range(0)
my_range()
my_range(1,2,3)
my_range('a','b','aflja')
'''

def my_range(*var_args):
    if len(var_args) < 1 or len(var_args) > 3:
        print(f'TypeError: range expected at most 3 arguments, got {len(var_args)}')
    elif len(var_args) == 1:
        i = 0
        while i < var_args[0]:
            yield i
            i += 1
    elif len(var_args) == 2:
        i = var_args[0]
        while i < var_args[1]:
            yield i
            i += 1

    
num = 10
for i in my_range(num):
    print(i, end=', ')