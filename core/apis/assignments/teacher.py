from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments submitted to this teacher"""
    teacher_assignments = Assignment.filter(Assignment.teacher_id == p.teacher_id).all()
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    graded_assignment = Assignment.grading(grade_assignment_payload.id, p.teacher_id, grade_assignment_payload.grade)
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
