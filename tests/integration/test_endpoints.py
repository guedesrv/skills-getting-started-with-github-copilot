import src.app as app_module


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_names = set(app_module.activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activity_names


def test_signup_endpoint_registers_student(client):
    # Arrange
    activity_name = "Programming Class"
    email = "testing@mergington.edu"
    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_endpoint_returns_404_for_missing_activity(client):
    # Arrange
    invalid_activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_endpoint_returns_400_for_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_root_redirects_to_static_index(client):
    # Arrange / Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in {302, 307, 308}
    assert response.headers["location"] == "/static/index.html"
