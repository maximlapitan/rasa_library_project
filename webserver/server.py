from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/test")
def testfunc():
    return "Success"

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
            
        