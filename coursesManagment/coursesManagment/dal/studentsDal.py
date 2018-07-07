

#from pymongo import MongoClient
from .dbconnection import client
from bson.objectid import ObjectId

#client = MongoClient('localhost', 27017)

db = client.UniversityDB

class StudentsDal:

    def insert(self, name, age, studentId):

        return db.Students.insert_one(
            {
                "_id": studentId,
                "name": name,
                "age": age,
                "coursesGrades" : {}
            }).inserted_id

    def studentById(self, studentId):

        studentIt = self.search(_id = studentId)

        for student in studentIt:
            return student

        return None

    def adaptFields(self, kwargs):
        fields = {}
        for key, value in kwargs.items():
            if key == 'name' or key == 'age' or key == '_id':
                fields[key] = value

            else:
                raise Exception('unknon filter {0}'.format(key))

        return fields

    def search(self, **kwargs):

        filter = self.adaptFields(kwargs)

        student = db.Students.find(filter)

        return student

    def update(self, **kwargs):

        if kwargs is None or len(kwargs) == 0:
            raise Exception('missing update fields')

        fieldsToUpdate = self.adaptFields(kwargs)

        studentId = fieldsToUpdate['_id']
        del fieldsToUpdate['_id']

        return db.Students.update_one({"_id": studentId}, {"$set": fieldsToUpdate})


    def delete(self, studentId):
        result = db.Students.delete_one({'_id': studentId})
        return result.deleted_count > 0

    def assinCourseToStudent(self, studentId, courseId):
        db.Students.update(

            {'_id': studentId},
            {'$set': {'coursesGrades.{0}'.format(ObjectId(courseId)): None}}

          )

    def assinAllStudentsToCourse(self, courseId):
        db.Students.updateMany({}, {'$set': {'coursesIds.{0}'.format(courseId): None}})


    def courseStudents(self, courseId):

        students = db.collection.find({"coursesIds.{0}".format(courseId): {"$exists": True}})
        return students



    def setCourseGrade(self, studentId, courseId, grade):
        
        db.Students.update(

            {'_id': studentId},
            {'$set': {'coursesGrades.{0}'.format(ObjectId(courseId)): grade}}
        )


__instance = StudentsDal()

def instance():
    return __instance