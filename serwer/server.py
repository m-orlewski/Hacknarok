from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json, mimetypes, threading, time
from db import DB
from hashlib import sha256 
from jinja2 import Template, Environment, FileSystemLoader


html_path = '/html'

database = DB()

env = Environment(loader=FileSystemLoader('html'))


def create_location(dane):
    global database
    parsed_string = dane.split('=')
    dic = {}

    name = parsed_string[1].split('&')[0].strip()
    address = parsed_string[2].split('&')[0].strip()
    size = parsed_string[3].strip()
    hash_data = f'{name}{address}{size}'
    locationid = sha256( bytes(hash_data, encoding='utf-8') ).hexdigest()
    print(name, address, size, locationid)
    if database.add_location(locationid, name, address, int(size) ):
        return True
    return False

class Serv(BaseHTTPRequestHandler):
    global database
    
    def do_POST(self):
        print("Zapytanie POST")
        print(self.path)
        
        if self.path == '/create':
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length) 
            #Parse POST data, and send response
            if create_location(post_data.decode('utf-8')):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('ok', "utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('ok', "utf-8"))

    def do_GET(self):
        print(self.path)

        if self.path == '/':
            template = env.get_template('index.html')
            output_from_parsed_template = template.render(locations=database.get_all())

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(output_from_parsed_template, "utf-8"))
            return

        if self.path == '/create':
            path = 'html/create.html'
            self.path = '/create.html'
            data = open('html/create.html').read()
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
