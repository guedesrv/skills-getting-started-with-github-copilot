import src.app as app_module


def test_multiple_students_can_sign_up_for_same_activity(client):
    # Arrange
    activity_name = "Gym Class"
    emails = ["student1@mergington.edu", "student2@mergington.edu"]
    previous_count = len(app_module.activities[activity_name]["participants"])

    # Act
    for email in emails:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 200

    # Assert
    assert len(app_module.activities[activity_name]["participants"]) == previous_count + len(emails)
    assert all(email in app_module.activities[activity_name]["participants"] for email in emails)


def test_activity_list_reflects_new_signup(client):
    # Arrange
    activity_name = "Debate Team"
    email = "newparticipant@mergington.edu"
    before_response = client.get("/activities")
    before_data = before_response.json()
    before_count = len(before_data[activity_name]["participants"])

    # Act
    post_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    after_data = client.get("/activities").json()

    # Assert
    assert post_response.status_code == 200
    assert len(after_data[activity_name]["participants"]) == before_count + 1
    assert email in after_data[activity_name]["participants"]


def test_same_student_can_sign_up_for_multiple_activities(client):
    # Arrange
    email = "crossparticipant@mergington.edu"
    activities_to_join = ["Chess Club", "Art Studio"]

    # Act
    for activity_name in activities_to_join:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 200

    # Assert
    for activity_name in activities_to_join:
        assert email in app_module.activities[activity_name]["participants"]
