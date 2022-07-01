import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert "<h3>About Me:</h3>" in html
        assert "<h3  id=\"projects\">Projects:</h3>" in html
        assert "<h3 id=\"hobbies\">Hobbies:</h3>" in html
        assert "<h3 id=\"travels\">Places I've Been:</h3>" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert  "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_timeline_post_from_endpoints(self):
        #Creates new post and checks if it did it correctly
        post_request_response = self.client.post("/api/timeline_post", data=
        {"name": "Brandon", "email": "brandon@example.com", "content": "Hello world, I'm Brandon"})
        assert post_request_response.status_code == 200
        
        #Creates second post and checks if it did it correctly
        post_request_response2 = self.client.post("/api/timeline_post", data=
        {"name": "Kevin", "email": "kevin@example.com", "content": "Hello world, I'm Kevin"})
        assert post_request_response2.status_code == 200
        
        #Checking if the request is getting both posts
        get_request_response = self.client.get("/api/timeline_post")
        json = get_request_response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2
        
        #Checking if the most recent post has its name attribute corresponding to "Kevin"
        most_recent_post = json["timeline_posts"][0]
        assert most_recent_post["name"] ==  "Kevin"

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data=
        {"name": "", "email": "john@example.com", "content": "Hello world, I'm John"})
        assert response.status_code == 400
        message = response.get_data(as_text=True)
        assert "Invalid name" in message

        #POST request with empty content
        response = self.client.post("/api/timeline_post", data=
        {"name": "John Doe", "email" : "john@example.com", "content": ""})
        assert response.status_code == 400
        response = response.get_data(as_text=True)
        assert "Invalid content" in response
        
        #POST request with malformed email
        response = self.client.post("/api/timeline_post", data=
        {"name": "John Doe", "email" : "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        response = response.get_data(as_text=True)
        assert "Invalid email" in response 
        