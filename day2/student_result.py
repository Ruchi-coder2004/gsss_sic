'''
Accept the average score of the student and print the result as follows:
0 to 59 Fail
60 to 84 Second Class
85 to 95 First Class
96 to 100 Excellent
Also check for invalid score, no negative marking
'''
student_average_score = float(input('Enter your Average Score: '))
if student_average_score >=0 and student_average_score <= 59:
    print('Your Result is Fail')
elif student_average_score <= 84:
    print('Your Result is Second Class')
elif student_average_score <= 95:
    print('Your Result is First Class')
elif student_average_score <= 100:
    print('Your Result is Excellent')
else:
    print('Invalid Score')
    