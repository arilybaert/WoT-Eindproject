class Students(Resource):
    # methods go here
    pass

class Classrooms(Resource):
    # methods go here
    pass
api.add_resource(Students, '/students')
api.add_resource(Classrooms, '/classrooms')