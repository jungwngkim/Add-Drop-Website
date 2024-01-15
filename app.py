from flask import Flask, render_template, redirect, url_for, request, make_response
import re
import secrets

from src.decorators import *
from src.mail import *
from src.student import Student
from src import globals

# Flask App
app = Flask(__name__)

# ==== Student, Teacher ==== #


@app.route("/")
def index():
    return render_template('index.html')

# ==== Student only ==== #


@app.route("/register", methods=["GET", "POST"])
@server_open_required
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        email, name, grade = (
            request.form["student-email"],
            request.form["student-name"],
            request.form["student-grade"],
        )
        email_regex = r"s\d{8}@sjajeju.kr$"

        result = re.match(email_regex, email)

        if not result:
            return render_template("register.html", error_text="Email Error")

        new_student = Student(email, name, int(grade))

        if new_student in globals.waiting_list:
            return render_template("register.html", error_text="Already Registered")

        globals.waiting_list.append(new_student)
        send_email(new_student, EmailType.ON_REGISTER, 'Successful Registration')

        return redirect(url_for("waiting_list_screen"))


@app.route("/waiting-list-screen")
@server_open_required
def waiting_list_screen():
    print(globals.waiting_list[globals.current_index:])
    return render_template(
        'waiting_list.html',
        waiting_list=globals.waiting_list[globals.current_index:],
        priority_list=globals.priority_list,
        current_index=0,
    )


# ==== Teacher only ==== #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        password = request.form['teacher-password']

        if password in globals.password:
            index = globals.password.index(password)
            new_session = secrets.token_hex(32)

            globals.session[index] = new_session

            print(f'new session: {new_session}')

            res = make_response(redirect(url_for('admin')))
            res.set_cookie(globals.session_key, new_session)
            return res
        else:
            return render_template('login.html', error_text='Wrong Password')


@app.get("/admin")
@login_required
def admin():
    return render_template(
        "admin.html",
        waiting_list=globals.waiting_list,
        priority_list=globals.priority_list,
        current_index=globals.current_index,
        is_open=globals.server_is_open,
        admin=True,
    )


@app.route("/next_student")
@login_required
def next_student():
    max_index = len(globals.waiting_list) - 1

    if globals.current_index < max_index:
        globals.current_index += 1

        # send email to first student
        send_email(globals.waiting_list[globals.current_index], EmailType.ON_FIRST, 'You are in First place in waiting line.')

        # send email to tenth student, if exists
        if globals.current_index + 9 <= max_index:
            send_email(globals.waiting_list[globals.current_index + 9], EmailType.ON_TENTH, 'You are in Tenth place in waiting line.')

    return redirect(url_for("admin"))


@app.route("/delete_all_student")
@login_required
def delete_all_student():
    globals.waiting_list.clear()
    globals.current_index = 0

    return redirect(url_for("admin"))


@app.route("/delete_visited_student")
@login_required
def delete_visited_student():
    globals.waiting_list = globals.waiting_list[globals.current_index:]
    globals.current_index = 0

    return redirect(url_for("admin"))

@app.route("/delete_student")
@login_required
def delete_student():
    student_index = int(request.args.get('student_index'))

    if 0 <= student_index < len(globals.waiting_list):
        globals.waiting_list.pop(student_index)
        if globals.current_index > student_index:
            globals.current_index -= 1

    return redirect(url_for("admin"))

@app.route("/prioritize_student")
@login_required
def prioritize_student():
    student_index = int(request.args.get('student_index'))

    if 0 <= student_index < len(globals.waiting_list):
        moved_student = globals.waiting_list.pop(student_index)
        if globals.current_index > student_index:
            globals.current_index -= 1
        
        globals.priority_list.append(moved_student)

    return redirect(url_for("admin"))

@app.route("/delete_prioritized_student")
@login_required
def delete_prioritized_student():
    student_index = int(request.args.get('student_index'))

    if 0 <= student_index < len(globals.priority_list):
        globals.priority_list.pop(student_index)
    
    return redirect(url_for("admin"))


@app.route("/server_toggle")
@login_required
def server_toggle():
    globals.server_is_open = not globals.server_is_open

    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, debug=True)
