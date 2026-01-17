#!/usr/bin/env python3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

class TaskFlowHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/health':
            response = {'status': 'ok', 'message': 'Backend running!', 'service': 'taskflow-backend'}
        elif self.path == '/api/test':
            response = {'status': 'success', 'message': 'API is working!', 'version': '1.0.0'}
        else:
            self.send_response(404)
            response = {'error': 'Endpoint not found'}
        
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    PORT = 5000
    server = HTTPServer(('0.0.0.0', PORT), TaskFlowHandler)
    print(f'[TaskFlow] Server running on port {PORT}')
    print(f'[TaskFlow] Health: GET http://localhost:{PORT}/health')
    server.serve_forever()