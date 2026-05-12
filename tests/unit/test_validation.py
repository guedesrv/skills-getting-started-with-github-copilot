import src.app as app_module


def test_activity_data_contains_required_fields():
    # Arrange
    activity_name = "Chess Club"

    # Act
    activity = app_module.activities[activity_name]

    # Assert
    assert set(activity.keys()) == {"description", "schedule", "max_participants", "participants"}
    assert isinstance(activity["participants"], list)


def test_all_activities_are_loaded():
    # Arrange / Act
    activities = app_module.activities

    # Assert
    assert len(activities) == 9
    assert "Art Studio" in activities
    assert "Science Club" in activities
