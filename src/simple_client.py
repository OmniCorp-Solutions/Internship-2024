import requests
import socketserver
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np

PORT = 8080


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image


def send_image(url, key, image_path, output_path):
    # B64 Encode the image
    encoded_image = encode_image(image_path)

    # Prepare the JSON payload
    payload = {"key": key, "image": encoded_image}

    # Send the POST request
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Print the response from the server
    print(f"Status Code: {response.status_code}")

    if(response.status_code == 200):
        data = json.loads(response.text)
        print(data['result'])
    else:
        print(f"Response: {response.text}")



def getData(image_path, output_path, key):
    # URL of the server endpoint
    root_url = "http://127.0.0.1:8080"
    endpoint = "facial_input"
    full_url = f"{root_url}/api/{endpoint}"

    send_image(full_url, key, image_path, output_path)
