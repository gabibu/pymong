
from .dbconnection import client

db = client.UniversityDB
from bson.objectid import ObjectId


class CoursesDal:

    def insert(self, name, points):

      return db.Courses.insert_one(
            {
                "name": name,
                "points": points
            }).inserted_id

    def courseByName(self, name):

        return list(self.fetch(name = name))

    def courseById(self, courseId):

        filter = {}
        filter['_id'] = ObjectId(courseId)

        return db.Courses.find_one(filter)



    def update(self, **kwargs):

        if kwargs is None or len(kwargs) == 0:
            raise Exception('missing update fields')

        fieldsToUpdate = self.__toFilter(kwargs)

        courseId = fieldsToUpdate['_id']
        del fieldsToUpdate['_id']

        return db.Courses.update_one({"_id": courseId}, {"$set": fieldsToUpdate})

    def delete(self, courseId):

        result = db.Courses.delete_one({'_id': ObjectId(courseId) })
        return result.deleted_count > 0


    def fetch(self, **kwargs):

        filter = self.__toFilter(kwargs)

        courses = db.Courses.find(filter)

        return courses


    def __toFilter(self, kwargs):

        if kwargs is None or len(kwargs) == 0:
            raise Exception('missing filters')

        filter = {}

        for key, value in kwargs.items():
            if key == 'name' or key == 'points' or key == '_id':

                filter[key] = ObjectId(value) if key == '_id' else value

            else:
                raise Exception('unknon filter {0}'.format(key))

        return filter


__instance = CoursesDal()


