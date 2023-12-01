from flask import Flask, request, jsonify

import sqlite3

app = Flask(__name__)

@app.get("/test")
def testfunc():
    return "Success, the server is up and running, rasa is requesting as expected"

def get_column_names(table_name):
    conn = sqlite3.connect('server_data/electives_description.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    column_info = cursor.fetchall()
    column_names = [info[1] for info in column_info]
    conn.close()
    return column_names
    
    
@app.get('/student/<int:student_id>')
def get_student_by_id(student_id):
    conn = sqlite3.connect('server_data/electives_description.db')
    cursor = conn.cursor()
    cursor.execute(f"select * from student where student_mn={student_id};")
    conn.commit()
    student = cursor.fetchall()[0]
    column_names = get_column_names("student")
    result = jsonify(dict(zip(column_names, student)))
    conn.close()
    return result


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)

    # student:
    #     student_mn:
    #     name:
    #     surname:
    #     gpa:
            
    # courses:
    #     course_id:
    #     name:
    #     ects: int
    #     timetable: json text
    #     program: 
        
    # student-course:
    #     student_course_id:
    #     course_id: course_id
    #     student_mn: student_mn
        
    # student_course_status:
    #     student_course_status_id:
    #     student_course_id: student_course_id
    #     status: [ATTENDING, COMPLETED, RETAKE, MUST_BE_TAKEN]
        
    # course_prerequisite:
    #     course_prerequisite_id:
    #     course_wish: course_id
    #     course_to_take: course_id
        
    # faculty:
    #     faculty_id:
    #     name:
            
    # program:
    #     program_id:
    #     faculty_id:
    #     program_name:
            
        