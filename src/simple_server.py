import http.server
import socketserver
import json
import pickle
from urllib.parse import urlparse, parse_qs

PORT = 8080

# Load the pickled database of keys
with open('keys_db.pkl', 'rb') as f:
    keys_db = pickle.load(f)

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/face':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                key = data['key']
                image = data['image']
                
                if key in keys_db:
                    # Process the image (this is just a placeholder)
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
        # Placeholder for image processing function
        return "Processed image data"

# Set up the server
handler = SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)

print(f"Serving on port {PORT}")
httpd.serve_forever()
