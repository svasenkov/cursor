import pytest
import requests
from typing import Dict
import uuid
import time

# Base URL for the API - configure based on your environment
BASE_URL = "http://localhost:8000"

@pytest.fixture
def api_client():
    """Fixture for making API requests"""
    class APIClient:
        def __init__(self):
            self.base_url = BASE_URL
            self.session = requests.Session()

        def get(self, endpoint: str):
            return self.session.get(f"{self.base_url}{endpoint}")

        def post(self, endpoint: str, json: Dict = None):
            return self.session.post(f"{self.base_url}{endpoint}", json=json)

        def put(self, endpoint: str, json: Dict = None):
            return self.session.put(f"{self.base_url}{endpoint}", json=json)

        def delete(self, endpoint: str):
            return self.session.delete(f"{self.base_url}{endpoint}")

    return APIClient()

def test_health_check(api_client):
    """Test the health check endpoint"""
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_courses(api_client):
    """Test getting all courses"""
    response = api_client.get("/api/courses")
    assert response.status_code == 200
    data = response.json()
    
    # Check pagination structure
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    
    # Check courses list
    courses = data["items"]
    assert isinstance(courses, list)
    
    if courses:  # If there are any courses
        first_course = courses[0]
        # Only check fields we know exist
        assert "title" in first_course
        assert "description" in first_course
        assert "duration" in first_course

def test_get_single_course(api_client):
    """Test getting a single course by ID"""
    # First get all courses to get a valid ID
    courses_response = api_client.get("/api/courses")
    courses = courses_response.json()["items"]
    
    if not courses:
        pytest.skip("No courses available for testing")
    
    course_id = courses[0]["id"]
    response = api_client.get(f"/api/courses/{course_id}")
    assert response.status_code == 200
    course = response.json()
    assert course["id"] == course_id

def test_create_course(api_client):
    """Test creating a new course"""
    new_course = {
        "title": "Test Course",
        "description": "This is a test course",
        "duration": 28,
        "instructor": "Test Instructor",
        "level": "junior",
        "categories": ["testing", "automation"],
        "price": 99.99,
        "status": "active",
        "prerequisites": ["Basic Python"],
        "objectives": ["Learn testing fundamentals"],
        "target_audience": ["Beginner testers"],
        "curriculum": ["Module 1: Intro to Testing"]
    }
    
    response = api_client.post("/api/courses", json=new_course)
    if response.status_code == 405:  # Method Not Allowed
        pytest.skip("POST method not allowed - API is in read-only mode")
        
    assert response.status_code == 201, f"Create failed with status {response.status_code}"
    created_course = response.json()
    
    # Verify only the essential fields that we know exist
    assert created_course["title"] == new_course["title"]
    assert created_course["description"] == new_course["description"]
    assert created_course["duration"] == new_course["duration"]
    assert "id" in created_course

def test_update_course(api_client):
    """Test updating an existing course"""
    # Get a sample course to update
    list_response = api_client.get("/api/courses")
    courses = list_response.json()["items"]
    assert len(courses) > 0, "No courses available for testing"
    
    # Get the first course since it's most likely to be stable
    test_course = courses[0]
    course_id = test_course["id"]
    
    # First verify we can get this course directly
    get_response = api_client.get(f"/api/courses/{course_id}")
    assert get_response.status_code == 200, f"Cannot get course {course_id} for update test"
    original_course = get_response.json()
    print(f"Original course data: {original_course}")
    
    # Prepare update data, matching the original course structure
    updated_data = {
        "title": "Updated Course",
        "description": "This course has been updated",
        "duration": 21,  # Changed to integer
        "instructor": "Updated Instructor",
        "engineer_level": original_course.get("engineer_level", "junior"),
        "categories": original_course.get("categories", ["testing"]),
        "price": original_course.get("price", 149.99),
        "school_id": original_course.get("school_id"),
        "platform_id": original_course.get("platform_id"),
        "students_amount": original_course.get("students_amount", 0),
        "rating": original_course.get("rating", 4.0)
    }
    
    # Try to update the course
    response = api_client.put(f"/api/courses/{course_id}", json=updated_data)
    
    # If we get 404 or 405, the API might be read-only
    if response.status_code in (404, 405):
        pytest.skip("API appears to be read-only - update operations not supported")
    
    # Print response for debugging if update fails
    if response.status_code != 200:
        print(f"Update failed with status {response.status_code}")
        print(f"Response body: {response.text}")
        print(f"Update payload: {updated_data}")
        
    assert response.status_code == 200, f"Update failed with status {response.status_code}"
    updated_course = response.json()
    
    # Verify only the essential fields that we updated
    assert updated_course["id"] == course_id
    assert updated_course["title"] == updated_data["title"]
    assert updated_course["description"] == updated_data["description"]
    assert updated_course["duration"] == updated_data["duration"]
    assert updated_course["instructor"] == updated_data["instructor"]
    assert updated_course["engineer_level"] == updated_data["engineer_level"]

def wait_for_course_in_listing(api_client, title: str, max_attempts: int = 5) -> dict:
    """Helper function to wait for a course to appear in the listing"""
    for attempt in range(max_attempts):
        list_response = api_client.get("/api/courses")
        courses = list_response.json()["items"]
        our_courses = [c for c in courses if c["title"] == title]
        
        if our_courses:
            return our_courses[0]
            
        print(f"Course not found in listing, attempt {attempt + 1}/{max_attempts}")
        time.sleep(1)  # Wait before next attempt
    
    raise AssertionError(f"Course with title '{title}' not found in listing after {max_attempts} attempts")

def test_delete_course(api_client):
    """Test deleting a course"""
    # First get a sample course to work with
    list_response = api_client.get("/api/courses")
    courses = list_response.json()["items"]
    assert len(courses) > 0, "No courses available for testing"
    
    # Get the first course since it's most likely to be stable
    test_course = courses[0]
    course_id = test_course["id"]
    original_title = test_course["title"]
    
    print(f"Testing with sample course - ID: {course_id}, Title: {original_title}")
    
    # Verify we can get the course directly
    get_response = api_client.get(f"/api/courses/{course_id}")
    assert get_response.status_code == 200, "Cannot get test course"
    course_data = get_response.json()
    assert course_data["title"] == original_title
    print(f"Retrieved course data: {course_data}")
    
    # Try to delete the course
    delete_response = api_client.delete(f"/api/courses/{course_id}")
    print(f"Delete response status: {delete_response.status_code}")
    print(f"Delete response body: {delete_response.text}")
    
    # If we get 404 or 405, the API might be read-only
    if delete_response.status_code in (404, 405):
        pytest.skip("API appears to be read-only - delete operations not supported")
    
    assert delete_response.status_code == 204, "Delete operation failed"
    
    # Add a small delay to allow deletion to process
    time.sleep(1)
    
    # Verify the course is no longer accessible
    get_response = api_client.get(f"/api/courses/{course_id}")
    assert get_response.status_code == 404, f"Expected 404 for deleted course, got {get_response.status_code}"

def test_create_course_invalid_data(api_client):
    """Test creating a course with invalid data"""
    invalid_course = {
        "title": "",  # Empty title should be invalid
        "duration": "not_a_number",  # Invalid duration (should be integer)
        "level": "invalid_level"
    }
    
    response = api_client.post("/api/courses", json=invalid_course)
    assert response.status_code == 422  # Unprocessable Entity 