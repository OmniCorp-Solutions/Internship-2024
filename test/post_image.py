import sys
import requests
import base64
import json

def main(image_path):
    # Read the image file and encode it to base64
    with open(image_path, 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Define the data to send in the POST request
    data = {
        'key': 'key1',  # Replace with the actual key to test
        'image': image_base64
    }
    
    # Send the POST request to the server
    url = 'http://localhost:8080/api/face'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Print the response from the server
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python post_image.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    main(image_path)
