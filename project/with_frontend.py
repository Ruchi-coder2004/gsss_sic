import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

students = courses = enrollments = grades = None
merge = total = average = course_result = CourseDept = StudentDept = toppers = ranking = None 

# ----------------------
# Helper utilities
# ----------------------
def compute_totals_if_needed():
    """
    Ensure total, average and course_result are computed from merge.
    This does not change existing logic — it only computes when those globals are None.
    """
    global total, average, course_result, merge
    if merge is None:
        return
    if total is None or average is None or course_result is None:
        try:
            total = merge.groupby("Name")["Grade"].sum().reset_index(name="TotalMarks")
            average = merge.groupby("Name")["Grade"].mean().reset_index(name="AverageMarks")
            course_result = merge.groupby("CourseName")["Grade"].agg(
                highest="max", lowest="min", average="mean"
            ).reset_index()
        except Exception:
            # keep existing values if grouping fails
            total = total or pd.DataFrame()
            average = average or pd.DataFrame()
            course_result = course_result or pd.DataFrame()

def safe_jsonify_from_df(df):
    """
    Convert DataFrame to list-of-dicts; ensure at least one row is returned so frontend
    table renderer always has something to show.
    """
    try:
        if isinstance(df, pd.Series):
            df = df.reset_index()
        if not isinstance(df, pd.DataFrame):
            # try to convert if possible
            df = pd.DataFrame(df)
    except Exception:
        df = pd.DataFrame()

    rows = df.to_dict(orient='records') if not df.empty else []
    if not rows:
        # return a harmless placeholder row (frontend will display it)
        return jsonify([{"info": "No data available"}])
    return jsonify(rows)

