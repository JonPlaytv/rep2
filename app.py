<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text to Image Generator</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">
    <style>
        body {
            background-color: #f8f9fa;
        }

        .ui.container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            color: #000000;
        }

        .field {
            margin-bottom: 20px;
        }

        .field:last-child {
            margin-bottom: 0;
        }

        .field label {
            display: inline-block;
            margin-right: 10px;
            text-align: right;
            width: 120px;
        }

        .small-download-button {
            font-size: 12px;
            padding: 20px; /* Adjusted padding */
            width:200px; /* Set a specific width */
        }




        .field textarea,
        .field input[type="number"] {
            width: calc(100% - 130px); /* Adjusted width to make space for the seed field */
            padding: 15px;
            box-sizing: border-box;
        }

        .field textarea {
            height: 100px;
            resize: vertical;
        }

        .ui.button {
            width: 100%;
            padding: 15px;
            box-sizing: border-box;
        }

        #loading-spinner {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1000;
        }

        #result-container {
            margin-top: 20px;
            text-align: center;
        }

        #generated-image {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        #download-button {
            margin-top: 20px;
            width:20px;
        }

        #loading-spinner {
            display: none;
        }

        #result-container {
            display: none;
        }

        .ui.form .field:not(:first-child) {
            margin-top: 10px;
        }

        .ui.form .field:first-child {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="ui container mt-5">
        <h1>Text to Image Generator</h1>

        <form class="ui form" id="text-form">
            <div class="field">
                <label for="user-text">Prompt:</label>
                <textarea class="field" id="user-text" name="user_text" required></textarea>
            </div>

            <div class="field">
                <label for="negative-prompt">Negative Prompt:</label>
                <textarea class="field" id="negative-prompt" name="negative_prompt"></textarea>
            </div>

            <div class="field">
                <label for="width">Width:</label>
                <input type="number" class="field" id="width" name="width" min="0" max="5000" value="512">
            </div>

            <div class="field">
                <label for="height">Height:</label>
                <input type="number" class="field" id="height" name="height" min="0" max="5000" value="512">
            </div>

            <div class="field">
                <label for="steps">Steps:</label>
                <input type="number" class="field" id="steps" name="Steps" min="0" max="50" value="20">
            </div>

            <div class="field">
                <label for="seed">Seed:</label>
                <input type="number" class="field" id="seed" name="Seed" min="0" value="-1">
            </div>

            <button class="ui button primary" type="button" onclick="generateImage()">Generate Image</button>
        </form>

        <div id="loading-spinner">
            <div class="ui active inverted dimmer">
                <div class="ui large text loader">Loading</div>
            </div>
        </div>
        <div id="result-container">
            <img id="generated-image" class="ui image" alt="Generated Image">
            <button class="ui button primary mt-3 small-download-button" onclick="downloadImage()">Download Image</button>
        </div>
    </div>

    <script>
        const userTextInput = document.getElementById('user-text');
        const negativePromptInput = document.getElementById('negative-prompt');
        const widthInput = document.getElementById('width');
        const heightInput = document.getElementById('height');
        const stepsInput = document.getElementById('steps');
        const seedInput = document.getElementById('seed');
    
        async function generateImage() {
            const userText = userTextInput.value;
            const negativePrompt = negativePromptInput.value;
            const width = widthInput.value;
            const height = heightInput.value;
            const steps = stepsInput.value;
            const seed = seedInput.value;
            document.getElementById('loading-spinner').style.display = 'block';
    
            try {
                // Prepare the request body
                const requestBody = {
                    prompt: userText,
                    negative_prompt: negativePrompt,
                    width: parseInt(width),
                    height: parseInt(height),
                    steps: parseInt(steps),
                    seed: parseInt(seed)
                };
    
                // Send the request to the server for image generation
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestBody),
                });
    
                const result = await response.json();
                const generatedImage = document.getElementById('generated-image');
                generatedImage.src = `data:image/png;base64,${result.images[0]}`;
                document.getElementById('result-container').style.display = 'block';
    
                // Show the download button
                document.getElementById('download-button').style.display = 'block';
            } catch (error) {
                console.error(error);
            } finally {
                document.getElementById('loading-spinner').style.display = 'none';
            }
        }
    
        function downloadImage() {
            const imageData = document.getElementById('generated-image').src.split(",")[1];
            const link = document.createElement('a');
            link.href = `data:image/png;base64,${imageData}`;
            link.download = 'generated_image.png';
            link.click();
        }
    </script>
</body>
</html>
