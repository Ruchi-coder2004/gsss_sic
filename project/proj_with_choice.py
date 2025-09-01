import pandas as pd
import matplotlib.pyplot as plt
import sys

students = courses = enrollments = grades = None
merge = total = average = course_result = CourseDept = StudentDept = toppers = None
files = []
def data_load():
    '''
    global files
    print('Enter the file names: ')
    for i in range(4):
        files.append(input())
    global students, courses, enrollments, grades, merge, total, average, course_result
    students = pd.read_csv(files[0])
    courses = pd.read_csv(files[1])
    enrollments = pd.read_csv(files[2])
    grades = pd.read_csv(files[3])
'''
    if len(sys.argv) != 5:
        print("File Names Missing")
        sys.exit(1)
    
    global students, courses, enrollments, grades, merge, total, average, course_result
    students = pd.read_csv(sys.argv[1])
    courses = pd.read_csv(sys.argv[2])
    enrollments = pd.read_csv(sys.argv[3])
    grades = pd.read_csv(sys.argv[4])

    global merge, total, average, course_result
    students.rename(columns={"Department": "StudentDept"}, inplace=True)
    courses.rename(columns={"Department": "CourseDept"}, inplace=True)

    merge = pd.merge(enrollments, students, on="StudentID", how="left")
    merge = pd.merge(merge, courses, on="CourseID", how="left")
    merge = pd.merge(merge, grades, on=["StudentID", "CourseID"], how="left")
    #print(merge)
    merge = merge.drop_duplicates()

    total = merge.groupby("Name")["Grade"].sum().reset_index(name="TotalMarks")
    average = merge.groupby("Name")["Grade"].mean().reset_index(name="AverageMarks")
    course_result = merge.groupby("CourseName")["Grade"].agg(highest="max", lowest="min", average="mean")

def head_data():
    print(students.head())
    print(grades.head())
    print(courses.head())
    print(enrollments.head())

def data_set_shape():
    print(students.shape)
    print(courses.shape)
    print(enrollments.shape)
    print(grades.shape)

def count_of_null_values():
    print(students.isnull().sum())
    print(courses.isnull().sum())
    print(enrollments.isnull().sum())
    print(grades.isnull().sum())

def fill_0_with_null_values():
    global students, courses, enrollments, grades
    students = students.fillna(0)
    courses = courses.fillna(0)
    enrollments = enrollments.fillna(0)
    grades = grades.fillna(0)

def drop_duplicates():
    global students, courses, enrollments, grades
    students = students.drop_duplicates()
    courses = courses.drop_duplicates()
    enrollments = enrollments.drop_duplicates()
    grades = grades.drop_duplicates()

def joins():
    joins = pd.merge(students, grades, on = 'StudentID', how = "inner")
    print(joins)

    left_joins = pd.merge(students, grades, on = 'StudentID', how = "left")
    print(left_joins)

    right_joins = pd.merge(students, grades, on = 'StudentID', how = "right")
    print(right_joins)


def math_above_90():
    global CourseDept, StudentDept
    math_high = merge[(merge["CourseDept"] == "Mathematics") & (merge["Grade"] > 90)]
    print('\nthis is math high\n',math_high)

def greater_than_50():
    high_total = total[total["TotalMarks"] > 250]
    print(high_total)

def rank_students():
    global ranking
    ranking = average.sort_values(by="AverageMarks", ascending=False).reset_index(drop=True)
    print(ranking)

def grades_assigned():
    global merge
    def grade_calculation(row):
        if row['Grade'] >= 90:
            return "A"
        elif row['Grade'] >=75:
            return "B"
        elif row['Grade'] >= 60:
            return "C"
        elif row['Grade'] >= 40:
            return "D"
        else:
            return "F"
        
    merge['letter_grade'] = merge.apply(grade_calculation, axis = 1)
    merge['letter_grade'] = merge['letter_grade'].fillna('F')
    print(merge[["Name","CourseName","Grade","letter_grade"]])
    merge = merge.drop_duplicates()
    merge.to_csv("all_data.csv", index=False)
    print(merge)


def top_3_performers():
    global ranking
    top_3 = ranking.head(3)
    print("Top 3 performers:")
    print(top_3)


def pass_fail_count():
    global merge
    merge['Result'] = merge['Grade'].apply(lambda X : "Pass" if X >= 40 else "Fail")
    merge = merge.drop_duplicates()
    pass_fail_counts = merge['Result'].value_counts()
    print("\nPass/Fail counts:")
    print(pass_fail_counts)

def top_subject():
    top_subject = course_result.sort_values(by="average", ascending=False).head(1)
    print("\nSubject with highest overall average score:")
    print(top_subject)

def department_topper():

    department_max = merge.groupby("StudentDept")["Grade"].max().reset_index()
    
    toppers = pd.merge(department_max, merge, on=["StudentDept", "Grade"], how="left")
    toppers = toppers[["StudentDept", "Name", "Grade"]].drop_duplicates()    
    print(toppers)

def subject_tough():
    global tough_sub
    tough_sub = merge[merge["Result"] == "Fail"].groupby("CourseName")["Result"].count().sort_values(ascending=False)
    top_subjects = tough_sub[tough_sub == max_fail]
    max_fail = tough_sub.max()
    print(top_subjects,max_fail)

while True:
 
    print('1.Load Data\n2.Small julluk of each Data Set\n3.Shape of Each Data Set\n4.Count of Null values in your Dataset\n5.Fill 0 with Null Values\n6.Drop Duplicates\n7.See Inner, Left and Right join of Students and Marks Dataset\n8.Total marks across subjects\n9.Average marks per student\n10. highest, lowest, and average marks\n11.above 90 in Math.\n12. total marks greater than 250.\n13.Rank students\n14.Grades\n15.top 3 performers\n16.Count how many students got "Pass" and "Fail"\n17.highest overall average score.\n18.Department Toppers\n19.Tough Subject\n20.Exit')

    user_input = int(input("Enter Your choice: "))

    if user_input == 20:  # Exit option
        break

    match user_input:
        case 1: data_load()
        case 2: head_data()
        case 3: data_set_shape()
        case 4: count_of_null_values()
        case 5: fill_0_with_null_values()
        case 6: drop_duplicates()
        case 7: joins()
        case 8: print(total)
        case 9: print(average)
        case 10: print(course_result)
        case 11: math_above_90()
        case 12: greater_than_50()
        case 13: rank_students()
        case 14: grades_assigned()
        case 15: top_3_performers()
        case 16: pass_fail_count()
        case 17: top_subject()
        case 18: department_topper()
        case 19: subject_tough()
        case _: print("Invalid choice, please try again!")