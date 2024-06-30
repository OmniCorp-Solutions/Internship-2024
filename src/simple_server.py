import http.server
import socketserver
import json
import pickle
from urllib.parse import urlparse, parse_qs
import detector
import os

PORT = 8080

# Load the pickled database of keys. what if no keys yet?
if(os.path.isfile('keys_db.pkl')):
    with open('keys_db.pkl', 'rb') as f:
        keys_db = pickle.load(f)
else:
    keys_db = {}

def authenticator(key):
    #function to check pickled database for keys, can be changed later to improve security
    # for good security, you want the database itself encrypted. no plain text. ie zero-trust security modeling.
    return keys_db.get(key) or False

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/facial_input':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                key = data['key']
                image = data['image']
                
                if authenticator(key):
                    # Process the image
                    result = self.process_image(image)
                    response = {'status': 'success', 'result': result}
                else:
                    response = {'status': 'error', 'message': 'Key not found'}

                self._set_response()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self._set_response(400)
                response = {'status': 'error', 'message': str(e)}
                self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self._set_response(404)
            response = {'status': 'error', 'message': 'Not found'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def process_image(self, image):
        # Create object of class DataImport from detector
        face_rec = detector.DataImport()
        
        # Next process the image
        processed_image = face_rec.recognize_faces(image, True)
        
        return processed_image #return string to represent image with recognition data base64

def start():
    # Set up the server
    handler = SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)

    print(f"Serving on port {PORT}")
    httpd.serve_forever()
