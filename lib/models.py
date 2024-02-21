from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    student_name = Column(String, nullable=False)
    student_email = Column(String, nullable=False, unique=True)
    grades = relationship('Grade', back_populates='student')

    def __repr__(self):
        return f"<Student(name={self.student_name}, email={self.student_email})>"

class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False)
    course_teacher = Column(String, nullable=False)
    grades = relationship('Grade', back_populates='course')

    def __repr__(self):
        return f"<Course(name={self.course_name}, teacher={self.course_teacher})>"

class Grade(Base):
    __tablename__ = 'grades'

    student_id = Column(Integer, ForeignKey('students.student_id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)
    grade = Column(Text, nullable=False)
    student = relationship('Student', back_populates='grades')
    course = relationship('Course', back_populates='grades')

    def __repr__(self):
        return f"<Grade(student_id={self.student_id}, course_id={self.course_id}, grade={self.grade})>"


# create an engine that stores data in the local directory's school_performance.db file.
engine = create_engine('sqlite:///school_performance.db')

# create all tables in the engine
Base.metadata.create_all(engine)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a session
session = Session()

# add and commit objects to the session

#Function for adding students data into the table, checks whether theres an existing student with the same data& can print an error message
new_student_email = 'john.doe@example.com'
existing_student = session.query(Student).filter_by(student_email=new_student_email).first()
if existing_student is None:
    new_student = Student(student_name='John Doe', student_email=new_student_email)
    session.add(new_student)
    session.commit()
else:
    new_student = existing_student
    print(f"Student with email {new_student_email} already exists.")

#function for creating new courses for the students
new_course = Course(course_name='Mathematics', course_teacher='Jane Smith') 
session.add(new_course)
session.commit()  

# Now we have the IDs needed for the Grade
new_grade = Grade(student_id=new_student.student_id, course_id=new_course.course_id, grade='A')
session.add(new_grade)
session.commit()

# query the database
students = session.query(Student).all()
for student in students:
    print(student)

courses = session.query(Course).all()
for course in courses:
    print(course)

grades = session.query(Grade).all()
for grade in grades:
    print(grade)


#Using lists

#adding new students using lists
students_list = [
    {'student_name': 'Alice Wanja', 'student_email': 'alice.wanja@moringa.com'},
    {'student_name': 'Paul Victor', 'student_email': 'paul.victor@moringa.com'}
]

for student_info in students_list:
    existing_student = session.query(Student).filter_by(student_email=student_info['student_email']).first()
    if existing_student is None:
        new_student = Student(**student_info)
        session.add(new_student)
    else:
        print(f"Student with email {student_info['student_email']} already exists.")

session.commit()


#Using Tuples
#Tuple to represent students grade in a course
student_grade_info = (104, 101, 'B')

# Check if the grade entry already exists
existing_grade = session.query(Grade).filter_by(student_id=student_grade_info[0], course_id=student_grade_info[1]).first()
if existing_grade is None:
    # Create a new Grade object using unpacking
    new_grade = Grade(student_id=student_grade_info[0], course_id=student_grade_info[1], grade=student_grade_info[2])
    # Add the Grade object to the session
    session.add(new_grade)
    # Commit the changes
    session.commit()
else:
    print(f"Grade for student_id {student_grade_info[0]} in course_id {student_grade_info[1]} already exists.")

#Using dictionaries
# Dictionary containing new student data
student_data = {
    'student_name': 'Charlie Green',
    'student_email': 'charlie.green@moringa.com'
}

# Check if the student with the given email already exists
existing_student = session.query(Student).filter_by(student_email=student_data['student_email']).first()
if existing_student is None:
    # Create a new Student object using **kwargs unpacking
    new_student = Student(**student_data)
    # Add the new Student object to the session
    session.add(new_student)
    # Commit the changes
    session.commit()
else:
    print(f"Student with email {student_data['student_email']} already exists.")