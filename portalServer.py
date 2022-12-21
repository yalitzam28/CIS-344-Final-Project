from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
from portalDatabase import Database
import cgi

class PortalServer(BaseHTTPRequestHandler):
    
    def __init__(self, *args):
        self.database = Database()
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        try:
            if self.path == '/addStudent':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                student_name     = form.getvalue("sname")
                student_courseid = int(form.getvalue("courseid"))
                student_grade    = float(form.getvalue("sgrade"))
                ##Call the Database Method to a add a new student
                '''
                    Example call: self.database.addStudent(student_name, student_courseid,student_grade)
                '''

                self.database.addStudent(student_name, student_courseid,student_grade)

                print("grabbed values",student_name, student_courseid,student_grade)
                self.wfile.write(b"<html><head><title> Teacher's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Teacher's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                    <a href='/addStudent'>Add Student</a>|\
                                    <a href='/addCourse'>Add Course</a>|\
                                    <a href='/searchStudent'>Search Student Name</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Student have been added</h3>")
                self.wfile.write(b"<div><a href='/addStudent'>Add A New Student</a></div>")
                self.wfile.write(b"</center></body></html>")
  
            if self.path == '/addCourse':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                course_name     = form.getvalue("cname")
                self.database.addCourse(course_name)

                self.wfile.write(b"<html><head><title> Teacher's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Teacher's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                    <a href='/addStudent'>Add Student</a>|\
                                    <a href='/addCourse'>Add Course</a>|\
                                    <a href='/searchStudent'>Search Student Name</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Course have been added</h3>")
                self.wfile.write(b"<div><a href='/addCourse'>Add A New Course</a></div>")
                self.wfile.write(b"</center></body></html>")

            if self.path == '/searchStudent':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                searchParam = form.getvalue("sparam")
                searchResult = self.database.searchStudent(searchParam)

                self.wfile.write(b"<html><head><title> Teacher's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Teacher's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                    <a href='/addStudent'>Add Student</a>|\
                                    <a href='/addCourse'>Add Course</a>|\
                                    <a href='/searchStudent'>Search Student Name</a></div>")

                self.wfile.write(b"<hr><h2>All Students with name containing '")
                self.wfile.write(str(searchParam).encode())
                self.wfile.write(b"'</h2>")

                self.wfile.write(b"<table border=2> \
                                    <tr><th>Student Name </th>\
                                        <th> Student ID </th>\
                                        <th> Course Name </th>\
                                        <th> Grade </th></tr>")
                for row in searchResult:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td></tr>')
                
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

        return


    def do_GET(self):
        try:

            if self.path == '/':
                data=[]
                records = self.database.getAllStudents()
                courses = self.database.getAllCourse()
                for record in records:
                    data=record.fetchall()

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Teacher's Portal </title></head>")
                self.wfile.write(b"<body>")
                
                self.wfile.write(b"<center><h1>Teacher's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addStudent'>Add Student</a>|\
                                  <a href='/addCourse'>Add Course</a>|\
                                  <a href='/searchStudent'>Search Student Name</a></div>")
                self.wfile.write(b"<hr><h2>All Students With Grade</h2>")
                self.wfile.write(b"<table border=2> \
                                    <tr><th>Student Name </th>\
                                        <th> Student ID </th>\
                                        <th> Course Name </th>\
                                        <th> Grade </th></tr>")
                for row in data:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[5]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td></tr>')
                
                self.wfile.write(b"</table>")
                self.wfile.write(b"<hr><h2>All Courses</h2>")
                self.wfile.write(b"<table border=2> \
                                    <tr><th>Course Name </th></tr>")

                for row in courses:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td></tr>')
                
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/addStudent':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Teacher's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Teacher's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addStudent'>Add Student</a>|\
                                  <a href='/addCourse'>Add Course</a>|\
                                  <a href='/searchStudent'>Search Student Name</a></div>")
                self.wfile.write(b"<hr><h2>Add New Student</h2>")

                self.wfile.write(b"<form action='/addStudent' method='post'>")
                self.wfile.write(b'<label for="sname">Student Name:</label>\
                      <input type="text" id="sname" name="sname"><br><br>\
                      <label for="courseid">course id:</label>\
                      <input type="number" id="courseid" name="courseid"><br><br>\
                      <label for="sgrade">Grade:</label>\
                      <input type="text" id="sgrade" name="sgrade"><br><br>\
                      <input type="submit" value="Submit">\
                      </form>')
                
                self.wfile.write(b"</center></body></html>")
                return
            if self.path == '/addCourse':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Teacher's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Teacher's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addStudent'>Add Student</a>|\
                                  <a href='/addCourse'>Add Course</a>|\
                                  <a href='/searchStudent'>Search Student Name</a></div>")
                self.wfile.write(b"<hr><h2>Add New Course</h2>")

                self.wfile.write(b"<form action='/addCourse' method='post'>")
                self.wfile.write(b'<label for="cname">Course Name:</label>\
                      <input type="text" id="cname" name="cname"><br><br>\
                      <input type="submit" value="Submit">\
                      </form>')

                self.wfile.write(b"</center></body></html>")
                return
            
            if self.path =='/searchStudent':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Teacher's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Teacher's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addStudent'>Add Student</a>|\
                                  <a href='/addCourse'>Add Course</a>|\
                                  <a href='/searchStudent'>Search Student Name</a></div>")
                self.wfile.write(b"<hr><h2>Search Student</h2>")

                self.wfile.write(b"<form action='/searchStudent' method='post'>")
                self.wfile.write(b'<label for="sparam">Student Name:</label>\
                      <input type="text" id="sparam" name="sparam"><br><br>\
                      <input type="submit" value="Submit">\
                      </form>')

                self.wfile.write(b"</center></body></html>")
                return

            if self.path =='/modifyStudent':
                return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
            
def run(server_class=HTTPServer, handler_class=PortalServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()
    
run()
