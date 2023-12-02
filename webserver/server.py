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
    column_names = get_column_names("student")
    try:
        student = cursor.fetchall()[0]
        result = jsonify(dict(zip(column_names, student)))
        conn.close()
        return result
    except IndexError:
        result = jsonify(dict(zip(column_names, [None,None,None,None])))
        conn.close()
        return result


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
        