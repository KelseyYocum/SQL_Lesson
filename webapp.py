from flask import Flask, render_template, request, redirect
import hackbright_app

app = Flask(__name__)

#code goes here

@app.route("/")
def get_github ():
    return render_template("index.html")


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_name = request.args.get("student_name").split()
    list_of_rows = hackbright_app.show_grades(student_name[0], student_name[1])
    if list_of_rows == []:
        return render_template("index.html")
    return render_template("student_info.html", first_name=student_name[0],
                                                last_name = student_name[1],
                                                list_of_rows = list_of_rows)

# click a project name and it returns a page listing all students and their grades for that project
#SELECT first_name, last_name, project_title, grade
@app.route("/project")
def get_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("title")
    list_of_rows = hackbright_app.search_for_project_grade(project_title)
    project_details = hackbright_app.search_by_project(project_title)
    html = render_template("get_project.html", list_of_rows=list_of_rows,
                                                project_details=project_details)

    return html

@app.route("/new_student", methods=['POST'])
def add_student():
    hackbright_app.connect_to_db()
    student_name = request.form.get("student_name").split()
    github = request.form.get("github")
    hackbright_app.make_new_student(student_name[0], student_name[1], github)
    return redirect("/student?student_name=%s" %" ".join(student_name))

@app.route("/new_project")
def add_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    project_description = request.args.get("project_description")
    max_grade = request.args.get("max_grade")
    hackbright_app.make_new_project(project_title, project_description, max_grade)
    # return render_template("index.html")
    return redirect("/project?title=%s" %project_title)


@app.route("/give_grade")
def give_grade():
    hackbright_app.connect_to_db()
    #first_name, last_name, project_title, grade
    student_name = request.args.get("student_name").split()
    project_title = request.args.get("project_title")
    grade = request.args.get("grade")
    hackbright_app.give_grade(student_name[0], student_name[1], project_title, grade)
    return redirect("/student?student_name=%s" %" ".join(student_name))


if __name__ == "__main__":
    app.run(debug=True)
