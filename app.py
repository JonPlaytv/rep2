from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
from gevent.pywsgi import WSGIServer


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get user input from the request
        user_text = request.json.get('prompt')
        width = request.json.get('width')
        height = request.json.get('height')
        negative_prompt = request.json.get('negative_prompt')
        steps = request.json.get('steps')  # Use request.json instead of request.form
        seed = request.json.get('seed')  # Use request.json instead of request.form
        # Make a request to your FastAPI endpoint
        response = requests.post('http://37.60.173.43:8080/sdapi/v1/txt2img', json={
            'prompt': user_text,
            'width': width,
            'height': height,
            'negative_prompt': negative_prompt,
            'steps': steps,
            'seed' : seed
        })

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Assume the API responds with an image encoded in base64
        base64_image = response.json().get('images')

        return jsonify({'images': base64_image})

    except requests.RequestException as e:
        return jsonify({'error': f'Error making API request: {e}'}), 500

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@app.route('/queue/status')
def queue_status():
    # Make a request to the external server for queue status
    response = requests.get('http://37.60.173.43:8080/queue/status')

    # Return the response from the external server
    return jsonify(response.json())

app.route('/nudenet/censor', methods=['POST'])
def nsfw():
    try:
        # Get user input from the request
        nsfw = request.json.get('nsfw')
       
        response = requests.post('http://37.60.173.43:8080/nudenet/censor', json={
            'enable_nudenet': nsfw,
            
        })

        return jsonify({'success': True})

    except requests.RequestException as e:
        return jsonify({'error': f'Error making API request: {e}'}), 500

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500







if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
