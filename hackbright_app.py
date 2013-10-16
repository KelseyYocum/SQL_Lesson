import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone() #returns a tuple that is one line from database
    return row
    # if row == None:
    #     return "No student by that name."
    # else:
    #     return """\
    #     Student: %s %s
    #     Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()


def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" %(first_name, last_name)

def search_by_project(project_title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title =?"""
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    return row
    # if row == None:
    #     print "No project found by that name."
    # else:
    #     print """\
    #     Project: %s
    #     description: %s
    #     max_grade: %d"""%(row[0], row[1], row[2]) 

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s %s" % (title, description, max_grade)

def search_for_project_grade(project_title):
    query = """SELECT first_name, last_name, project_title, grade FROM Students JOIN Grades ON (github = student_github) WHERE project_title = ?"""
    DB.execute(query, (project_title,))
    rows = DB.fetchall()
    return rows
    # if rows == []:
    #     print "No projects found by that name."
    # else:
    #     for row in rows:
    #         print """\
    #         First Name: %s
    #         Project: %s
    #         Grade: %d"""%(row[0], row[1], row[2])

def give_grade (first_name, last_name, project_title, grade):
    github = """SELECT github FROM Students WHERE first_name=? AND last_name=?"""
    DB.execute(github, (first_name, last_name))
    row = DB.fetchone()
    stu_github = row[0]
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (stu_github, project_title, grade))
    CONN.commit()
    print "Successfully gave grade of %s for %s." %(grade, project_title)



def show_grades(first_name, last_name):
    query = """SELECT first_name, last_name, project_title, grade FROM Students LEFT JOIN Grades ON (github = student_github) WHERE first_name = ? AND last_name = ?"""
    DB.execute(query, (first_name, last_name))
    rows = DB.fetchall()
    return rows
    # if rows == []:
    #     print "That student does not exist"
    # else:
    #     for row in rows:
    #         print """\
    #         First Name: %s
    #         Last Name: %s
    #         Project Title: %s
    #         Grade: %r"""%(row[0],row[1],row[2],row[3])

def main():
    connect_to_db()
    command = None
    give_grade("Mica", "Megan", "Cake", 40)
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            search_by_project(*args)
        elif command == "new_project":
            title = args[0]
            description_string = ' '.join(args[1:-1])
            max_grade = args[-1]
            make_new_project(title, description_string, max_grade)
        elif command == "project_grade":
            search_for_project_grade(*args)
        elif command == "give_grade":
            give_grade(*args)
        elif command == "show_grades":
            show_grades(*args)
    CONN.close()


if __name__ == "__main__":
    main()
