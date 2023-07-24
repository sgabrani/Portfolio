import unittest
import os
from flask import template_rendered
from contextlib import contextmanager
from io import StringIO

os.environ[ 'TESTING' ] = 'true'
from app import app

#function is used to record the templates that get rendered and their context during the execution of a block of code
@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class AppTestCase(unittest. TestCase):
    def setUp(self):
        self.client = app.test_client()
        
    def test_home (self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h1 class=\"sub-title\">About Me</h1>" in html

    
    def test_home_rendered(self):
        with captured_templates(app) as templates:
            response = self.client.get("/")
            assert response.status_code == 200
            template, context = templates[0]

            # Check that the correct template was used
            assert template.name == "index.html" 

            # You can also check the context data passed to the template
            assert "location" in context 
            assert context["title"] == "MLH Fellow"  
        

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
    

    def test_timeline_post_valid(self):
        post_data = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'content': 'Test Content'
        }
        response = self.client.post("/api/timeline_post", data=post_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], post_data['name'])
        self.assertEqual(data['email'], post_data['email'])
        self.assertEqual(data['content'], post_data['content'])
    
    def test_timeline_post_then_get(self):
        post_data = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'content': 'Test Content'
        }
        post_response = self.client.post("/api/timeline_post", data=post_data)
        self.assertEqual(post_response.status_code, 200)
        get_response = self.client.get("/api/timeline_post")
        self.assertEqual(get_response.status_code, 200)
        get_data = get_response.get_json()
        self.assertIsInstance(get_data, dict)
        self.assertIn('timeline_posts', get_data)
        self.assertGreater(len(get_data['timeline_posts']), 0)
        self.assertEqual(get_data['timeline_posts'][0]['name'], post_data['name'])
        self.assertEqual(get_data['timeline_posts'][0]['email'], post_data['email'])
        self.assertEqual(get_data['timeline_posts'][0]['content'], post_data['content'])
    

    def test_timeline_page(self):
        response = self.client.get("/timeline")
        self.assertEqual(response.status_code, 200)

        # Check that the page title is present in the rendered HTML
        self.assertIn('<h3 class="title-a">Timeline</h3>', response.get_data(as_text=True))

        # Check that the form for posting a new timeline post is present in the rendered HTML
        self.assertIn('<form action="/api/timeline_post" method="POST">', response.get_data(as_text=True))

        # Check that the required inputs are present in the rendered HTML
        self.assertIn('<input type="text" id="name" name="name" required>', response.get_data(as_text=True))
        self.assertIn('<input type="email" id="email" name="email" required>', response.get_data(as_text=True))
        self.assertIn('<textarea id="content" name="content" rows="4" required></textarea>', response.get_data(as_text=True))

        # Check that the container for the timeline posts is present in the rendered HTML
        self.assertIn('<div id="timeline-posts"></div>', response.get_data(as_text=True))
    

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data = {"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html


        # POST request with empty content
        response = self.client.post("/api/timeline_post", data= {"name": "John Doe", "email": "john@example.com", "content":""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html


        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data= {"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html