# app.py

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get user input from the request using request.form.get
    user_text = request.form.get('user_text', '')

    # Make a request to your FastAPI endpoint
    response = requests.post('http://37.60.173.43:8080/sdapi/v1/txt2img', json={'text': user_text})

    # Assume the API responds with an image encoded in base64
    base64_image = response.json().get('base64_image')

    return render_template('result.html', base64_image=base64_image)

if __name__ == '__main__':
    app.run(debug=True)
