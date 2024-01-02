import unittest

from app import app


@app.route('/')
def index():
    return 'Hello, World!'


class TestApp(unittest.TestCase):

    def test_index(self):
        client = app.test_client()

        response = client.get('http://37.60.173.43:8080/')


        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')


    def test_generate(self):
        client = app.test_client()

        response = client.post('/generate', json={
            'prompt': 'A cat sitting on a table',
            'width': 512,
            'height': 512,
            'negative_prompt': 'A dog sitting on a table',
            'steps': 100
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)


    def test_queue_status(self):
        client = app.test_client()

        response = client.get('/queue/status')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)


if __name__ == '__main__':
    unittest.main()
t