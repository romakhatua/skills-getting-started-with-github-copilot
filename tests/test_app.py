"""
Unit tests for the Mergington High School API.
Uses the AAA (Arrange, Act, Assert) pattern.
"""

import pytest


class TestRoot:
    """Test suite for the root endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """Test that the root endpoint redirects to static/index.html."""
        # Arrange: TestClient is ready

        # Act: Make a GET request to root
        response = client.get("/", follow_redirects=False)

        # Assert: Check redirect status and location header
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that all activities are returned from the database."""
        # Arrange: Activities are pre-loaded in the app
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Drama Club",
            "Art Studio",
            "Debate Team",
            "Science Club"
        ]

        # Act: Make a GET request to /activities
        response = client.get("/activities")
        activities = response.json()

        # Assert: Check status code and content
        assert response.status_code == 200
        assert len(activities) == len(expected_activities)
        for activity in expected_activities:
            assert activity in activities

    def test_get_activities_contains_required_fields(self, client):
        """Test that each activity contains all required fields."""
        # Arrange: Expected fields in activity objects
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act: Fetch all activities
        response = client.get("/activities")
        activities = response.json()

        # Assert: Each activity has all required fields
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())

    def test_get_activities_returns_json(self, client):
        """Test that the endpoint returns JSON content type."""
        # Arrange: Expected content type
        expected_content_type = "application/json"

        # Act: Make a GET request
        response = client.get("/activities")

        # Assert: Check content type
        assert expected_content_type in response.headers["content-type"]


class TestRemoveParticipant:
    """Test suite for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_existing_participant(self, client):
        """Test removing a participant that exists in an activity."""
        # Arrange: Get initial participant count
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act: Remove participant
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert: Check response and participant was removed
        assert response.status_code == 200
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1
        assert email not in final_response.json()[activity_name]["participants"]

    def test_remove_participant_from_nonexistent_activity(self, client):
        """Test removing a participant from a non-existent activity."""
        # Arrange: Use an activity name that doesn't exist
        nonexistent_activity = "Nonexistent Club"
        email = "test@example.com"

        # Act: Attempt to remove participant
        response = client.delete(f"/activities/{nonexistent_activity}/participants/{email}")

        # Assert: Check for 404 error
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_nonexistent_participant(self, client):
        """Test removing a participant that doesn't exist in an activity."""
        # Arrange: Use valid activity but non-existent email
        activity_name = "Chess Club"
        nonexistent_email = "nonexistent@example.com"

        # Act: Attempt to remove non-existent participant
        response = client.delete(f"/activities/{activity_name}/participants/{nonexistent_email}")

        # Assert: Check for 404 error
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_remove_participant_returns_success(self, client):
        """Test that removing a participant returns a successful response."""
        # Arrange: Select existing activity and participant
        activity_name = "Programming Class"
        email = "emma@mergington.edu"

        # Act: Remove participant
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert: Check for successful response
        assert response.status_code == 200
        assert response.json() is not None