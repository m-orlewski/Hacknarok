from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json, mimetypes, threading, time

html_path = '/html'

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)

        if self.path == '/':
            self.path = '/index.html'
            data = open('html/index.html').read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(data, "utf-8"))
            return

        # # Clear the database before new game/round
        # elif self.path.startswith('/reset'):
        #     data = get_db()
        #     data.clear()
        #     self.send_response(200)
        #     self.send_header("Content-type", "text/html")
        #     self.end_headers()
        #     self.wfile.write(bytes("Database cleared", "utf-8"))
        #     return

        else:
            data = open(self.path[1::]).read()
            mimetype, _ = mimetypes.guess_type(self.path[1::])
            self.send_response(200)            
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(bytes(data, "utf-8"))
            return 



if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 8080), Serv)
    print("Running server on localhost:8080")
    httpd.serve_forever()
