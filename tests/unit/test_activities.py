import pytest

import src.app as app_module


def test_signup_for_activity_adds_student():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    previous_count = len(app_module.activities[activity_name]["participants"])

    # Act
    result = app_module.signup_for_activity(activity_name, email)

    # Assert
    assert result == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == previous_count + 1


def test_signup_for_activity_duplicate_raises_http_exception():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act / Assert
    with pytest.raises(app_module.HTTPException) as exc_info:
        app_module.signup_for_activity(activity_name, email)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Student already signed up"


def test_signup_for_invalid_activity_raises_http_exception():
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act / Assert
    with pytest.raises(app_module.HTTPException) as exc_info:
        app_module.signup_for_activity(activity_name, email)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Activity not found"
