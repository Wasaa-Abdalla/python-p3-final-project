#Providing interface for connecting to an sqlite database
import sqlite3

#function to connect an SQLite database specified by the filepath 'db_file'
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    
    return conn

#Execute sql statement for creating a specified table & prints error if theres one
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

#Insert or replaces data into a specified table
def insert_data(conn, table, data):
    """ Insert new data into the table or replace if it already exists
    """
    placeholders = ", ".join(["?"] * len(data))
    sql = f'INSERT OR REPLACE INTO {table} VALUES ({placeholders})'
    try:
        c = conn.cursor()
        c.execute(sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

#queries the database to join three tables i.e. students, courses & grades
def get_student_grades(db_file):
    """
    Query grades for each student per course
    """
    conn = create_connection(db_file)
    if conn is not None:
        cursor = conn.cursor()

        # SQL query to join the three tables
        query = '''
        SELECT 
            students.student_name, 
            courses.course_name, 
            grades.grade 
        FROM 
            grades 
        INNER JOIN students ON students.student_id = grades.student_id
        INNER JOIN courses ON courses.course_id = grades.course_id;
        '''

        try:
            cursor.execute(query)
            all_grades = cursor.fetchall()
            for grade in all_grades:
                print(f"Student Name: {grade[0]}, Course: {grade[1]}, Grade: {grade[2]}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
    else:
        print("Error! cannot create the database connection.")

#queries the database to determine which courses each student is taking
def get_student_courses(db_file):
    """
    Query courses for each student
    """
    # create a database connection
    conn = create_connection(db_file)
    if conn is not None:
        cursor = conn.cursor()

        # SQL query to join the tables and retrieve the courses each student is taking
        query = '''
        SELECT 
            students.student_name, 
            courses.course_name
        FROM 
            students
        JOIN grades ON students.student_id = grades.student_id
        JOIN courses ON courses.course_id = grades.course_id;
        '''

        try:
            cursor.execute(query)
            student_courses = cursor.fetchall()
            for student_course in student_courses:
                print(f"Student Name: {student_course[0]}, Course: {student_course[1]}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
    else:
        print("Error! cannot create the database connection.")


# main code block
def main():
    database = 'school_performance.db'  #creates a database with the name schoo_performance.db
    
    sql_create_students_table = '''CREATE TABLE IF NOT EXISTS students (
                                      student_id INTEGER PRIMARY KEY,
                                      student_name TEXT NOT NULL,
                                      student_email TEXT UNIQUE NOT NULL
                                  );'''
    
    sql_create_courses_table = '''CREATE TABLE IF NOT EXISTS courses (
                                     course_id INTEGER PRIMARY KEY,
                                     course_name TEXT NOT NULL,
                                     course_teacher TEXT NOT NULL
                                 );'''
    
    sql_create_grades_table = '''CREATE TABLE IF NOT EXISTS grades (
                                    student_id INTEGER,
                                    course_id INTEGER,
                                    grade TEXT NOT NULL,
                                    PRIMARY KEY (student_id, course_id),
                                    FOREIGN KEY (student_id) REFERENCES students (student_id),
                                    FOREIGN KEY (course_id) REFERENCES courses (course_id)
                                );'''
    
    # create a database connection
    conn = create_connection(database)
    
    # create tables
    if conn is not None:
        create_table(conn, sql_create_students_table)
        create_table(conn, sql_create_courses_table)
        create_table(conn, sql_create_grades_table)
        
        # Function for creating new students into the database
        student_data = (4, 'Ralph Bunche', 'ralph.bunche@moringa.com')
        insert_data(conn, 'students', student_data)
        
        # Function for creating course information in the database
        course_data = (4, 'Python Programmng', 'Mr. White')
        insert_data(conn, 'courses', course_data)
        
        # insert grades i the database
        grades_data = (4, 4, "A")  
        insert_data(conn, 'grades', grades_data)

        grades_data =(4, 2, "C")
        insert_data(conn, 'grades', grades_data)
        
        # Close the database connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()


#printing students name & performance
get_student_grades('school_performance.db')

#printing students courses
get_student_courses('school_performance.db')

#the printing part of the code prints the students details, courses they are taking and the grades they have gotten per course