# ----------------------
# Routes
# ----------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload_files():  
    global students, courses, enrollments, grades, merge, total, average, course_result
    try:
        required_files = ['students', 'courses', 'enrollment', 'grade']
        for f in required_files:
            if f not in request.files:
                return jsonify({"status": "error", "message": f"Missing file: {f}"}), 400
            
        students = pd.read_csv(request.files['students'])
        courses = pd.read_csv(request.files['courses'])
        enrollments = pd.read_csv(request.files['enrollment'])
        grades = pd.read_csv(request.files['grade'])

        for i in [students, courses, enrollments, grades]:
            i.fillna(0, inplace = True)
            i.drop_duplicates(inplace = True)

        students.rename(columns={"Department": "StudentDept"}, inplace=True)
        courses.rename(columns={"Department": "CourseDept"}, inplace=True)

        # merge all datasets (keeps original logic)
        merge = pd.merge(enrollments, students, on="StudentID", how="left")
        merge = pd.merge(merge, courses, on="CourseID", how="left")
        merge = pd.merge(merge, grades, on=["StudentID", "CourseID"], how="left")
        #print(merge)
        merge.drop_duplicates(inplace=True)

        # compute derived frames (keeps original logic)
        total = merge.groupby("Name")["Grade"].sum().reset_index(name="TotalMarks")
        average = merge.groupby("Name")["Grade"].mean().reset_index(name="AverageMarks")
        course_result = merge.groupby("CourseName")["Grade"].agg(highest="max", lowest="min", average="mean").reset_index()

        return jsonify({"status": "Success","message":"Files uploaded and Processed!"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def ensure_data_loaded():
    # keep original response structure
    if merge is None:
        return False, jsonify({"status": "error", "message": "Please upload data first."}), 400
    return True, None, None

@app.route('/data_header', methods=['GET'])
def head_data():
    global merge
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code    
    # global students, courses, enrollments, grades
    return jsonify({
        "students": students.head().to_dict(orient='records'),
        "courses": courses.head().to_dict(orient='records'),
        "enrollments": enrollments.head().to_dict(orient='records'),
        "grades": grades.head().to_dict(orient='records')
    })

@app.route('/data_size', methods=['GET'])
def data_set_shape():
    global merge
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code
    data = [
        {"Dataset": "Students", "Rows": students.shape[0], "Columns": students.shape[1]},
        {"Dataset": "Courses", "Rows": courses.shape[0], "Columns": courses.shape[1]},
        {"Dataset": "Enrollments", "Rows": enrollments.shape[0], "Columns": enrollments.shape[1]},
        {"Dataset": "Grades", "Rows": grades.shape[0], "Columns": grades.shape[1]},
    ]
    return jsonify(data)

@app.route('/null_values', methods=['GET'])
def count_of_null_values():
    global merge
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code
    data = []
    for name, df in [("Students", students), ("Courses", courses), ("Enrollments", enrollments), ("Grades", grades)]:
        nulls = int(df.isnull().sum().sum())  # convert numpy ints to native int for JSON
        data.append({"Dataset": name, "Total Null Values": nulls})
    return jsonify(data)


# def fill_0_with_null_values():
#     global students, courses, enrollments, grades
    

# def drop_duplicates(inplace=True):
#     global students, courses, enrollments, grades
    
@app.route('/joins',methods=['GET'])
def joins():
    global merge
    # global students, courses, enrollments, grades
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code

    inner = pd.merge(students, grades, on='StudentID', how="inner")
    left  = pd.merge(students, grades, on='StudentID', how="left")
    right = pd.merge(students, grades, on='StudentID', how="right")

    # choose the columns you want to show (keep original logic)
    cols = ['StudentID','Name','CourseID','Grade']

    def pick_and_tag(df, tag):
        # keep only available columns to avoid key errors
        sel = [c for c in cols if c in df.columns]
        df2 = df[sel].copy()
        df2['JoinType'] = tag
        return df2

    combined = pd.concat([
        pick_and_tag(inner, 'inner'),
        pick_and_tag(left, 'left'),
        pick_and_tag(right, 'right')
    ], ignore_index=True)

    if combined.empty:
        return jsonify([{"JoinType":"N/A","StudentID":"N/A","Name":"N/A","CourseID":"N/A","Grade":0}])

    return jsonify(combined.to_dict(orient='records'))


@app.route('/math_above_90', methods=['GET'])
def math_above_90():
    global CourseDept, StudentDept, merge
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code
    # keep the original filter logic but return placeholder if empty
    math_high = merge[(merge.get("CourseDept")== "Mathematics") & (merge.get("Grade") > 90)] if not merge.empty else pd.DataFrame()
    if math_high.empty:
        return jsonify([{"Name":"N/A","CourseName":"N/A","Grade":0}])
    return jsonify(math_high.to_dict(orient='records'))


@app.route('/total_marks', methods=['GET'])
def greater_than_50():
    global merge, total, average, course_result
    # global students, courses, enrollments, grades
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code
    
    # compute if needed (keeps original variables & logic)
    compute_totals_if_needed()

    if total is None or (isinstance(total, pd.DataFrame) and total.empty):
        return jsonify([{"Name": "N/A", "TotalMarks": 0}])
    high_total = total.sort_values(by="TotalMarks", ascending=False)
    return jsonify(high_total.to_dict(orient='records'))

@app.route('/rank_students', methods=['GET'])
def rank_students():
    global ranking, merge, total, average, course_result
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code

    compute_totals_if_needed()

    # ranking based on average (keeps original logic)
    if average is None or average.empty:
        return jsonify([{"Name": "N/A", "AverageMarks": 0}])
    ranking = average.sort_values(by="AverageMarks", ascending=False).reset_index(drop=True)
    return jsonify(ranking.to_dict(orient='records'))

@app.route('/letter_grade', methods=['GET'])
def grades_assigned():
    global merge
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code

    # operate on a copy (preserve original merge)
    temp = merge.copy()

    def grade_calculation(x):
        try:
            val = float(x)
        except Exception:
            return "F"
        if val >= 90:
            return "A"
        elif val >= 75:
            return "B"
        elif val >= 60:
            return "C"
        elif val >= 40:
            return "D"
        else:
            return "F"

    temp['letter_grade'] = temp['Grade'].apply(grade_calculation).fillna('F')
    temp.drop_duplicates(inplace=True)

    if temp.empty:
        return jsonify([{"Name":"N/A","CourseName":"N/A","Grade":0,"letter_grade":"N/A"}])

    return jsonify(temp[['Name', 'CourseName', 'Grade', 'letter_grade']].to_dict(orient='records'))


@app.route('/top_3',methods=['GET'])
def top_3_performers():
    global merge, ranking, average
    # global ranking, students, courses, enrollments, grades
    # top_3 = ranking.head(3)
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code

    # compute ranking on the fly if needed (preserve logic)
    compute_totals_if_needed()
    if average is None or average.empty:
        return jsonify([{"Name":"N/A","AverageMarks":0}])
    ranking = average.sort_values(by="AverageMarks", ascending=False).reset_index(drop=True)
    return jsonify(ranking.head(3).to_dict(orient='records'))


@app.route('/pass_fail', methods=['GET'])
def pass_fail_count():
    global merge
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code

    temp = merge.copy()
    temp['Result'] = temp['Grade'].apply(lambda X: "Pass" if X >= 40 else "Fail")
    counts = temp['Result'].value_counts().reset_index()
    counts.columns = ["Result", "Count"]
    if counts.empty:
        return jsonify([{"Result":"N/A","Count":0}])
    return jsonify(counts.to_dict(orient='records'))

@app.route('/top_subject',methods=['GET'])
def top_subject():
    global merge, course_result
    # global students, courses, enrollments, grades
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code

    compute_totals_if_needed()
    if course_result is None or course_result.empty:
        return jsonify([{"CourseName":"N/A","average":0}])
    top_subject = course_result.sort_values(by="average", ascending=False).head(1)
    return jsonify(top_subject.to_dict(orient='records'))

@app.route('/dept_topper', methods=['GET'])
def department_topper():
    global merge
    # global students, courses, enrollments, grades
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code
    if merge is None or merge.empty:
        return jsonify([{"StudentDept":"N/A","Name":"N/A","Grade":0}])
    department_max = merge.groupby("StudentDept")["Grade"].max().reset_index()
    toppers = pd.merge(department_max, merge, on=["StudentDept", "Grade"], how="left")
    merge.drop_duplicates(inplace=True)
    toppers = toppers[["StudentDept", "Name", "Grade"]].drop_duplicates()    
    if toppers.empty:
        return jsonify([{"StudentDept":"N/A","Name":"N/A","Grade":0}])
    return jsonify(toppers.to_dict(orient='records'))

@app.route('/tough_subject', methods=['GET'])
def subject_tough():
    global merge
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code

    temp = merge.copy()
    temp['Result'] = temp['Grade'].apply(lambda x: "Pass" if x >= 40 else "Fail")
    tough_sub = temp[temp['Result'] == 'Fail'].groupby('CourseName').size().reset_index(name='FailCount')

    if tough_sub.empty:
        tough_sub = pd.DataFrame([{"CourseName": "N/A", "FailCount": 0}])

    hardest = tough_sub.sort_values(by="FailCount", ascending=False).head(1)
    return jsonify(hardest.to_dict(orient='records'))

@app.route('/dept_analysis', methods=['GET'])
def department_wise_analysis():
    global merge
    ok, resp, code = ensure_data_loaded()
    if not ok:
        return resp, code
    
    if merge is None or merge.empty:
        return jsonify([{"StudentDept":"N/A","AverageMarks":0,"HighestMarks":0,"LowestMarks":0,"PassCount":0,"FailCount":0}])

    temp = merge.copy()
    temp['Result'] = temp['Grade'].apply(lambda x: "Pass" if x >= 40 else "Fail")

    # Group by Department
    dept_analysis = temp.groupby('StudentDept').agg(
        AverageMarks=('Grade', 'mean'),
        HighestMarks=('Grade', 'max'),
        LowestMarks=('Grade', 'min'),
        PassCount=('Result', lambda x: (x == 'Pass').sum()),
        FailCount=('Result', lambda x: (x == 'Fail').sum())
    ).reset_index()

    if dept_analysis.empty:
        return jsonify([{"StudentDept":"N/A","AverageMarks":0,"HighestMarks":0,"LowestMarks":0,"PassCount":0,"FailCount":0}])

    return jsonify(dept_analysis.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
