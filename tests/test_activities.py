"""
Test suite for the Mergington High School Activities API.

Tests cover all endpoints: getting activities, signing up for activities,
and unregistering from activities. Tests include both happy path scenarios
and error handling cases.
"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities(self, client):
        """Test that the activities endpoint returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200

        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0

        # Verify expected activities exist
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Swimming Club",
            "Art Workshop",
            "Music Ensemble",
            "Science Club",
            "Debate Team"
        ]
        for activity in expected_activities:
            assert activity in activities

        # Verify activity structure
        first_activity = activities[expected_activities[0]]
        assert "description" in first_activity
        assert "schedule" in first_activity
        assert "max_participants" in first_activity
        assert "participants" in first_activity
        assert isinstance(first_activity["participants"], list)


class TestSignup:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        email = "testuser@mergington.edu"
        activity = "Chess Club"

        # Get initial participant count
        response = client.get("/activities")
        initial_participants = response.json()[activity]["participants"].copy()

        # Sign up
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

        # Verify participant was added
        response = client.get("/activities")
        updated_participants = response.json()[activity]["participants"]
        assert email in updated_participants
        assert len(updated_participants) == len(initial_participants) + 1

    def test_signup_already_signed_up(self, client):
        """Test error when trying to sign up with email already registered."""
        email = "michael@mergington.edu"  # Already registered in Chess Club
        activity = "Chess Club"

        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_activity_not_found(self, client):
        """Test error when trying to sign up for non-existent activity."""
        email = "testuser@mergington.edu"
        activity = "Nonexistent Activity"

        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()


class TestUnregister:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client):
        """Test successful unregistration from an activity."""
        # First sign up a test user
        email = "testuser@mergington.edu"
        activity = "Programming Class"

        client.post(f"/activities/{activity}/signup?email={email}")

        # Verify user is signed up
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]

        # Unregister
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

        # Verify user was removed
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

    def test_unregister_not_registered(self, client):
        """Test error when trying to unregister someone not registered."""
        email = "notregistered@mergington.edu"
        activity = "Art Workshop"

        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"].lower()

    def test_unregister_activity_not_found(self, client):
        """Test error when trying to unregister from non-existent activity."""
        email = "testuser@mergington.edu"
        activity = "Nonexistent Activity"

        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
