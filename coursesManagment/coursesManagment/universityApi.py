from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
import json
from django.views.decorators.csrf import csrf_exempt

from .adapters.ApiAdapter import adaptCreateStudentRequest,\
    adaptStudentToStudentDetails,adaptUpdateStudentRequest, \
    adaptAssinCourseToStudent, adaptGradeStudent


from .dal.studentsDal import __instance

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        m1 = {}
        m1['x'] = 1

        d1 = json.dumps(m1)
        return JSONResponse(d1)


@csrf_exempt
def studentDetails(request):
    if request.method == 'GET':
        studentId = int(request.GET["studentId"])

        student = __instance.studentById(studentId)

        studentDetails = adaptStudentToStudentDetails(student)

        d1 = json.dumps(studentDetails)
        return JSONResponse(d1)


@csrf_exempt
def deleteStudent(request):
    if request.method == 'DELETE':
        studentId = int(request.GET["studentId"])

        isDeleted = __instance.delete(studentId)

        res = {'deleted' : isDeleted}
        d1 = json.dumps(res)
        return JSONResponse(d1)


@csrf_exempt
def createStudent(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        obj = json.loads(body_unicode)

        name, age, studentId = adaptCreateStudentRequest(obj)

        __instance.insert(name, age, studentId)
        res = {'res': 'creates'}
        return JSONResponse(json.dumps(res))

@csrf_exempt
def updateStudent(request):
    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        obj = json.loads(body_unicode)

        fields = adaptUpdateStudentRequest(obj)

        __instance.update(**fields)

        res = {'res': 'updated'}

        return JSONResponse(json.dumps(res))


@csrf_exempt
def assignCourseToStudent(request):
    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        obj = json.loads(body_unicode)

        studentId, courseId = adaptAssinCourseToStudent(obj)

        __instance.assinCourseToStudent(studentId, courseId)

        res = {'res': 'updated'}

        return JSONResponse(json.dumps(res))

@csrf_exempt
def gradeStudent(request):
    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        obj = json.loads(body_unicode)

        studentId, courseId, grade = adaptGradeStudent(obj)

        __instance.setCourseGrade(studentId, courseId, grade)

        res = {'res': 'updated'}

        return JSONResponse(json.dumps(res))

@csrf_exempt
def searchStudents(request):
    if request.method == 'GET':

        filters = {}
        if 'name' in request.GET:
            filters['name'] =request.GET["name"]

        if 'age' in request.GET:
            filters['age'] = int(request.GET["age"])



        students = __instance.search(**filters)

        studentsDetails = []
        for student in students:
            studentDetails = adaptStudentToStudentDetails(student)

            studentsDetails.append(studentDetails)



        d1 = json.dumps(studentsDetails)
        return JSONResponse(d1)
