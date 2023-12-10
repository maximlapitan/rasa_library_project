from flask import Flask, request, jsonify, redirect
from os.path import isfile
import sqlite3

app = Flask(__name__)
file_location = ""
if isfile("webserver/server_data/electives_description.db"):
    file_location = "webserver/server_data/electives_description.db"

if isfile("server_data/electives_description.db"):
    file_location = "server_data/electives_description.db"


@app.get("/test")
def testfunc():
    return "Success, the server is up and running, rasa is requesting as expected"


@app.get("/languages/faq")
def faq_func():
    # return redirect("https://www.th-deg.de/Studierende/AWP-Sprachkurse/FAQ_EN.pdf")
    return "https://www.th-deg.de/Studierende/AWP-Sprachkurse/FAQ_EN.pdf"


def get_column_names(table_name):
    conn = sqlite3.connect(file_location)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    column_info = cursor.fetchall()
    column_names = [info[1] for info in column_info]
    conn.close()
    return column_names


@app.get('/student/<int:student_id>')
def get_student_by_id(student_id):
    conn = sqlite3.connect(file_location)
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
        result = jsonify(dict(zip(column_names, [None, None, None, None])))
        conn.close()
        return result


@app.get("/languages/levels/<ll_value>")
def give_info_by_level(ll_value):
    conn = sqlite3.connect(file_location)
    cursor = conn.cursor()
    columns = ["elective_name", "link"]
    cursor.execute(
        f'select {",".join(columns)} from electives where lower(elective_name) like "%{ll_value}%" and cathegory="german";')
    conn.commit()
    column_names = [column for column in get_column_names(
        "electives") if column in columns]
    electives = cursor.fetchall()
    result = [dict(zip(column_names, elective)) for elective in electives]
    print(electives)
    conn.close()
    return result


@app.get("/exams/<exam>")
def give_info_by_exam(exam):
    conn = sqlite3.connect(file_location)
    cursor = conn.cursor()
    columns = ["name", "link", "Notes"]
    cursor.execute(
        f'select {",".join(columns)} from side_exam where lower(name)="{exam}";')
    conn.commit()
    column_names = [column for column in get_column_names(
        "side_exam") if column in columns]
    electives = cursor.fetchall()
    result = [dict(zip(column_names, elective)) for elective in electives]
    print(electives)
    conn.close()
    return result


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
