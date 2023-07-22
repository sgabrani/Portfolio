import unittest
import os
from app import app
os.environ['TESTING'] = 'true'

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        html = response.get_data(as_text=True)

        # Check headers within index.html
        self.assertIn("<title>MLH Fellow</title>", html)
        self.assertIn("<h1 class=\"sub-title\">About Me</h1>", html)
        self.assertIn("<h1 class=\"sub-title\">My Experience</h1>", html)
        self.assertIn("<h1 class=\"sub-title\">My Projects</h1>", html)
        self.assertIn("<h1 class=\"sub-title\">Contact Me</h1>", html)
    
    def test_hobbies_page(self):
        response = self.client.get('/hobbies')
        self.assertEquals(response.status_code, 200)
        html = response.get_data(as_text=True)

        # Check headers in hobbies.html
        self.assertIn("other fun things besides computer science...", html)
        self.assertIn("Cool places I've been to", html)

    # def test_timeline_page(self):
    #     response = self.client.get("/timelines")
    #     assert response.status_code == 200
    #     html = response.get_data(as_text=True)

    #     # Check headers in timelines.html
    #     assert "<h1>Timeline</h1>" in html
    #     assert "<h2>Create a New Post</h2>" in html
    #     assert "<label for=\"name\">Name:</label>" in html
    #     assert "<label for=\"email\">Email:</label>" in html
    #     assert "<label for=\"content\">Content:</label>" in html
    #     assert "<button type=\"submit\" class=\"button\">Post</button>" in html
    #     assert "<h2>Timeline Posts</h2>" in html
    #     assert "<button class=\"button\" onclick=\"showList()\">Show Posts</button>" in html


    def test_timeline_api_get(self):
        response = self.client.get('/api/timeline_post')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.is_json)

        json = response.get_json()
        self.assertIn("timeline_posts", json)
        self.assertEquals(len(json['timeline_posts']), 0)

    def test_timeline_api_post(self):
        info = {
            'name': "Jane Doe",
            'email': "jane@doe.com",
            'content': "My name is Jane!"
        }
        response = self.client.post('/api/timeline_post', data=info)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.is_json)

        json = response.get_json()
        self.assertIn('id', json)
        self.assertEquals(json['name'], info['name'])
        self.assertEquals(json['email'], info['email'])
        self.assertEquals(json['content'], info['content'])


    def test_timeline_api_post_then_get(self):
        # POST testing
        info = {
            'name': "Jane Doe",
            'email': "jane@doe.com",
            'content': "My name is Jane!"
        }
        response_post = self.client.post('/api/timeline_post', data=info)
        self.assertEquals(response_post.status_code, 200)
        self.assertTrue(response_post.is_json)

        # GET testing
        response_get = self.client.get('/api/timeline_post')
        self.assertEquals(response_get.status_code, 200)
        self.assertTrue(response_get.is_json)

        json = response_get.get_json()
        self.assertIn("timeline_posts", json)
        self.assertGreater(len(json['timeline_posts']), 0)

        posts = json['timeline_posts']
        self.assertIn('id', posts[0])
        self.assertEquals(posts[0]['name'], info['name'])
        self.assertEquals(posts[0]['email'], info['email'])
        self.assertEquals(posts[0]['content'], info['content'])


    def test_timeline_api_post_then_delete(self):
        # POST testing
        info = {
            'name': "Jane Doe",
            'email': "jane@doe.com",
            'content': "My name is Jane!"
        }
        response = self.client.post('/api/timeline_post', data=info)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.is_json)

        json = response.get_json()
        self.assertIn('id', json)

        # DELETE testing
        delete_id = json['id']
        response = self.client.delete(f'/api/timeline_post/{delete_id}')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, b"Timeline post deleted successfully")
