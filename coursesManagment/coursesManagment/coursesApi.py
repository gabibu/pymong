from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
import json
from django.views.decorators.csrf import csrf_exempt

from .adapters.ApiAdapter import  adaptCreateCourseRequestRequest, \
    adaptUpdateCourseRequest, adaptToCourseDetails, adaptAssinCourseToStudent


from .dal.courseDal import __instance

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



@csrf_exempt
def courseDetails(request):
    if request.method == 'GET':
        courseId = request.GET["courseId"]

        course = __instance.courseById(courseId)
        courseDetails = adaptToCourseDetails(course)

        d1 = json.dumps(courseDetails)
        return JSONResponse(d1)


@csrf_exempt
def deleteCourse(request):
    if request.method == 'DELETE':
        courseId = request.GET["courseId"]

        isDeleted = __instance.delete(courseId)

        res = {'deleted' : isDeleted}
        d1 = json.dumps(res)
        return JSONResponse(d1)


@csrf_exempt
def createCourse(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        obj = json.loads(body_unicode)

        name, points = adaptCreateCourseRequestRequest(obj)

        courseId = __instance.insert(name, points)

        res = {'courseId': str(courseId)}

        return JSONResponse(json.dumps(res))

@csrf_exempt
def     updateCourse(request):
    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        obj = json.loads(body_unicode)

        fields = adaptUpdateCourseRequest(obj)

        __instance.update(**fields)

        res = {'res': 'updated'}

        return JSONResponse(json.dumps(res))
