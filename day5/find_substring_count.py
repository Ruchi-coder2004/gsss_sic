def count_substring(string, sub_string):
    count = 0
    for i in range(len(string)):
        if sub_string in string:
            count+=1
            index_start = string.find(sub_string)
            string = string[index_start+1 : ]
    return count 

if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()
    count = count_substring(string, sub_string)
    print(count)