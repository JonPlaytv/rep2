from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
from gevent.pywsgi import WSGIServer
import logging



app = Flask(__name__)


@app.route('/')
def index():
    ip_address = request.remote_addr
    logging.info(f'Accessed index route from IP: {ip_address}', extra={'ip': ip_address})
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/options', methods=['POST'])
def options():
    try:
        default_style = "revAnimated_v122EOL.safetensors [4199bcdd14]"
        style = request.json.get('sd_model_checkpoint')
        print(style) 
        # Set up options payload
        

        
        # Set the style based on the user's selection
        if style == "anime":
            sd_model_checkpoint = "darkSushiMixMix_225D.safetensors [cca17b08da]"
        elif style == "real":
            sd_model_checkpoint = "photon_v1.safetensors [ec41bd2a82]"
        elif style == "cartoon":
            sd_model_checkpoint = "realcartoonPixar_v7.safetensors [08de5efb8a]"
        else:
            sd_model_checkpoint = default_style

        option_payload = {
            'sd_model_checkpoint': sd_model_checkpoint
            
        }
        response_options = requests.post(url='http://37.60.173.43:8080/sdapi/v1/options', json=option_payload)
        response_options.raise_for_status()
        
        
        return jsonify({'success': True})
        
        
        
    except requests.RequestException as e:
        # Log API request error with IP address
        
        return jsonify({'error': f'Error making API request: {e}'}), 500    
        
        
        
        
        
        
       
        
























@app.route('/generate', methods=['POST'])
def generate():
    try:
        

        # Get user input from the request
        user_text = request.json.get('prompt')
        width = request.json.get('width')
        height = request.json.get('height')
        negative_prompt = request.json.get('negative_prompt')
        steps = request.json.get('steps')
        seed = request.json.get('seed')
        enable_nsfw = request.json.get('nsfw')
       
        

        

        # Validate user input
        if not user_text:
            return jsonify({'error': 'Missing prompt'}), 400

        # Prepare the request body for image generation
        payload = {
            'prompt': user_text,
            'width': width,
            'height': height,
            'negative_prompt': negative_prompt,
            'steps': steps,
            'seed': seed,
            'sampler_name': "DPM++ 2M Karras",
            

            'override_settings': {
                'nudenet_nsfw_censor_enable': enable_nsfw
            },
            "override_settings_restore_afterwards": True,
        }

        # Make a request to your FastAPI endpoint
        response = requests.post('http://37.60.173.43:8080/sdapi/v1/txt2img', json=payload)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Assume the API responds with an image encoded in base64
        prebase64_image = response.json().get('images')

        # Log successful generation with IP address
       

        # Return the response as JSON
        return jsonify({'images': prebase64_image})

    except requests.RequestException as e:
        # Log API request error with IP address
       
        return jsonify({'error': f'Error making API request: {e}'}), 500

    except Exception as e:
        # Log unexpected error with IP address
        
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@app.route('/queue/status')
def queue_status():
    try:
        ip_address = request.remote_addr

        # Make a request to the external server for queue status
        response = requests.get('http://37.60.173.43:8080/sdapi/v1/queuestats')
        response.raise_for_status()

        # Assume the API responds with a JSON object containing queue status
        queue_status = response.json()

        # Log successful queue status retrieval with IP address
        

        # Return the queue status as JSON
        return jsonify(queue_status)

    except requests.RequestException as e:
        # Log API request error with IP address
        
        return jsonify({'error': f'Error making API request: {e}'}), 500

    except Exception as e:
        # Log unexpected error with IP address
    
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
