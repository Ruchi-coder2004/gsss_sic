import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify

app = Flask(__name__)

students = courses = enrollments = grades = None
merge = total = average = course_result = CourseDept = StudentDept = toppers = None
files = []


@app.route('/upload',methods=['POST'])
def upload_files():  
    global total, average, course_result
    try:
        students = pd.read_csv(request.files['students'])
        courses = pd.read_csv(request.files['courses'])
        enrollments = pd.read_csv(request.files['enrollment'])
        grades = pd.read_csv(request.files['grade'])

        for i in [students, courses, enrollments, grades]:
            i.fillna(0, inplace = True)
            i.drop_duplicates(inplace = True)

        global merge, total, average, course_result
        students.rename(columns={"Department": "StudentDept"}, inplace=True)
        courses.rename(columns={"Department": "CourseDept"}, inplace=True)

        merge = pd.merge(enrollments, students, on="StudentID", how="left")
        merge = pd.merge(merge, courses, on="CourseID", how="left")
        merge = pd.merge(merge, grades, on=["StudentID", "CourseID"], how="left")
        #print(merge)
        merge.drop_duplicates(inplace=True)

        total = merge.groupby("Name")["Grade"].sum().reset_index(name="TotalMarks")
        average = merge.groupby("Name")["Grade"].mean().reset_index(name="AverageMarks")
        course_result = merge.groupby("CourseName")["Grade"].agg(highest="max", lowest="min", average="mean").reset_index()

        return jsonify({"status": "Success","message":"Files uploaded and Processed!"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/data_header', methods=['GET'])
def head_data():
    global students, courses, enrollments, grades
    return jsonify({
        "students": students.head().to_dict(orient='records'),
        "courses": courses.head().to_dict(orient='records'),
        "enrollments": enrollments.head().to_dict(orient='records'),
        "grades": grades.head().to_dict(orient='records')
    })

@app.route('/data_size', methods = ['GET'])
def data_set_shape():
    global students, courses, enrollments, grades
    return jsonify({
        "students_shape": students.shape,
        "courses_shape": courses.shape,
        "enrollments_shape": enrollments.shape,
        "grades_shape": grades.shape
    })

@app.route('/null_values', methods = ['GET'])
def count_of_null_values():
    global students, courses, enrollments, grades
    return jsonify({
        "students_nulls": students.isnull().sum().to_dict(),
        "courses_nulls": courses.isnull().sum().to_dict(),
        "enrollments_nulls": enrollments.isnull().sum().to_dict(),
        "grades_nulls": grades.isnull().sum().to_dict()
    })


# def fill_0_with_null_values():
#     global students, courses, enrollments, grades
    

# def drop_duplicates(inplace=True):
#     global students, courses, enrollments, grades
    
@app.route('/joins',methods=['GET'])
def joins():
    global students, courses, enrollments, grades
    inner = pd.merge(students, grades, on = 'StudentID', how = "inner")
   
    left = pd.merge(students, grades, on = 'StudentID', how = "left")
    
    right = pd.merge(students, grades, on = 'StudentID', how = "right")
    return jsonify({
        "inner_join": inner.to_dict(orient='records'),
        "left_join": left.to_dict(orient='records'),
        "right_join": right.to_dict(orient='records')
    })
   

@app.route('/math_above_90', methods = ['GET'])
def math_above_90():
    global students, courses, enrollments, grades, CourseDept, StudentDept
    math_high = merge[(merge["CourseDept"] == "Mathematics") & (merge["Grade"] > 90)]
    return jsonify(math_high.to_dict(orient='records'))


@app.route('/total_marks', methods = ['GET'])
def greater_than_50():
    global students, courses, enrollments, grades
    high_total = total[total["TotalMarks"] > 250]
    return jsonify(high_total.to_dict(orient='records'))

@app.route('/rank_students', methods = ['GET'])
def rank_students():
    global ranking, students, courses, enrollments, grades
    ranking = average.sort_values(by="AverageMarks", ascending=False).reset_index(drop=True)
    return jsonify(ranking.to_dict(orient='records'))

@app.route('/letter_grade', methods = ['GET'])
def grades_assigned():
    global merge, students, courses, enrollments, grades
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
    merge.drop_duplicates(inplace = True)
    merge.to_csv("all_data.csv", index=False)
    return jsonify(merge[['Name', 'CourseName', 'Grade', 'letter_grade']].to_dict(orient='records'))

@app.route('/top_3',methods = ['GET'])
def top_3_performers():
    global ranking, students, courses, enrollments, grades
    top_3 = ranking.head(3)
    return jsonify(top_3.to_dict(orient='records'))

@app.route('/pass_fail',methods = ['GET'])
def pass_fail_count():
    global merge, students, courses, enrollments, grades
    merge['Result'] = merge['Grade'].apply(lambda X : "Pass" if X >= 40 else "Fail")
    merge.drop_duplicates(inplace=True)
    return jsonify(merge['Result'].value_counts().to_dict(orient='records'))

@app.route('/top_subject',methods = ['GET'])
def top_subject():
    global students, courses, enrollments, grades
    top_subject = course_result.sort_values(by="average", ascending=False).head(1)
    return jsonify(top_subject.to_dict(orient='records'))

@app.route('/dept_topper', methods = ['GET'])
def department_topper():
    global students, courses, enrollments, grades
    department_max = merge.groupby("StudentDept")["Grade"].max().reset_index()
    toppers = pd.merge(department_max, merge, on=["StudentDept", "Grade"], how="left")
    merge.drop_duplicates(inplace=True)
    toppers = toppers[["StudentDept", "Name", "Grade"]].drop_duplicates()    
    return jsonify(toppers.to_dict(orient='records'))

@app.route('/tough_subject', methods = ['GET'])
def subject_tough():
    global tough_sub, students, courses, enrollments, grades
    merge['Result'] = merge['Grade'].apply(lambda x: "Pass" if x >= 40 else "Fail")
    tough_sub = merge[merge["Result"] == "Fail"].groupby("CourseName")["Result"].count().sort_values(ascending=False)
    max_fail = tough_sub.max()
    top_subjects = tough_sub[tough_sub == max_fail].reset_index()
    return jsonify(top_subjects.to_dict(orient='records'))

# while True:
#     print('1.Load Data\n2.Small julluk of each Data Set\n3.Shape of Each Data Set\n4.Count of Null values in your Dataset\n5.Fill 0 with Null Values\n6.Drop Duplicates\n7.See Inner, Left and Right join of Students and Marks Dataset\n8.Total marks across subjects\n9.Average marks per student\n10. highest, lowest, and average marks\n11.above 90 in Math.\n12. total marks greater than 250.\n13.Rank students\n14.Grades\n15.top 3 performers\n16.Count how many students got "Pass" and "Fail"\n17.highest overall average score.\n18.Department Toppers\n19.Tough Subject\n20.Exit')
#     user_input = int(input("Enter Your choice: "))
#     if user_input == 20:  # Exit option
#         break
#     match user_input:
#         case 1: data_load()
#         case 2: head_data()
#         case 3: data_set_shape()
#         case 4: count_of_null_values()
#         case 5: fill_0_with_null_values()
#         case 6: drop_duplicates(inplace=True)
#         case 7: joins()
#         case 8: print(total)
#         case 9: print(average)
#         case 10: print(course_result)
#         case 11: math_above_90()
#         case 12: greater_than_50()
#         case 13: rank_students()
#         case 14: grades_assigned()
#         case 15: top_3_performers()
#         case 16: pass_fail_count()
#         case 17: top_subject()
#         case 18: department_topper()
#         case 19: subject_tough()
#         case _: print("Invalid choice, please try again!")