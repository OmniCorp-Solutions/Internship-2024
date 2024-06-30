import requests
import socketserver
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np

PORT = 8080

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def send_image(url, key, image_path, output_path):
    # B64 Encode the image
    encoded_image = encode_image(image_path)

    # Prepare the JSON payload
    payload = {
        "key": key,
        "image": encoded_image
    }

    # Send the POST request
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Print the response from the server
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    data = json.loads(response.text)
    
    # Now save the image and display
    image_decoded = base64.b64decode(data["result"])
    image = Image.open(BytesIO(image_decoded))
    input_image = np.array(image)

    pillow_image = Image.fromarray(input_image)
    pillow_image.show()
    pillow_image.save(output_path, format="PNG")

if __name__ == "__main__":
    # URL of the server endpoint
    root_url = "http://127.0.0.1:8080"
    endpoint = "facial_input"
    full_url = f"{root_url}/api/{endpoint}"

    # Key to be sent
    key = "s$8cyGN7KHjEU@DyTY7s4^NwNhp&e"

    # Path to the image file
    image_path = "../../data/Validation/Johnny Depp/086_f052c533.jpg"

    #path to file output
    output_path = "..\..\data\Outputs\client_return.png"

    send_image(full_url, key, image_path, output_path)
