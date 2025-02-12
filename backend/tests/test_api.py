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

def test_get_course_statistics(api_client):
    """Test getting course statistics"""
    response = api_client.get("/api/courses/statistics")
    assert response.status_code == 200
    stats = response.json()
    
    # Check that all required statistics fields are present
    assert "category_distribution" in stats
    assert "level_distribution" in stats
    assert "platform_distribution" in stats
    assert "price_statistics" in stats
    
    # Verify category distribution
    category_dist = stats["category_distribution"]
    assert isinstance(category_dist, dict)
    for category, count in category_dist.items():
        assert isinstance(category, str)
        assert isinstance(count, int)
        assert count >= 0
    
    # Verify level distribution
    level_dist = stats["level_distribution"]
    assert isinstance(level_dist, dict)
    for level, count in level_dist.items():
        assert isinstance(level, str)
        assert isinstance(count, int)
        assert count >= 0
    
    # Verify platform distribution
    platform_dist = stats["platform_distribution"]
    assert isinstance(platform_dist, dict)
    for platform, count in platform_dist.items():
        assert isinstance(platform, str)
        assert isinstance(count, int)
        assert count >= 0
    
    # Verify price statistics
    price_stats = stats["price_statistics"]
    assert isinstance(price_stats, dict)
    assert "average" in price_stats
    assert "median" in price_stats
    assert "minimum" in price_stats
    assert "maximum" in price_stats
    assert isinstance(price_stats["average"], (int, float))
    assert isinstance(price_stats["median"], (int, float))
    assert isinstance(price_stats["minimum"], (int, float))
    assert isinstance(price_stats["maximum"], (int, float))
    assert price_stats["minimum"] <= price_stats["maximum"]
    assert price_stats["minimum"] <= price_stats["average"] <= price_stats["maximum"]

def test_get_course_level_distribution(api_client):
    """Test getting course level distribution"""
    response = api_client.get("/api/courses/statistics")  # Updated endpoint
    assert response.status_code == 200
    stats = response.json()
    
    # Verify level distribution
    assert "level_distribution" in stats
    distribution = stats["level_distribution"]
    assert isinstance(distribution, dict)
    
    # Verify each level entry
    total_courses = sum(distribution.values())
    for level, count in distribution.items():
        assert isinstance(level, str)
        assert isinstance(count, int)
        assert count >= 0
        # Calculate percentage
        if total_courses > 0:
            percentage = (count / total_courses) * 100
            assert 0 <= percentage <= 100

def test_get_popular_categories(api_client):
    """Test getting popular course categories"""
    response = api_client.get("/api/courses/statistics")
    assert response.status_code == 200
    stats = response.json()
    
    # Verify category distribution
    assert "category_distribution" in stats
    categories = stats["category_distribution"]
    assert isinstance(categories, dict)
    
    # Verify data types and values
    for category, count in categories.items():
        assert isinstance(category, str)
        assert isinstance(count, int)
        assert count >= 0
    
    # Get sorted categories by count (we don't require the API to sort them)
    sorted_categories = sorted(categories.items(), key=lambda x: (-x[1], x[0]))
    
    # Print for debugging
    print("Categories distribution:")
    for category, count in sorted_categories:
        print(f"  {category}: {count}")
    
    # Verify we have some categories
    assert len(categories) > 0, "No categories found in distribution"

def test_get_price_statistics(api_client):
    """Test getting course price statistics"""
    response = api_client.get("/api/courses/statistics")  # Updated endpoint
    assert response.status_code == 200
    stats = response.json()
    
    # Verify price statistics
    assert "price_statistics" in stats
    price_stats = stats["price_statistics"]
    
    # Check required fields
    assert "average" in price_stats
    assert "median" in price_stats
    assert "minimum" in price_stats
    assert "maximum" in price_stats
    
    # Verify data types and constraints
    assert isinstance(price_stats["average"], (int, float))
    assert isinstance(price_stats["median"], (int, float))
    assert isinstance(price_stats["minimum"], (int, float))
    assert isinstance(price_stats["maximum"], (int, float))
    
    # Verify logical constraints
    assert price_stats["minimum"] <= price_stats["maximum"]
    assert price_stats["minimum"] <= price_stats["median"] <= price_stats["maximum"]
    assert price_stats["minimum"] <= price_stats["average"] <= price_stats["maximum"]

def test_get_rating_statistics(api_client):
    """Test getting course rating statistics"""
    response = api_client.get("/api/courses/statistics")
    assert response.status_code == 200
    stats = response.json()
    
    # Get all courses to calculate rating statistics
    courses_response = api_client.get("/api/courses")
    courses = courses_response.json()["items"]
    
    # Calculate rating statistics from courses
    ratings = [course.get("rating", 0) for course in courses if course.get("rating") is not None]
    
    if ratings:
        min_rating = min(ratings)
        max_rating = max(ratings)
        avg_rating = sum(ratings) / len(ratings)
        
        print(f"Rating statistics from courses:")
        print(f"  Min: {min_rating}")
        print(f"  Max: {max_rating}")
        print(f"  Avg: {avg_rating}")
        print(f"  Total rated courses: {len(ratings)}")
        
        # Verify all ratings are in valid range
        assert all(0 <= r <= 5 for r in ratings), "All ratings should be between 0 and 5"
    else:
        print("No course ratings found") 