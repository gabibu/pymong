

def adaptCreateStudentRequest(createStudentRequest):
    return createStudentRequest['name'],  createStudentRequest['age'], createStudentRequest['studentId']

def adaptCreateCourseRequestRequest(createCourseRequest):

    return createCourseRequest['name'], createCourseRequest['points']

def adaptUpdateStudentRequest(updateStudentRequest):

    fields = {}
    if 'name' in updateStudentRequest:
        fields['name'] = updateStudentRequest['name']

    if 'age' in updateStudentRequest:
        fields['age'] = updateStudentRequest['age']

    if 'studentId' in updateStudentRequest:
        fields['_id'] = updateStudentRequest['studentId']

    return fields

def adaptAssinCourseToStudent(request):
    return request['studentId'], request['courseId']


def adaptGradeStudent(request):
    return request['studentId'], request['courseId'], request['grade']

def adaptUpdateCourseRequest(updateCourseRequest):

    fields = {}
    if 'name' in updateCourseRequest:
        fields['name'] = updateCourseRequest['name']

    if 'points' in updateCourseRequest:
        fields['points'] = updateCourseRequest['points']

    if 'courseId' in updateCourseRequest:
        fields['_id'] = updateCourseRequest['courseId']

    return fields

def adaptToCourseDetails(course):
    if course is not None:
        courseDetails = {}
        courseDetails['courseId'] = str(course['_id'])
        courseDetails['name'] = course['name']
        courseDetails['points'] = course['points']
    else:
        courseDetails = None

    return courseDetails


def adaptStudentToStudentDetails(student):

    if student is not None:
        studentDetails = {}
        studentDetails['age'] = student['age']
        studentDetails['name'] = student['name']
        studentDetails['studentId'] = student['_id']
        studentDetails['coursesGrades'] = student['coursesGrades']
    else:
        studentDetails = None

    return studentDetails





