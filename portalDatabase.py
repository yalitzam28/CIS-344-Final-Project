import mysql.connector
from mysql.connector import Error


class Database():
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="teachers_portal",
                 user='root',
                 password='MySQLServer23@#'):

        self.host       = host
        self.port       = port
        self.database   = database
        self.user       = user
        self.password   = password
        self.connection = None
        self.cursor     = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host         = self.host,
                port         = self.port,
                database     = self.database,
                user         = self.user,
                password     = self.password)
            
            if self.connection.is_connected():
                return
        except Error as e:
            print("Error while connecting to MySQL", e)
    

    def getAllStudents(self):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            self.cursor.callproc("studentsWithGrade")
            records = self.cursor.stored_results()
            return records

    def getAllCourse(self):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = ("SELECT courseName FROM courses")
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def addStudent(self, name, courseID,grade=0):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()

            add_student = ("INSERT INTO students  "
               "(studentName, enrolledInCourseID, grade) "
               "VALUES (%s, %s, %s)")

            data_student = (name, courseID, grade)

            self.cursor.execute(add_student, data_student)  
            self.connection.commit()
        pass

    def addCourse(self, name):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()

            add_course = f"INSERT INTO courses (courseName) VALUE ('{name}')"

            self.cursor.execute(add_course)  
            self.connection.commit()
        pass

    def searchStudent(self, searchParam):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            search_student = ("SELECT st.studentId, st.studentName, c.courseName, st.grade FROM teachers_portal.students st "
            "LEFT JOIN teachers_portal.courses c ON st.enrolledInCourseID = c.courseId "
            f"WHERE st.studentName LIKE '%{searchParam}%'")
            self.cursor.execute(search_student)
            records = self.cursor.fetchall()
            return records
        pass
    
    def modifyGrade(self, studentID, grade):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            update_student_grade = "UPDATE students SET grade = %s WHERE student_id = %s"
            values = (studentID, grade)
            self.cursor.execute(update_student_grade, values)  
            self.connection.commit()
        pass
        
        
        
    
    
