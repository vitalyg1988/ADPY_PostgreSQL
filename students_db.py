import psycopg2


NAME_DB = 'dbname=adpy_students'


def create_db():
    with psycopg2.connect(NAME_DB) as conn:
        with conn.cursor() as curs:
            curs.execute("""CREATE TABLE IF NOT EXISTS Students(
                                            id serial PRIMARY KEY,
                                            name varchar(100),
                                            gpa numeric(10, 2),
                                            birth timestamp with time zone); """)

            curs.execute("""CREATE TABLE IF NOT EXISTS Courses(
                                            id serial PRIMARY KEY,
                                            name varchar(100)); """)

            curs.execute("""CREATE TABLE IF NOT EXISTS Student_course(
                                            id serial PRIMARY KEY,
                                            student_id integer REFERENCES Students(id) ON DELETE CASCADE,
                                            course_id integer REFERENCES Courses(id)) ON DELETE CASCADE; """)


def add_new_student(student, cur):
    cur.execute("""INSERT INTO students (name, gpa, birth) VALUES (%s, %s, %s) RETURNING id;""",
                (student['name'], student['gpa'], student['birth']))
    return cur.fetchone()


def add_student(student):
    with psycopg2.connect(NAME_DB) as conn:
        with conn.cursor() as curs:
            return add_new_student(student, curs)


def get_students(student_id):
    with psycopg2.connect(NAME_DB) as conn:
        with conn.cursor() as curs:
            curs.execute("""SELECT * FROM students WHERE students.id = (%s);""", (student_id,))
            return curs.fetchone()


def add_students(course_id, students):
    with psycopg2.connect(NAME_DB) as conn:
        with conn.cursor() as curs:
            curs.execute("""SELECT * FROM courses WHERE course.id= (%s);""", (course_id,))

            if not curs.fetchone():
                return f'Курс id {course_id} отсутвует'

            for student in students:
                curs.execute("""INSERT INTO student_course (student_id, course_id) values (%s, %s)""",
                             (add_new_student(student, curs), course_id))


def get_students(course_id):
    with psycopg2.connect(NAME_DB) as conn:
        with conn.cursor() as curs:
            curs.execute("""SELECT students.name, courses.name FROM students
                        JOIN student_course on student_course.student_id = student.id
                        JOIN course on course.id = (%s)""", (course_id,))
            return curs.fetchall()

if __name__ == '__main__':
    get_students()
