from core.models.assignments import AssignmentStateEnum


def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    print(response.json)
    
    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assingment_resubmitt_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only assignment in draft state can be submitted'

def test_invalid_assignment_submission(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 99,  # Non-existent assignment ID
            'teacher_id': 2
        })

    assert response.status_code == 404
    error_response = response.json
    assert error_response['error'] == 'FyleError'

def test_submit_assignment_as_teacher(client, h_teacher_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_teacher_1,
        json={
            'id': 1,
            'teacher_id': 2
        })

    assert response.status_code == 403
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'requester should be a student'

def test_unauthorized_request(client):
    response = client.get('/student/assignments')

    assert response.status_code == 401
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'UNAUTHORIZED'

def test_forbidden_request(client, h_teacher_1):
    response = client.get('/student/assignments', headers=h_teacher_1)

    assert response.status_code == 403
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'requester should be a student'

def test_bad_request_submit_assignment(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 9999,  # Non-existing assignment
            'teacher_id': 2
        })

    assert response.status_code == 404
    error_response = response.json
    assert error_response['error'] == 'FyleError'

def test_not_found_assignment(client, h_student_1):
    response = client.get('/student/assignments/9999', headers=h_student_1)

    assert response.status_code == 404
    error_response = response.json
    assert error_response['error'] == 'NotFound'
    assert error_response["message"] == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'




def test_update_assignment_non_draft_state_error(client, h_student_1):
    # Create a new assignment in draft state
    content = 'New draft assignment for test'
    create_response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        }
    )
    assert create_response.status_code == 200
    created_data = create_response.json['data']
    assignment_id = created_data['id']

    # Submit the assignment to change its state from DRAFT to SUBMITTED
    submit_response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': assignment_id,
            'teacher_id': 2
        }
    )
    assert submit_response.status_code == 200
    submitted_data = submit_response.json['data']
    assert submitted_data['state'] == 'SUBMITTED'


    new_content = 'Updated content for submitted assignment'
    update_response = client.post(f'/student/assignments',
    headers=h_student_1,
    json={
        'id': assignment_id,
        'content': new_content
    }
    )

    # Check if the response status code indicates an error as expected
    assert update_response.status_code == 400
    error_message = update_response.json['message']
    assert error_message == 'only assignment in draft state can be edited'

def test_successful_assignment_update(client, h_student_1):
    # Create a new assignment in draft state
    content = 'New draft assignment for test'
    create_response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        }
    )
    assert create_response.status_code == 200
    created_data = create_response.json['data']
    assignment_id = created_data['id']

    # Update the draft assignment
    new_content = 'Updated content for draft assignment'
    update_response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': assignment_id,
            'content': new_content
        }
    )

    # Check if the response status code indicates success
    assert update_response.status_code == 200
    updated_data = update_response.json['data']
    assert updated_data['id'] == assignment_id
    assert updated_data['content'] == new_content
    assert updated_data['state'] == 'DRAFT'






