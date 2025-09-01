import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv("E:\\learnings\\gsss_sic_\\project\\students.csv")
courses = pd.read_csv("E:\\learnings\\gsss_sic_\\project\\courses.csv")
enrollments = pd.read_csv("E:\\learnings\\gsss_sic_\\project\\enrollments.csv")
grades = pd.read_csv("E:\\learnings\\gsss_sic_\\project\\grades.csv")

#data_frames = [students, courses, enrollments, grades]

#merged_dat_frames = reduce(lambda left, right: pd.merge(left, right, on = "student_id"), data_frames)

print('\n\n',students.head())
print('\n\n',grades.head())

print('\n\n',students.shape)
print('\n\n',courses.shape)
print('\n\n',enrollments.shape)
print('\n\n',grades.shape)

#print('\n\n',merged_dat_frames.head())

# merged_dat_frames.plot(x="name", y=["Math", "Science"], kind="bar", figsize=(8,6))

# plt.title("Final Scores in Math & Science")
# plt.xlabel("Students")
# plt.ylabel("Scores")
# plt.legend(title="Subjects")
# plt.show()

# totals = merged_dat_frames[["Math", "Science"]].sum()

# # Plot pie chart
# plt.pie(totals, labels=totals.index, autopct="%1.1f%%", startangle=90)
# plt.title("Overall Subject Distribution in Class")
# plt.show()


print('\n\n',students.isnull().sum())
print('\n\n',courses.isnull().sum())
print('\n\n',enrollments.isnull().sum())
print('\n\n',grades.isnull().sum())

students = students.fillna(0)
courses = courses.fillna(0)
enrollments = enrollments.fillna(0)
grades = grades.fillna(0)

students = students.drop_duplicates()
courses = courses.drop_duplicates()
enrollments = enrollments.drop_duplicates()
grades = grades.drop_duplicates()

joins = pd.merge(students, grades, on = 'StudentID', how = "inner")
print('\n\n',joins)

left_joins = pd.merge(students, grades, on = 'StudentID', how = "left")
print('\n\n',left_joins)

right_joins = pd.merge(students, grades, on = 'StudentID', how = "right")
print('\n\n',right_joins)


students.rename(columns={"Department": "StudentDept"}, inplace=True)
courses.rename(columns={"Department": "CourseDept"}, inplace=True)

merge = pd.merge(enrollments, students, on="StudentID", how="left")
merge = pd.merge(merge, courses, on="CourseID", how="left")
merge = pd.merge(merge, grades, on=["StudentID", "CourseID"], how="left")
merge = merge.drop_duplicates()
print('\n\n',merge)

total = merge.groupby("Name")["Grade"].sum().reset_index(name="TotalMarks")
average = merge.groupby("Name")["Grade"].mean().reset_index(name="AverageMarks")
course_result = merge.groupby("CourseName")["Grade"].agg(highest="max", lowest="min", average="mean")
print('\n\n',total)
print('\n\n',average)
print('\n\n',course_result)

math_high = merge[(merge["CourseDept"] == "Mathematics") & (merge["Grade"] > 90)]
print('\nthis is math high\n',math_high)

high_total = total[total["TotalMarks"] > 250]
print('\n\n',high_total)

ranking = average.sort_values(by="AverageMarks", ascending=False).reset_index(drop=True)
print('\n\n',ranking)

merge['Result'] = merge['Grade'].apply(lambda X : "Pass" if X >= 40 else "Fail")
merge = merge.drop_duplicates()
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
print('merge with grade')
print(merge[["Name","CourseName","Grade","letter_grade"]])
merge = merge.drop_duplicates()
merge.to_csv("all_data.csv", index=False)
print(merge)

top_3 = ranking.head(3)
print('\n\n',"Top 3 performers:")
print('\n\n',top_3)

pass_fail_counts = merge['Result'].value_counts()
print('\n\n',"\nPass/Fail counts:")
print('\n\n',pass_fail_counts)

top_subject = course_result.sort_values(by="average", ascending=False).head(1)
print('\n\n',"\nSubject with highest overall average score:")
print('\n\n',top_subject)