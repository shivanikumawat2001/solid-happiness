from flask import Flask, render_template, request
import requests
import os
import openai 
import pathlib
current_directory = os.getcwd()
new_directory = os.path.join(current_directory, 'templates')
pathlib.Path(new_directory).mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    description = request.form.get('description')
    api_url = "https://api.openai.com/v1/images/generations"
    model = "image-alpha-001"
    api_key = "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"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = """
    {
        """
    data += f'"model": "{model}",'
    data += f'"prompt": "{description}",'
    data += """
        "num_images":1,
        "size":"1024x1024",
        "response_format":"url"
    }
    """

    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code != 200:
        return "An error occurred: " + response.text
    image_url = response.json()['data'][0]['url']
    return render_template('generated_image.html', image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
